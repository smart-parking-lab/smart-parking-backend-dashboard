from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.app.model import Vehicle, VehicleType, User 
from src.app.schemas.vehicle import VehicleCreate, VehicleResponse,UpdateVehicleRequest
from src.app.schemas.admin import VehicleTypeResponse

def register_vehicle(db: Session, user_id: str, payload: VehicleCreate) -> VehicleResponse:
    vehicle_type = db.query(VehicleType).filter(VehicleType.name == payload.vehicle_type_name).first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Loại xe không tồn tại")

    existing_vehicle = db.query(Vehicle).filter(Vehicle.plate_number == payload.plate_number).first()
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Biển số xe đã được đăng ký")

    new_vehicle = Vehicle(
        user_id=user_id,
        vehicle_type_id=vehicle_type.id,
        plate_number=payload.plate_number,
        is_active=True
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return VehicleResponse(
        vehicle_type_name=vehicle_type.name,
        plate_number=new_vehicle.plate_number,
        is_active=new_vehicle.is_active,
        created_at=new_vehicle.created_at,
        updated_at=new_vehicle.updated_at
    )

def get_user_vehicles(db: Session, user_id: str) -> list[VehicleResponse]:
    vehicles = db.query(Vehicle).filter(Vehicle.user_id == user_id).all()
    return [
        VehicleResponse(
            vehicle_type_name=v.vehicle_type.name if v.vehicle_type else None,
            plate_number=v.plate_number,
            is_active=v.is_active,
            created_at=v.created_at,
            updated_at=v.updated_at
        ) for v in vehicles
    ]

def get_all_vehicle_types(db: Session) -> list[VehicleTypeResponse]:
    return db.query(VehicleType).all()

def update_vehicle(db: Session, user_id: str, payload: UpdateVehicleRequest) -> VehicleResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle không tồn tại")
    
    if user.role.name != "Admin" and user.id != vehicle.user_id :
        raise HTTPException(status_code=404, detail="Vehicle không phải của bạn")

    vehicle_type = db.query(VehicleType).filter(VehicleType.name == payload.vehicle_type_name).first()
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle_type không tồn tại")
    
    has_changes = False
    
    if vehicle_type.id != vehicle.vehicle_type_id :
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
    
    db.commit()
    db.refresh(vehicle)
    
    
    return VehicleResponse(
        vehicle_type_name= vehicle.vehicle_type.name,
        plate_number= vehicle.plate_number,
        is_active= vehicle.is_active,
        created_at= vehicle.created_at,
        updated_at= vehicle.updated_at
    )