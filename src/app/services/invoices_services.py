from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from app.model.invoices import Invoice
from app.model.parking_sessions import ParkingSession
from app.model.pricing_rules import PricingRule
from app.model.vehicle_type import VehicleType
from app.model.vehicle import Vehicle
from app.schemas.invoices import InvoiceCreate, InvoiceCheckout, InvoicePay,RevenueResponse,InvoiceResponse
from sqlalchemy.orm import Session
from app.model.user import User

def create_invoice(db: Session, payload: InvoiceCreate):
    session = db.query(ParkingSession).filter(ParkingSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session không tồn tại")
    
    invoice = Invoice(**payload.dict())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def checkout_invoice(db: Session, payload: InvoiceCheckout):
    invoice = db.query(Invoice).filter(Invoice.id == payload.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice không tồn tại")
    if invoice.status != "unpaid":
        raise HTTPException(status_code=400, detail="Invoice đã được thanh toán")
    
    now = datetime.now()
    day_of_week = now.weekday()
    current_time = now.strftime("%H:%M:%S")
    if day_of_week == 5  or day_of_week == 6:
        day_of_week = "SAT-SUN"
    else:
        day_of_week = "MON-FRI"
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == invoice.session.vehicle_id).first()
    vehicle_type = db.query(VehicleType).filter(VehicleType.id == vehicle.vehicle_type_id).first()

    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type không tồn tại")
    pricing_rule = db.query(PricingRule).filter(PricingRule.vehicle_type_id == vehicle_type.id, PricingRule.days_of_week == day_of_week, current_time >= PricingRule.start_time, current_time <= PricingRule.end_time).first()
    if not pricing_rule:
        raise HTTPException(status_code=404, detail="Pricing rule không tồn tại")
    invoice.pricing_rule_id = pricing_rule.id
    invoice.duration_minutes = payload.time_total
    if invoice.duration_minutes > 1440:
        invoice.amount = invoice.duration_minutes/1440 * pricing_rule.price_per_day
    else:
        invoice.amount = invoice.duration_minutes/60 * pricing_rule.price_per_hour
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def pay_invoice(db: Session, payload: InvoicePay):
    invoice = db.query(Invoice).filter(Invoice.id == payload.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice không tồn tại")
    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice đã được thanh toán")
    
    invoice.status = "paid"
    invoice.paid_at = datetime.now()
    invoice.payment_method = payload.payment_method
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def get_revenue(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")
    invoices = db.query(Invoice).all()
    total_revenue = 0
    total_paid_invoices = 0
    list_invoices = []
    for invoice in invoices:
        amount = invoice.amount or 0
        total_revenue += amount
        if invoice.status == "paid":
            total_paid_invoices += amount
        list_invoices.append(InvoiceResponse.model_validate(invoice))
    return RevenueResponse(
        total_revenue=total_revenue,
        total_paid_invoices=total_paid_invoices,
        list_invoices=list_invoices
    )