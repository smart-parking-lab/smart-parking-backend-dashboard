import uuid
from sqlalchemy import Column, UUID, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.model.base import Base
from sqlalchemy.orm import relationship

class ParkingSession(Base):
    __tablename__ = "parking_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"))
    entry_time = Column(DateTime(timezone=True), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    entry_image_url = Column(String(255), nullable=True)
    exit_image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    vehicle = relationship("Vehicle", backref="parking_sessions")

    @property
    def plate_number(self) -> str:
        return self.vehicle.plate_number if self.vehicle else "Unknown"