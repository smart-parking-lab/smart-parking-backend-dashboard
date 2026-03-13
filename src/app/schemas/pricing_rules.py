from pydantic import BaseModel
from uuid import UUID
from datetime import time

class PricingRuleBase(BaseModel):
    name: str
    price_per_hour: float
    price_per_day: float
    apply_after_minutes: int
    start_time: time
    end_time: time
    days_of_week: str
    priority: int
    is_active: bool
    vehicle_type_id: UUID

class PricingRuleCreate(PricingRuleBase):
    pass

class PricingRuleResponse(BaseModel):
    name: str
    price_per_hour: float
    price_per_day: float
    apply_after_minutes: int
    start_time: time
    end_time: time
    days_of_week: str
    priority: int
    is_active: bool
    vehicle_type_name: str

    class Config:
        from_attributes = True

class updatePricingRule(PricingRuleBase):
    id: UUID