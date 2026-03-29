from sqlalchemy.orm import Session
from app.model import ParkingSlot,User, Sensor
from app.schemas.parking_slots import (
    ParkingSlotCreate,
    ParkingSlotResponse,
    ParkingSlotUpdate,
    ParkingSlotStatusUpdate,
    ParkingSlotWithSensorResponse
)
from fastapi import HTTPException
from datetime import datetime
from uuid import UUID


def create_new_parking_slot(db: Session, payload: ParkingSlotCreate,user_id: UUID) -> ParkingSlotResponse:
    user_id = db.query(User).filter(User.id == user_id).first()
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User is not admin")

    parking_slot = ParkingSlot(**payload.dict())
    db.add(parking_slot)
    db.commit()
    db.refresh(parking_slot)
    return parking_slot

def get_parking_slots(db: Session, user_id: UUID) -> list[ParkingSlotResponse]:
    user_id = db.query(User).filter(User.id == user_id).first()
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User is not admin")
    
    parking_slots = db.query(ParkingSlot).all()
    return parking_slots

def update_parking_slot(db: Session, payload: ParkingSlotUpdate,user_id: UUID) -> ParkingSlotResponse:
    user_id = db.query(User).filter(User.id == user_id).first()
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User is not admin")
    parking_slot = db.query(ParkingSlot).filter(ParkingSlot.id == payload.id).first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    parking_slot.slot_code = payload.slot_code
    parking_slot.status = payload.status
    parking_slot.position_x = payload.position_x
    parking_slot.position_y = payload.position_y
    db.commit()
    db.refresh(parking_slot)
    return parking_slot

def update_parking_slot_status(db: Session, payload: ParkingSlotStatusUpdate) -> ParkingSlotResponse:
    parking_slot = db.query(ParkingSlot).filter(ParkingSlot.id == payload.id).first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    parking_slot.status = payload.status
    db.commit()
    db.refresh(parking_slot)
    return parking_slot

def get_parking_slots_with_active_sensors(db: Session, user_id: UUID) -> list[ParkingSlotWithSensorResponse]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User is not admin")

    parking_slots = db.query(ParkingSlot).join(Sensor).filter(Sensor.status != "đã thay thế").all()

    return parking_slots