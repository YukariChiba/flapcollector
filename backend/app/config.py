import os

BIND_IP = os.environ.get("FLAP_BIND_IP", "127.0.0.1")
BIND_PORT = int(os.environ.get("FLAP_PORT", "8179"))

BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

SERVERS_CONFIG_FILE = os.path.join(DATA_DIR, "servers.json")
STATUS_FILE = os.path.join(DATA_DIR, "status.json")

CACHE_DURATION = int(os.environ.get("FLAP_CACHE_DURATION", "300"))  # 5 minutes
VALIDITY_WINDOW = int(os.environ.get("FLAP_VALIDITY_WINDOW", "1200"))  # 20 minutes
