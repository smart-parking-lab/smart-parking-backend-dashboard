from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.parking_sessions import ParkingSessionResponse
from app.services import parking_sessions_services
from app.utils.database import get_db
from uuid import UUID
from fastapi import Path
from app.validators import vehicle_validator
router = APIRouter(prefix="/parking-sessions", tags=["Parking Sessions"])

@router.post("", response_model=ParkingSessionResponse, status_code=201)
async def create_parking_session(
    plate_number: str = Form(...),
#    entry_image: UploadFile = File(...),
    url: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
#    vehicle_validator.validate_vehicle(plate_number)
    return await parking_sessions_services.create_parking_session(
        db, plate_number, url
    )

@router.get("", response_model=list[ParkingSessionResponse])
async def get_all_parking_sessions(db: AsyncSession = Depends(get_db)):
    return await parking_sessions_services.get_all_parking_sessions(db)

@router.get("/{id}", response_model=ParkingSessionResponse)
async def get_parking_session_by_id(db: AsyncSession = Depends(get_db), id: UUID = Path(...)):
    return await parking_sessions_services.get_parking_session_by_id(db, id)

@router.put("", response_model=int)
async def update_parking_session(
    plate_number: str = Form(...),
#    exit_image: UploadFile = File(...),
    url: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
#    vehicle_validator.validate_vehicle(plate_number)
    return await parking_sessions_services.update_parking_session(db, plate_number, url)
