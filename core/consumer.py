import redis
import json
import time

client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "demo_queue"

def consume():
    print("Waiting for jobs...")

    while True:
        _, data = client.brpop(QUEUE_NAME)
        job = json.loads(data)

        print(f"Processing: {job}")
        time.sleep(2)  # simulate processing
        print(f"Completed job {job['id']}")

if __name__ == "__main__":
    consume()