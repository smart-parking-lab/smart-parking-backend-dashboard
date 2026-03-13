from fastapi import HTTPException
from app.schemas.pricing_rules import PricingRuleBase,updatePricingRule

def validate_pricing_rule(pricing_rule: PricingRuleBase) -> PricingRuleBase:
    if not pricing_rule.name:
        raise HTTPException(status_code=400, detail="Name is required")
    if pricing_rule.price_per_hour <=0:
        raise HTTPException(status_code=400, detail="Price per hour is required")
    if pricing_rule.price_per_day <=0:
         raise HTTPException(status_code=400, detail="Price per day is required")
    if pricing_rule.apply_after_minutes <=0:
        raise HTTPException(status_code=400, detail="Apply after minutes is required")
    if not pricing_rule.start_time:
        raise HTTPException(status_code=400, detail="Start time is required")
    if not pricing_rule.end_time:
        raise HTTPException(status_code=400, detail="End time is required")
    if pricing_rule.start_time >= pricing_rule.end_time:
        raise HTTPException(status_code=400,detail="start_time must be before end_time")
    if not pricing_rule.days_of_week:
        raise HTTPException(status_code=400, detail="Days of week is required")
    if not pricing_rule.priority:
        raise HTTPException(status_code=400, detail="Priority is required")
    if not pricing_rule.is_active:
        raise HTTPException(status_code=400, detail="Is active is required")
    if not pricing_rule.vehicle_type_id:
        raise HTTPException(status_code=400, detail="Vehicle type id is required")
    
    return pricing_rule

def validate_update_pricing_rule(pricing_rule: updatePricingRule) -> updatePricingRule:
    if not pricing_rule.id:
        raise HTTPException(status_code=400, detail="Id is required")
    validate_pricing_rule(pricing_rule) 
    return pricing_rule