from fastapi import APIRouter, Depends, Form, Path
from sqlalchemy.orm import Session
from app.schemas.invoices import InvoiceResponse, InvoiceCreate, InvoiceCheckout, InvoicePay
from app.services import invoices_services
from app.utils.database import get_db

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("", response_model=InvoiceResponse, status_code=201)
async def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    return  invoices_services.create_invoice(db, payload)

@router.put("/{id}", response_model=InvoiceResponse, status_code=200)
async def update_invoice(payload: InvoiceCheckout,db: Session = Depends(get_db)):
    return  invoices_services.checkout_invoice(db, payload)

@router.put("/{id}/pay", response_model=InvoiceResponse, status_code=200)
async def pay_invoice(payload: InvoicePay,db: Session = Depends(get_db)):
    return  invoices_services.pay_invoice(db, payload)



