from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.model import Vehicle, VehicleType, User 
from app.schemas.vehicle import VehicleCreate, VehicleResponse, UpdateVehicleRequest
from app.schemas.admin import VehicleTypeResponse

async def register_vehicle(db: AsyncSession, user_id: str, payload: VehicleCreate) -> VehicleResponse:
    result = await db.execute(select(VehicleType).filter(VehicleType.name == payload.vehicle_type_name))
    vehicle_type = result.scalars().first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Loại xe không tồn tại")

    existing_result = await db.execute(select(Vehicle).filter(Vehicle.plate_number == payload.plate_number))
    existing_vehicle = existing_result.scalars().first()
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Biển số xe đã được đăng ký")

    new_vehicle = Vehicle(
        user_id=user_id,
        vehicle_type_id=vehicle_type.id,
        plate_number=payload.plate_number,
        is_active=True
    )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    return VehicleResponse(
        vehicle_type_name=vehicle_type.name,
        plate_number=new_vehicle.plate_number,
        is_active=new_vehicle.is_active,
        created_at=new_vehicle.created_at,
        updated_at=new_vehicle.updated_at
    )

async def get_user_vehicles(db: AsyncSession, user_id: str) -> list[VehicleResponse]:
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .filter(Vehicle.user_id == user_id)
    )
    vehicles = result.scalars().all()
    return [
        VehicleResponse(
            vehicle_type_name=v.vehicle_type.name if v.vehicle_type else None,
            plate_number=v.plate_number,
            is_active=v.is_active,
            created_at=v.created_at,
            updated_at=v.updated_at
        ) for v in vehicles
    ]

async def get_all_vehicle_types(db: AsyncSession) -> list[VehicleTypeResponse]:
    result = await db.execute(select(VehicleType))
    return result.scalars().all()

async def update_vehicle(db: AsyncSession, user_id: str, payload: UpdateVehicleRequest) -> VehicleResponse:
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    vehicle_result = await db.execute(select(Vehicle).options(selectinload(Vehicle.vehicle_type)).filter(Vehicle.id == payload.vehicle_id))
    vehicle = vehicle_result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle không tồn tại")
    
    if user.role.name != "Admin" and user.id != vehicle.user_id:
        raise HTTPException(status_code=404, detail="Vehicle không phải của bạn")

    vt_result = await db.execute(select(VehicleType).filter(VehicleType.name == payload.vehicle_type_name))
    vehicle_type = vt_result.scalars().first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle_type không tồn tại")
    
    has_changes = False
    
    if vehicle_type.id != vehicle.vehicle_type_id:
        vehicle.vehicle_type_id = vehicle_type.id
        has_changes = True
        
    if payload.plate_number != vehicle.plate_number:
        vehicle.plate_number = payload.plate_number
        has_changes = True
        
    if payload.is_active != vehicle.is_active:
        vehicle.is_active = payload.is_active
        has_changes = True
        
    if not has_changes:
        raise HTTPException(status_code=400, detail="Không có thông tin nào mới để cập nhật")
    
    await db.commit()
    await db.refresh(vehicle)
    
    return VehicleResponse(
        vehicle_type_name=vehicle.vehicle_type.name,
        plate_number=vehicle.plate_number,
        is_active=vehicle.is_active,
        created_at=vehicle.created_at,
        updated_at=vehicle.updated_at
    )