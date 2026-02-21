from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# Enums help avoid typos (e.g. "Queued" vs "QUEUED")
class JobStatusEnum(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# 1. What Frontend sends
class JobSubmitRequest(BaseModel):
    code: str = Field(..., description="The Python code to execute", min_length=1)


# 2. What is returned to frontend
class JobSubmitResponse(BaseModel):
    job_id: str
    status: str = JobStatusEnum.QUEUED


# 3. What sits in the Database and what frontend sees when polling
class JobResult(BaseModel):
    job_id: str
    status: JobStatusEnum
    output: Optional[str] = None
    error: Optional[str] = None