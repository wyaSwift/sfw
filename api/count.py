import json
import os
from http.server import BaseHTTPRequestHandler
import redis

r = redis.from_url(os.environ["REDIS_URL"])

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        keys = r.keys("session:*")
        players = []
        for key in keys:
            val = r.get(key)
            if val:
                try:
                    players.append(json.loads(val))
                except:
                    pass

        body = json.dumps({ "count": len(players), "players": players })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass
