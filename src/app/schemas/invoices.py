
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class InvoiceResponse(BaseModel):
    id: UUID
    session_id: UUID
    pricing_rule_id: Optional[UUID]
    duration_minutes: Optional[float]
    amount: Optional[float]
    status: str
    payment_method: Optional[str]
    paid_at: Optional[datetime]

class InvoiceCreate(BaseModel):
    session_id: UUID
    
class InvoiceCheckout(BaseModel):
    id: UUID
    time_total: int

class InvoicePay(BaseModel):
    id: UUID
    payment_method: str