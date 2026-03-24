from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.parking_sessions import ParkingSessionResponse
from app.services import parking_sessions_services
from app.utils.database import get_db
from uuid import UUID
from fastapi import Path
from app.validators import vehicle_validator
from app.schemas.invoices import InvoiceResponse
router = APIRouter(prefix="/parking-sessions", tags=["Parking Sessions"])

@router.post("", response_model=ParkingSessionResponse, status_code=201)
async def create_parking_session(
    plate_number: str = Form(...),
    entry_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    vehicle_validator.validate_plate_number(plate_number)
    return await parking_sessions_services.create_parking_session(
        db, plate_number, entry_image
    )

@router.get("", response_model=list[ParkingSessionResponse])
def get_all_parking_sessions(db: Session = Depends(get_db)):
    return parking_sessions_services.get_all_parking_sessions(db)

@router.get("/{id}", response_model=ParkingSessionResponse)
def get_parking_session_by_id(db: Session = Depends(get_db), id: UUID = Path(...)):
    return parking_sessions_services.get_parking_session_by_id(db, id)



@router.get("/check/{plate_number}", response_model=ParkingSessionResponse)
def is_vehicle_parked(db: Session = Depends(get_db), plate_number: str = Path(...)):
    vehicle_validator.validate_plate_number(plate_number)
    return parking_sessions_services.check_car_in_parking(db, plate_number)

@router.put("", response_model=InvoiceResponse)
async def update_parking_session(
    plate_number: str = Form(...),
    exit_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    vehicle_validator.validate_plate_number(plate_number)
    return await parking_sessions_services.update_parking_session(db, plate_number, exit_image)