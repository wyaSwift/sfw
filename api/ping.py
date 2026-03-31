import json
import os
from http.server import BaseHTTPRequestHandler
import redis

r = redis.from_url(os.environ["REDIS_URL"])
TIMEOUT = 30  # seconds — Roblox script should ping every ~15s


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors(200)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._respond(400, {"error": "invalid json"})
            return

        player_id = data.get("id")
        if not player_id:
            self._respond(400, {"error": "missing id"})
            return

        payload = json.dumps({
            "id":       str(player_id),
            "username": data.get("username", "Unknown"),
            "jobId":    data.get("jobId", ""),
        })

        r.setex(f"session:{player_id}", TIMEOUT, payload)
        self._respond(200, {"status": "ok"})

    def _respond(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._add_cors()
        self.end_headers()
        self.wfile.write(body)

    def _cors(self, status):
        self.send_response(status)
        self._add_cors()
        self.end_headers()

    def _add_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass
