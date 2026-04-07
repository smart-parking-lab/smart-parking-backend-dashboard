from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vehicle import VehicleCreate, VehicleResponse, UpdateVehicleRequest
from app.services import vehicle_services
from app.utils.database import get_db
from app.validators import vehicle_validator
from app.schemas.admin import VehicleTypeResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("", response_model=VehicleResponse, status_code=201)
async def register_vehicle(request: Request, payload: VehicleCreate, db: AsyncSession = Depends(get_db)):
    vehicle_validator.http_validate_vehicle(payload.plate_number, payload.vehicle_type_name)
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    vehicle = await vehicle_services.register_vehicle(db, user_id=user_id, payload=payload)
    return vehicle

@router.get("", response_model=list[VehicleResponse])
async def get_my_vehicles(request: Request, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    vehicles = await vehicle_services.get_user_vehicles(db, user_id=user_id)
    return vehicles

@router.get("/vehicle-types", response_model=list[VehicleTypeResponse], summary="Lấy danh sách tất cả loại xe")
async def get_all_vehicle_types(db: AsyncSession = Depends(get_db)):
    return await vehicle_services.get_all_vehicle_types(db)

@router.put("/update", response_model=VehicleResponse)
async def update_vehicle(request: Request, payload: UpdateVehicleRequest, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return await vehicle_services.update_vehicle(db, user_id, payload)