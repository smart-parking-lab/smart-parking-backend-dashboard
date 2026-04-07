import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import Invoice, ParkingSession
from fastapi import HTTPException
from datetime import datetime
from app.utils.mqtt_client import mqtt_client
from app.services.invoices_services import checkout_invoice, create_invoice
from app.schemas.invoices import InvoiceCheckout, InvoiceCreate


async def create_parking_session(db: AsyncSession, plate_number: str, url: str):

    parking_session = ParkingSession(
        plate_number=plate_number,
        entry_time=datetime.now(),
        status="active",
        entry_image_url=url,
    )
    db.add(parking_session)
    await db.commit()
    await db.refresh(parking_session)
    await create_invoice(db, InvoiceCreate(session_id=parking_session.id))
    mqtt_client.open_servo("SERVO_IN")
    return parking_session

async def get_all_parking_sessions(db: AsyncSession):
    result = await db.execute(select(ParkingSession))
    return result.scalars().all()

async def get_parking_session_by_id(db: AsyncSession, session_id: uuid.UUID):
    result = await db.execute(select(ParkingSession).filter(ParkingSession.id == session_id))
    parking_session = result.scalars().first()
    if not parking_session:
        raise HTTPException(status_code=404, detail="Parking session not found")
    return parking_session

async def update_parking_session(db: AsyncSession, plate_number: str, url: str):
    result = await db.execute(
        select(ParkingSession)
        .filter(
            ParkingSession.plate_number == plate_number, 
            ParkingSession.status == "active"
        )
        .order_by(ParkingSession.entry_time.desc())
    )
    parking_session = result.scalars().first()
    
    if not parking_session:
        raise HTTPException(status_code=404, detail="Active parking session not found")

    parking_session.exit_time = datetime.now()
    parking_session.status = "completed"
    parking_session.exit_image_url = url
    
    await db.commit()
    await db.refresh(parking_session)
    
    time_total = int((parking_session.exit_time - parking_session.entry_time).total_seconds() / 60)
    
    inv_result = await db.execute(select(Invoice).filter(Invoice.session_id == parking_session.id))
    invoice = inv_result.scalars().first()
    
    await checkout_invoice(db, InvoiceCheckout(id=invoice.id, time_total=time_total))
    mqtt_client.send_payment_start(str(parking_session.id), str(invoice.id), str(invoice.amount))
    return int(time_total)