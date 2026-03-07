from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password= Column(String)
    full_name = Column(String)
    phone = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at =Column(DateTime(timezone=True), server_default=func.now())

    