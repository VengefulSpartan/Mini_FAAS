from pydantic import BaseModel
from enum import Enum

class JobStatusEnum(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class LanguageEnum(str, Enum):
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    JAVA = "java"

class JobSubmitRequest(BaseModel):
    code: str
    language: str  # Use 'str' here to prevent the 422 error

class JobSubmitResponse(BaseModel):
    job_id: str
    status: JobStatusEnum

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatusEnum
    output: str | None = None
    error: str | None = None