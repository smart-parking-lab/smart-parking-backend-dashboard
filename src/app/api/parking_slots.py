from fastapi import APIRouter, Depends, Request
from app.schemas.parking_slots import (
    ParkingSlotCreate,
    ParkingSlotResponse,
    ParkingSlotUpdate,
    ParkingSlotStatusUpdate,
    ParkingSlotWithSensorResponse
)
from app.services import parking_slots
from sqlalchemy.orm import Session
from app.utils.database import get_db

router = APIRouter(prefix="/parking-slots", tags=["Parking Slots"])

@router.post("/", response_model=ParkingSlotResponse)
def create_parking_slot(request: Request, payload: ParkingSlotCreate, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return parking_slots.create_new_parking_slot(db, payload, user_id)

@router.get("/", response_model=list[ParkingSlotResponse])
def get_all_parking_slots(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return parking_slots.get_parking_slots(db, user_id)

@router.put("/", response_model=ParkingSlotResponse)
def update_parking_slot(request: Request, payload: ParkingSlotUpdate, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return parking_slots.update_parking_slot(db, payload, user_id)


@router.put("/status", response_model=ParkingSlotResponse)
def update_parking_slot_status(request: Request, payload: ParkingSlotStatusUpdate, db: Session = Depends(get_db)):
    return parking_slots.update_parking_slot_status(db, payload)

@router.get("/with-sensors", response_model=list[ParkingSlotWithSensorResponse])
def get_parking_slots_with_sensors(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return parking_slots.get_parking_slots_with_active_sensors(db, user_id)
