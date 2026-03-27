import time
from ping import USERS  # if memory persisted (won't survive serverless cold starts)

TIMEOUT = 30

def handler(request):
    now = time.time()
    # remove inactive
    to_delete = [uid for uid, ts in USERS.items() if now - ts > TIMEOUT]
    for uid in to_delete:
        USERS.pop(uid)
    return {"status": 200, "body": json.dumps({"count": len(USERS)})}
