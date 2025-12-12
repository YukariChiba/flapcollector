import json
import socket
import socketserver
import threading
import time

from app.state import update_server_data
from app.utils import load_servers_config, logger

# instance_name -> socket_object
_active_connections = {}
_conn_lock = threading.Lock()


class CollectorHandler(socketserver.StreamRequestHandler):
    def handle(self):
        instance_name = None
        try:
            # Phase 1: Send: HELLO
            line = self.rfile.readline().decode("utf-8").strip()
            if not line.startswith("HELLO"):
                return

            # Phase 1: Recv: VERSION
            self.rfile.readline()

            # Phase 2: Sent: INSTANCE
            self.wfile.write(b"INSTANCE\n")
            self.wfile.flush()

            # Phase 2: Recv: collectorInstanceName
            instance_name = self.rfile.readline().decode("utf-8").strip()
            if not instance_name:
                return

            config = load_servers_config()
            server_conf = config.get(instance_name)

            # Temporary: only servers in server_conf and in tcp mode is allowed
            if not server_conf or server_conf.get("mode") != "tcp":
                self.wfile.write(b"ERROR: Unknown instance or not in tcp mode\n")
                return

            # Force 1 instance_name <--> 1 conn
            with _conn_lock:
                existing_sock = _active_connections.get(instance_name)
                if existing_sock:
                    try:
                        existing_sock.shutdown(socket.SHUT_RDWR)
                        existing_sock.close()
                    except Exception:
                        pass
                    logger.info(f"Dropped duplicate connection for {instance_name}")

                _active_connections[instance_name] = self.request

            logger.info(f"TCP Monitor connected: {instance_name}")

            # rate limit: 15 cmds/min
            # ACTIVE_FLAPS -> SLEEP 10 -> PING -> SLEEP 10 = 1 cmds / 10s (6 cmds/min)
            while True:
                self.wfile.write(b"ACTIVE_FLAPS\n")
                self.wfile.flush()

                resp = self.rfile.readline().decode("utf-8").strip()
                if not resp:
                    break

                if not resp.startswith("ERROR"):
                    try:
                        payload = json.loads(resp)
                        self._process_data(instance_name, payload)
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON from {instance_name}")

                time.sleep(5)

                self.wfile.write(b"PING\n")
                self.wfile.flush()

                resp = self.rfile.readline().decode("utf-8").strip()
                if not resp:
                    break  # disconnected
                # Expect PONG

                time.sleep(5)

        except (ConnectionResetError, BrokenPipeError, OSError):
            pass
        finally:
            # Cleanup registry only if we are the current active connection
            if instance_name:
                with _conn_lock:
                    if _active_connections.get(instance_name) == self.request:
                        del _active_connections[instance_name]
                logger.info(f"TCP Monitor disconnected: {instance_name}")

    def _process_data(self, name, payload):
        if not isinstance(payload, list):
            return
        processed = []
        for item in payload:
            processed.append(
                {
                    "prefix": item.get("Prefix"),
                    "server": name,
                    "info": {
                        "FirstSeen": item.get("FirstSeen", 0),
                        "RateSec": item.get("RateSec", 0),
                        "TotalCount": item.get("TotalCount", 0),
                    },
                }
            )
        update_server_data(name, processed)


def start_tcp_server(ip, port):
    class DualStackTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        address_family = socket.AF_INET6 if ":" in ip else socket.AF_INET

    server = DualStackTCPServer((ip, port), CollectorHandler)
    server.daemon_threads = True

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logger.info(f"TCP Collector started on {ip}:{port}")
