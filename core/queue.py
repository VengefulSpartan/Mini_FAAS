import redis
import json

# Ankit's connection logic
client = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = "demo_queue"

def enqueue_job(job_id: str) -> bool:
    """
    Takes a real job_id from FastAPI and pushes it into Ankit's Redis queue.
    """
    try:
        # We push just the job_id. The actual code stays safely in MySQL.
        client.lpush(QUEUE_NAME, job_id)
        print(f"--> [QUEUE] Pushed Job ID to Redis: {job_id}")
        return True
    except redis.ConnectionError:
        print("🚨 ERROR: Could not connect to Redis.")
        return False