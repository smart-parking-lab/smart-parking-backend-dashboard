from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.services import admin_services
from app.schemas.admin import RoleResponse, AdminUserResponse, AdminVehicleResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/roles", response_model=list[RoleResponse], summary="Lấy danh sách tất cả các quyền")
async def get_all_roles(request: Request, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return await admin_services.get_all_roles(db, user_id)

@router.get("/users", response_model=list[AdminUserResponse], summary="Lấy danh sách tất cả người dùng")
async def get_all_users(request: Request, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub") 
    return await admin_services.get_all_users(db, user_id)

@router.get("/vehicles", response_model=list[AdminVehicleResponse], summary="Lấy danh sách tất cả các xe")
async def get_all_vehicles(request: Request, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")  
    return await admin_services.get_all_vehicles(db, user_id)
