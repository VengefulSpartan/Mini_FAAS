from sqlalchemy import Column, String, Text
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), default="python") # Add this!
    status = Column(String(20), nullable=False)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)