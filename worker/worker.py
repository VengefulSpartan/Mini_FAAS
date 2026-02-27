import time
import redis
from api.database import SessionLocal
from api import models
from core.executor import execute_code

# 1. Standardized Redis connection
# We use 'client' to match your queue.py naming convention
client = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = "job_queue"


def process_jobs():
    """
    Background worker that listens for Job IDs from Redis,
    fetches the code from MySQL, and executes it in a Docker container.
    """
    print("Worker is live and listening for Polyglot jobs... 🚀")

    while True:
        try:
            # 2. BLPOP blocks until a Job ID appears in the 'job_queue'
            # This is efficient because it doesn't waste CPU when the queue is empty.
            job_data = client.blpop(QUEUE_NAME, timeout=0)

            if job_data:
                # job_data is a tuple: (b'job_queue', b'job_id_string')
                job_id = job_data[1].decode("utf-8")
                print(f"--- Processing Job: {job_id} ---")

                # 3. Create a fresh Database session
                db = SessionLocal()
                try:
                    # Fetch the full job details from the MySQL database
                    job = db.query(models.Job).filter(models.Job.id == job_id).first()

                    if job:
                        # Update status to PROCESSING so the frontend shows progress
                        job.status = "PROCESSING"
                        db.commit()

                        # 4. Trigger the Polyglot Executor
                        # This spins up the Docker container for C, C++, or Python
                        print(f"Executing {job.language} code...")
                        result = execute_code(job.code, job.language)

                        # 5. Save the results back to the MySQL database
                        job.status = result["status"]
                        job.output = result.get("output")
                        job.error = result.get("error")
                        db.commit()

                        print(f"Job {job_id} finished. Status: {job.status}")
                    else:
                        print(f"⚠️ Error: Job {job_id} not found in database.")

                except Exception as e:
                    print(f"❌ Database/Execution Error: {e}")
                finally:
                    db.close()

        except redis.ConnectionError:
            print("🚨 Redis Connection Error. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"🚨 Unexpected Worker Error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    process_jobs()