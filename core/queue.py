import redis

client = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = "job_queue"  # Changed to job_queue

def enqueue_job(job_id: str) -> bool:
    try:
        # Using rpush to push to the end of the line
        client.rpush(QUEUE_NAME, job_id)
        print(f"--> [QUEUE] Pushed Job ID to Redis: {job_id}")
        return True
    except redis.ConnectionError:
        print("🚨 ERROR: Could not connect to Redis.")
        return False