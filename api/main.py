import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.queue import enqueue_job
from fastapi import FastAPI, Depends, HTTPException

# Import schemas and database tools
from Schema import JobSubmitRequest, JobSubmitResponse, JobStatusEnum, JobStatusResponse
from api.database import engine, get_db
from api import models

# 1. This line actually creates the 'mini_faas.db' file on your laptop
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-FaaS API")


# 2. We add 'db: Session = Depends(get_db)' so FastAPI gives us database access
@app.post("/submit", response_model=JobSubmitResponse)
def submit_job(request: JobSubmitRequest, db: Session = Depends(get_db)):
    new_job_id = str(uuid.uuid4())

    # 1. Create the database record
    db_job = models.Job(
        id=new_job_id,
        code=request.code,
        language=request.language,  # <--- The culprit!
        status=JobStatusEnum.QUEUED.value
    )

    db.add(db_job)
    db.commit()

    # 2. Push to Redis queue
    # The worker will use this ID to look up the code AND the language from MySQL
    enqueue_job(new_job_id)

    return JobSubmitResponse(
        job_id=new_job_id,
        status=JobStatusEnum.QUEUED
    )

@app.get("/status/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    # 1. Search the MySQL database for this exact ID
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    # 2. If it doesn't exist, throw a 404 error
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 3. If it does exist, return the current status and any output
    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        output=job.output,
        error=job.error
    )