import json
import os
from http.server import BaseHTTPRequestHandler
import redis

r = redis.from_url(os.environ["REDIS_URL"])


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors(200)

    def do_GET(self):
        keys = r.keys("session:*")
        players = []
        for key in keys:
            val = r.get(key)
            if val:
                try:
                    players.append(json.loads(val))
                except Exception:
                    pass

        self._respond(200, {
            "count":   len(players),
            "players": players,
        })

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
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass
