import json
import time

# temporary in-memory store (won't persist across serverless invocations)
USERS = {}

def handler(request):
    body = json.loads(request.get_data())
    user_id = body.get("id")
    if not user_id:
        return {"status": 400, "body": "bad"}

    USERS[user_id] = time.time()
    return {"status": 200, "body": "ok"}
