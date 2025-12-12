#!/usr/bin/env python3
import os
import time
from app.config import (
    API_BIND_IP,
    API_BIND_PORT,
    CACHE_DURATION,
    COLLECTOR_BIND_IP,
    COLLECTOR_BIND_PORT,
    CONFIG_DIR,
)
from app.utils import setup_logging, load_servers_config, logger
from app.server import start_http_server
from app.tcp import start_tcp_server
from app.logic import poll_servers


def main():
    setup_logging()
    os.makedirs(CONFIG_DIR, exist_ok=True)

    start_tcp_server(COLLECTOR_BIND_IP, COLLECTOR_BIND_PORT)
    start_http_server(API_BIND_IP, API_BIND_PORT)

    logger.info("Service started. Waiting for connections...")

    while True:
        loop_start = time.time()

        config = load_servers_config()

        poll_servers(config)

        elapsed = time.time() - loop_start
        sleep_time = max(0, CACHE_DURATION - elapsed)

        if sleep_time > 0:
            time.sleep(sleep_time)
        
        elapsed = time.time() - loop_start
        sleep_time = max(0, CACHE_DURATION - elapsed)
        
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Stopping...")
