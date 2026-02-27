import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.queue import enqueue_job

# Import schemas and database tools
from Schema import JobSubmitRequest, JobSubmitResponse, JobStatusEnum
from api.database import engine, get_db
from api import models

# 1. This line actually creates the 'mini_faas.db' file on your laptop
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-FaaS API")


# 2. We add 'db: Session = Depends(get_db)' so FastAPI gives us database access
@app.post("/submit", response_model=JobSubmitResponse)
def submit_job(request: JobSubmitRequest, db: Session = Depends(get_db)):
    new_job_id = str(uuid.uuid4())

    db_job = models.Job(
        id=new_job_id,
        code=request.code,
        status=JobStatusEnum.QUEUED.value
    )

    db.add(db_job)
    db.commit()

    # --- THE NEW LINE ---
    # After saving to MySQL, drop the ID into Ankit's Redis queue
    enqueue_job(new_job_id)

    return JobSubmitResponse(
        job_id=new_job_id,
        status=JobStatusEnum.QUEUED
    )