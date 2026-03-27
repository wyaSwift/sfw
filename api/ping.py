import json
import os
from http.server import BaseHTTPRequestHandler
import redis

r = redis.from_url(os.environ["REDIS_URL"])
TIMEOUT = 30

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except:
            self._respond(400, "invalid json")
            return

        player_id = data.get("id")
        if not player_id:
            self._respond(400, "missing id")
            return

        # Store id, username, and job id together
        payload = json.dumps({
            "id": player_id,
            "username": data.get("username", "Unknown"),
            "jobId": data.get("jobId", "")
        })
        r.setex(f"session:{player_id}", TIMEOUT, payload)
        self._respond(200, "ok")

    def _respond(self, status, text):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(text.encode())

    def log_message(self, format, *args):
        pass
