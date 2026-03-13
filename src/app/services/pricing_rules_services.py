from app.validators.vehicle_validator import validate_vehicle_type_name
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model import PricingRule
from app.schemas.pricing_rules import PricingRuleCreate,PricingRuleResponse,updatePricingRule
from app.services.admin_services import check_admin
from app.model.vehicle_type import VehicleType

def creat_new_pricing_rule(db: Session, pricing_rule: PricingRuleCreate, user_id: str) -> PricingRuleResponse:
    check_admin(db, user_id)
    vehicle_type = db.query(VehicleType).filter(VehicleType.id == pricing_rule.vehicle_type_id).first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    
    new_pricing_rule = PricingRule(**pricing_rule.dict())
    db.add(new_pricing_rule)
    db.commit()
    db.refresh(new_pricing_rule)
    return new_pricing_rule

def get_all_pricing_rules(db: Session) -> list[PricingRuleResponse]:
    
    pricing_rules = db.query(PricingRule).all()
    
    return pricing_rules

def update_pricing_rule(db: Session, pricing_rule_new: updatePricingRule,user_id:str) -> PricingRuleResponse:
    check_admin(db,user_id)
    pricing_rule = db.query(PricingRule).filter(PricingRule.id == pricing_rule_new.id).first()
    
    if not pricing_rule:
        raise HTTPException(status_code=404, detail="Pricing rule not found")
    
    # Check if vehicle type exists
    vehicle_type = db.query(VehicleType).filter(VehicleType.id == pricing_rule_new.vehicle_type_id).first()
    
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    
    pricing_rule.name = pricing_rule_new.name
    pricing_rule.price_per_hour = pricing_rule_new.price_per_hour
    pricing_rule.price_per_day = pricing_rule_new.price_per_day
    pricing_rule.apply_after_minutes = pricing_rule_new.apply_after_minutes
    pricing_rule.start_time = pricing_rule_new.start_time
    pricing_rule.end_time = pricing_rule_new.end_time
    pricing_rule.days_of_week = pricing_rule_new.days_of_week
    pricing_rule.priority = pricing_rule_new.priority
    pricing_rule.is_active = pricing_rule_new.is_active
    pricing_rule.vehicle_type_id = pricing_rule_new.vehicle_type_id
    db.commit()
    db.refresh(pricing_rule)
    return pricing_rule