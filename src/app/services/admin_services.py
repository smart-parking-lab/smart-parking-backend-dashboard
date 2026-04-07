from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.model import Role, User, VehicleType, Vehicle
from app.schemas.admin import RoleResponse, AdminUserResponse, VehicleTypeResponse, AdminVehicleResponse
from fastapi import HTTPException

async def check_admin(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .filter(User.id == user_id)
    )
    user = result.scalars().first()
    if not user or not user.role or user.role.name != "Admin":
        raise HTTPException(
            status_code=403, 
            detail="Quyền truy cập bị từ chối. Bạn không có quyền quản trị."
        )
    return user

async def get_all_roles(db: AsyncSession, user_id: str) -> list[RoleResponse]:
    await check_admin(db, user_id)
    result = await db.execute(select(Role))
    return result.scalars().all()

async def get_all_users(db: AsyncSession, user_id: str) -> list[AdminUserResponse]:
    await check_admin(db, user_id)
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
    )
    users = result.scalars().all()
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

async def get_all_vehicles(db: AsyncSession, user_id: str) -> list[AdminVehicleResponse]:
    await check_admin(db, user_id)
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.user), selectinload(Vehicle.vehicle_type))
    )
    vehicles = result.scalars().all()
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
