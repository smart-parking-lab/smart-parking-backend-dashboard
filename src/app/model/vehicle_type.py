import uuid
from sqlalchemy import Column, String, DateTime,UUID
from sqlalchemy.sql import func
from .base import Base

class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    display_name = Column(String)
    icon = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at =Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    