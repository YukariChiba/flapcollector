import json
import logging
import os
from app.config import SERVERS_CONFIG_FILE
from app.models import ServerConfig
from typing import Dict

logger = logging.getLogger("FlapTracker")

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def load_servers_config() -> Dict[str, ServerConfig]:
    if not os.path.exists(SERVERS_CONFIG_FILE):
        return {}
    try:
        with open(SERVERS_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load servers config: {e}")
        return {}
