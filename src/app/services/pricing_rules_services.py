from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.model import PricingRule
from app.schemas.pricing_rules import PricingRuleCreate, PricingRuleResponse, updatePricingRule
from app.services.admin_services import check_admin
from app.model.vehicle_type import VehicleType

from sqlalchemy.orm import selectinload

async def creat_new_pricing_rule(db: AsyncSession, pricing_rule: PricingRuleCreate, user_id: str) -> PricingRuleResponse:
    await check_admin(db, user_id)
    result = await db.execute(select(VehicleType).filter(VehicleType.id == pricing_rule.vehicle_type_id))
    vehicle_type = result.scalars().first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    
    new_pricing_rule = PricingRule(**pricing_rule.dict())
    db.add(new_pricing_rule)
    await db.commit()
    await db.refresh(new_pricing_rule)
    return new_pricing_rule

async def get_all_pricing_rules(db: AsyncSession) -> list[PricingRuleResponse]:
    result = await db.execute(select(PricingRule).options(selectinload(PricingRule.vehicle_type)))
    return result.scalars().all()

async def update_pricing_rule(db: AsyncSession, pricing_rule_new: updatePricingRule, user_id: str) -> PricingRuleResponse:
    await check_admin(db, user_id)
    result = await db.execute(select(PricingRule).filter(PricingRule.id == pricing_rule_new.id))
    pricing_rule = result.scalars().first()
    
    if not pricing_rule:
        raise HTTPException(status_code=404, detail="Pricing rule not found")
    
    # Check if vehicle type exists
    vt_result = await db.execute(select(VehicleType).filter(VehicleType.id == pricing_rule_new.vehicle_type_id))
    vehicle_type = vt_result.scalars().first()
    
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
    
    await db.commit()
    await db.refresh(pricing_rule)
    return pricing_rule