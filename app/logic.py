import time
import json
import threading
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from collections import defaultdict
from typing import Dict

from app.config import CACHE_DURATION, VALIDITY_WINDOW, DATA_DIR, STATUS_FILE
from app.models import ServerConfig
from app.state import update_server_data, get_snapshot, remove_server_data
from app.utils import logger

def fetch_url(url: str, timeout=10):
    try:
        req = Request(url, headers={'User-Agent': 'FlapTracker/1.0'})
        with urlopen(req, timeout=timeout) as response:
            return json.load(response)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        logger.warning(f"Fetch error for {url}: {e}")
        return None

def poll_single_server(name: str, config: ServerConfig):
    url = config.get('url')
    if not url:
        return

    target_url = f"{url.rstrip('/')}/flaps/active/compact"
    raw_data = fetch_url(target_url)

    if raw_data is not None:
        processed = []
        for item in raw_data:
            processed.append({
                "prefix": item.get('Prefix'),
                "server": name,
                "info": {
                    "FirstSeen": item.get('FirstSeen', 0),
                    "RateSec": item.get('RateSec', 0),
                    "TotalCount": item.get('TotalCount', 0)
                }
            })
        update_server_data(name, processed)

def poll_servers(config: Dict[str, ServerConfig]):
    threads = []
    
    for name, conf in config.items():
        if conf.get('mode') == 'poll':
            t = threading.Thread(target=poll_single_server, args=(name, conf))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

def clean_expired_data(config: Dict[str, ServerConfig]) -> Dict[str, bool]:
    now = int(time.time())
    status_map = {}
    configured_names = set(config.keys())
    
    snapshot = get_snapshot()
    
    to_remove = []
    for name, entry in snapshot.items():
        if name not in configured_names:
            to_remove.append(name)
            continue
        
        ts = entry['timestamp']
        if (now - ts) > (CACHE_DURATION + 10):
            status_map[name] = False
            to_remove.append(name)
        else:
            status_map[name] = True
            
    for name in to_remove:
        remove_server_data(name)

    for name in configured_names:
        if name not in status_map:
            status_map[name] = False
            
    return status_map

def generate_files(status_map: Dict[str, bool]):
    now = int(time.time())
    
    with open(STATUS_FILE, 'w') as f:
        json.dump({"generated": now, "servers": status_map}, f)

    active_count = sum(1 for v in status_map.values() if v)

    logger.info(f"Aggregating data from {active_count} active servers...")

    grouped = defaultdict(list)
    snapshot = get_snapshot()

    for name, entry in snapshot.items():
        if not status_map.get(name):
            continue
        for row in entry['data']:
            grouped[row['prefix']].append({
                "server": row['server'],
                "info": row['info']
            })

    aggregated_rows = []
    for prefix, occurrences in grouped.items():
        metadata = {item['server']: item['info'] for item in occurrences}
        max_len = 128 if ':' in prefix else 32
        aggregated_rows.append({
            "prefix": prefix,
            "asn": "0",
            "maxLength": max_len,
            "metadata": metadata,
            "count": len(occurrences)
        })

    limits = [1, 2, 3, 5, 7, 11]
    base_obj = {
        "metadata": {
            "generated": now,
            "valid": now + VALIDITY_WINDOW
        }
    }

    for limit in limits:
        roas = [
            {k: v for k, v in row.items() if k != 'count'}
            for row in aggregated_rows if row['count'] >= limit
        ]
        
        output_data = base_obj.copy()
        output_data["roas"] = roas
        
        filename = "all.json" if limit == 1 else f"min_{limit}.json"
        with open(os.path.join(DATA_DIR, filename), 'w') as f:
            json.dump(output_data, f)
            
    logger.info("Aggregation complete.")
