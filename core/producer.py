import redis
import json
import time
from datetime import datetime

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "demo_queue"

def push_jobs():
    for i in range(1, 6):
        job = {
            "id": i,
            "message": f"Job number {i}",
            "timestamp": datetime.now().isoformat()
        }

        client.lpush(QUEUE_NAME, json.dumps(job))
        print(f"Pushed: {job}")
        time.sleep(1)

if __name__ == "__main__":
    push_jobs()