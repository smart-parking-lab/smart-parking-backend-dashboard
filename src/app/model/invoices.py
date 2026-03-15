from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.model.base import Base
from sqlalchemy.orm import relationship

class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("parking_sessions.id"), nullable=False, unique=True)
    pricing_rule_id = Column(UUID(as_uuid=True), ForeignKey("pricing_rules.id"), nullable=True)
    duration_minutes = Column(Numeric, nullable=True)
    amount = Column(Numeric, nullable=True)
    status = Column(String(20), nullable=False, default="unpaid")
    payment_method = Column(String(20), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    session = relationship("ParkingSession", backref="invoices")
    pricing_rule = relationship("PricingRule", backref="invoices")