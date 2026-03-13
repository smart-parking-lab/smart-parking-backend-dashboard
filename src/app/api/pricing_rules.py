from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.pricing_rules import PricingRuleCreate, PricingRuleResponse, updatePricingRule
from app.services import pricing_rules_services
from app.utils.database import get_db
from app.validators import pricing_rules_validator

router = APIRouter(prefix="/pricing-rules", tags=["Pricing Rules"])

@router.post("", response_model=PricingRuleResponse, status_code=201)
def create_pricing_rule(request: Request, payload: PricingRuleCreate, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    pricing_rules_validator.validate_pricing_rule(payload)
    return pricing_rules_services.creat_new_pricing_rule(db, payload, user_id)

@router.get("", response_model=list[PricingRuleResponse])
def get_all_pricing_rules(db: Session = Depends(get_db)):
    return pricing_rules_services.get_all_pricing_rules(db)

@router.put("/update", response_model=PricingRuleResponse)
def update_pricing_rule(request: Request, payload: updatePricingRule, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    pricing_rules_validator.validate_update_pricing_rule(payload)
    return pricing_rules_services.update_pricing_rule(db, payload, user_id)
