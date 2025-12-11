#!/usr/bin/env python3
import time
import os
from app.config import BIND_IP, BIND_PORT, CACHE_DURATION, DATA_DIR, PUBLIC_DIR
from app.utils import setup_logging, load_servers_config, logger
from app.server import start_server
from app.logic import poll_servers, clean_expired_data, generate_files

def main():
    setup_logging()
    
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    start_server(BIND_IP, BIND_PORT)

    logger.info("Starting main loop...")

    while True:
        loop_start = time.time()
        
        config = load_servers_config()
        
        poll_servers(config)
        
        status_map = clean_expired_data(config)
        
        generate_files(status_map)
        
        elapsed = time.time() - loop_start
        sleep_time = max(0, CACHE_DURATION - elapsed)
        
        if sleep_time > 0:
            logger.info(f"Sleeping {sleep_time:.1f}s...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Stopping...")
