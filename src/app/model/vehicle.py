import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UUID, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    vehicle_type_id= Column(UUID, ForeignKey("vehicle_types.id"))
    plate_number = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="vehicles")
    vehicle_type = relationship("VehicleType", backref="vehicles")

    