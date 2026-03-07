from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at =Column(DateTime(timezone=True), server_default=func.now())
