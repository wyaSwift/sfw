import json
import os
from http.server import BaseHTTPRequestHandler
import redis

r = redis.from_url(os.environ["REDIS_URL"])

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Count all keys matching session:* — expired ones are auto-removed by Redis
        keys = r.keys("session:*")
        count = len(keys)

        body = json.dumps({"count": count})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass

