import os

API_BIND_IP = os.environ.get("FLAP_API_BIND_IP", "127.0.0.1")
API_BIND_PORT = int(os.environ.get("FLAP_API_BIND_PORT", "8179"))
COLLECTOR_BIND_IP = os.environ.get("FLAP_COLLECTOR_BIND_IP", "127.0.0.1")
COLLECTOR_BIND_PORT = int(os.environ.get('FLAP_COLLECTOR_BIND_PORT', '9179'))

BASE_DIR = os.getcwd()
CONFIG_DIR = os.path.join(BASE_DIR, "config")
STATIC_DIR = os.path.join(BASE_DIR, "public")
SERVERS_CONFIG_FILE = os.path.join(CONFIG_DIR, "servers.json")

CACHE_DURATION = int(os.environ.get("FLAP_CACHE_DURATION", "300"))  # 5 minutes
VALIDITY_WINDOW = int(os.environ.get("FLAP_VALIDITY_WINDOW", "1200"))  # 20 minutes
