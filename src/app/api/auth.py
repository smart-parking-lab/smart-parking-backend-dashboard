from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse, ChangePasswordRequest, RefreshTokenRequest, UPdatedProfileRequest
from app.services import auth_services
from app.utils.database import get_db
from app.validators.auth_validator import http_validate_register, http_validate_login, http_validate_change_password
from app.model.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    http_validate_register(payload.email, payload.password, payload.full_name, payload.phone)
    user = await auth_services.register(db, payload)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    http_validate_login(payload.email, payload.password)
    return await auth_services.login(db, payload)


@router.get("/me", response_model=UserResponse)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return await auth_services.get_me(db, user_id)


@router.post("/change-password")
async def change_password(request: Request, payload: ChangePasswordRequest, db: AsyncSession = Depends(get_db)):
    http_validate_change_password(payload.new_password, payload.check_password)
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    # Redundant but kept for consistency with original code for now, converted to async select
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return await auth_services.change_password(db, user_id, payload.password, payload.new_password)


@router.post("/refresh")
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    return await auth_services.refresh_access_token(db, payload.refresh_token)


@router.put("/update-profile", response_model=UserResponse)
async def update_profile(request: Request, payload: UPdatedProfileRequest, db: AsyncSession = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return await auth_services.update_profile(db, user_id, payload)