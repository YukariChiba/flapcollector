import json
import mimetypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from app.config import DATA_DIR, PUBLIC_DIR
from app.state import remove_server_data, update_server_data
from app.utils import load_servers_config, logger


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        path = self.path.split('?')[0]
        
        if path not in ['/start', '/end']:
            self.send_error(404, "Endpoint not found")
            return
        
        instance_name = self.headers.get("X-Instance-Name")

        if not instance_name:
            self.send_error(400, "Missing X-Instance-Name header")
            return

        config = load_servers_config()
        server_conf = config.get(instance_name)

        if not server_conf or server_conf.get("mode") != "webhook":
            self.send_error(403, "Unknown instance or not in webhook mode")
            return

        if path == '/start':
            self._handle_start(instance_name)
        elif path == '/end':
            self._handle_end(instance_name)

    def _handle_start(self, instance_name):
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
        except Exception as e:
            logger.error(f"Invalid JSON from {instance_name}: {e}")
            self.send_error(400, "Invalid JSON")
            return

        processed = self._process_payload(payload, instance_name)
        update_server_data(instance_name, processed)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def _handle_end(self, instance_name):
        remove_server_data(instance_name)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def _process_payload(self, payload, server_name):
        if not isinstance(payload, list):
            payload = [payload]
        result = []
        for item in payload:
            if "Prefix" not in item:
                continue
            result.append(
                {
                    "prefix": item.get("Prefix"),
                    "server": server_name,
                    "info": {
                        "FirstSeen": item.get("FirstSeen", 0),
                        "RateSec": item.get("RateSec", 0),
                        "TotalCount": item.get("TotalPathChanges", 0),
                    },
                }
            )
        return result

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        if not path or path.endswith("/"):
            path = "index.html"

        if ".." in path:
            self.send_error(403, "Forbidden")
            return

        file_path = self._find_file(path)

        if file_path:
            self._serve_file(file_path)
        else:
            self.send_error(404, "File not found")

    def _find_file(self, path: str) -> Optional[str]:
        p1 = os.path.join(DATA_DIR, path)
        if os.path.isfile(p1):
            return p1

        p2 = os.path.join(PUBLIC_DIR, path)
        if os.path.isfile(p2):
            return p2

        return None

    def _serve_file(self, full_path: str):
        try:
            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                mime_type = "application/octet-stream"

            with open(full_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")  # 方便调试
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            logger.error(f"Error serving file {full_path}: {e}")
            self.send_error(500, "Internal Server Error")

    def log_message(self, format, *args):
        pass


def start_server(ip, port):
    server = HTTPServer((ip, port), RequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logger.info(f"Server started on {ip}:{port}")
