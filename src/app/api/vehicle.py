from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.app.schemas.vehicle import VehicleCreate, VehicleResponse, UpdateVehicleRequest
from src.app.services import vehicle_services
from src.app.utils.database import get_db
from src.app.validators import vehicle_validator
from src.app.schemas.admin import VehicleTypeResponse
router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("", response_model=VehicleResponse, status_code=201)
def register_vehicle(request: Request, payload: VehicleCreate, db: Session = Depends(get_db)):
    vehicle_validator.http_validate_vehicle(payload.plate_number, payload.vehicle_type_name)
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    vehicle = vehicle_services.register_vehicle(db, user_id=user_id, payload=payload)
    return vehicle

@router.get("", response_model=list[VehicleResponse])
def get_my_vehicles(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    vehicles = vehicle_services.get_user_vehicles(db, user_id=user_id)
    return vehicles

@router.get("/vehicle-types", response_model=list[VehicleTypeResponse], summary="Lấy danh sách tất cả loại xe")
def get_all_vehicle_types(db: Session = Depends(get_db)):
    return vehicle_services.get_all_vehicle_types(db)

@router.put("/update", response_model=VehicleResponse)
def update_vehicle(request: Request, payload: UpdateVehicleRequest, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return vehicle_services.update_vehicle(db, user_id, payload)