import threading
import time
from typing import Dict, Any

# { "server_name": { "timestamp": int, "data": [FlapEntry] } }
_data_store: Dict[str, Any] = {}
_data_lock = threading.Lock()

def update_server_data(server_name: str, data: list):
    with _data_lock:
        _data_store[server_name] = {
            "timestamp": int(time.time()),
            "data": data
        }

def get_snapshot():
    with _data_lock:
        return _data_store.copy()

def remove_server_data(server_name: str):
    with _data_lock:
        if server_name in _data_store:
            del _data_store[server_name]
