import threading

from flask import Flask, abort, jsonify, request

from app.config import STATIC_DIR
from app.logic import clean_expired_data, get_aggregated_roas, get_status_json
from app.utils import load_servers_config, logger

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")


def get_context():
    config = load_servers_config()
    status_map = clean_expired_data(config)
    return status_map


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/servers")
@app.route("/servers.json")
def servers():
    return jsonify(load_servers_config())


@app.route("/status")
@app.route("/status.json")
def status():
    return jsonify(get_status_json(get_context()))


# legacy
@app.route("/all")
@app.route("/all.json")
def all_roas():
    return jsonify(get_aggregated_roas(get_context(), min_count=1))


# legacy
@app.route("/min_<int:count>")
@app.route("/min_<int:count>.json")
def min_roas(count):
    if count < 1:
        abort(400)
    return jsonify(get_aggregated_roas(get_context(), min_count=count))


@app.route("/roa")
@app.route("/roa.json")
def filter_roas():
    rate = request.args.get("rate", default=0, type=int)
    vote = request.args.get("vote", default=1, type=int)

    if vote < 1:
        vote = 1

    return jsonify(get_aggregated_roas(get_context(), min_count=vote, min_rate=rate))


def start_http_server(ip, port):
    # Run Flask in a daemon thread to allow main.py to keep polling
    server_thread = threading.Thread(
        target=app.run,
        kwargs={"host": ip, "port": port, "debug": False, "use_reloader": False},
        daemon=True,
    )
    server_thread.start()
    logger.info(f"HTTP API started on {ip}:{port}")
