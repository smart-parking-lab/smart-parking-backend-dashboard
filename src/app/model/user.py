import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String)
    password= Column(String)
    full_name = Column(String)
    phone = Column(String)
    role_id = Column(UUID, ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    role = relationship("Role", backref="users")

    