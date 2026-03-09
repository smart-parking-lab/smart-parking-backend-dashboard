from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.app.utils.database import get_db
from src.app.services import admin_services
from src.app.schemas.admin import RoleResponse, AdminUserResponse, AdminVehicleResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/roles", response_model=list[RoleResponse], summary="Lấy danh sách tất cả các quyền")
def get_all_roles(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return admin_services.get_all_roles(db,user_id)

@router.get("/users", response_model=list[AdminUserResponse], summary="Lấy danh sách tất cả người dùng")
def get_all_users(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub") 
    return admin_services.get_all_users(db,user_id)

@router.get("/vehicles", response_model=list[AdminVehicleResponse], summary="Lấy danh sách tất cả các xe")
def get_all_vehicles(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")  
    return admin_services.get_all_vehicles(db,user_id)
