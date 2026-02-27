from sqlalchemy import Column, String, Text
from api.database import Base

class Job(Base):
    __tablename__ = "jobs"

    # Added (36) for the UUID and (50) for the status!
    id = Column(String(36), primary_key=True, index=True)
    status = Column(String(50), default="QUEUED")
    code = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)