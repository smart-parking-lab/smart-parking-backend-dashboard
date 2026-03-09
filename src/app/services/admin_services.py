from sqlalchemy.orm import Session
from src.app.model import Role, User, VehicleType, Vehicle
from src.app.schemas.admin import RoleResponse, AdminUserResponse, VehicleTypeResponse, AdminVehicleResponse
from fastapi import HTTPException

def check_admin(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.role or user.role.name != "Admin":
        raise HTTPException(
            status_code=403, 
            detail="Quyền truy cập bị từ chối. Bạn không có quyền quản trị."
        )
    return user

def get_all_roles(db: Session,user_id:str) -> list[RoleResponse]:
    check_admin(db,user_id)
    return db.query(Role).all()

def get_all_users(db: Session,user_id:str) -> list[AdminUserResponse]:
    check_admin(db,user_id)
    users = db.query(User).all()
    return [
        AdminUserResponse(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            phone=u.phone,
            role_name=u.role.name if hasattr(u, 'role') and u.role else None,
            created_at=u.created_at,
            updated_at=u.updated_at
        ) for u in users
    ]

def get_all_vehicles(db: Session,user_id:str) -> list[AdminVehicleResponse]:
    check_admin(db,user_id)
    vehicles = db.query(Vehicle).all()
    return [
        AdminVehicleResponse(
            id=v.id,
            plate_number=v.plate_number,
            is_active=v.is_active,
            user_name=v.user.full_name if v.user else None,
            vehicle_type_name=v.vehicle_type.name if v.vehicle_type else None,
            created_at=v.created_at,
            updated_at=v.updated_at
        ) for v in vehicles
    ]
