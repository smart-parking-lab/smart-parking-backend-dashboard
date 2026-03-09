from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse, ChangePasswordRequest, RefreshTokenRequest, UPdatedProfileRequest
from src.app.services import auth_services
from src.app.utils.database import get_db
from src.app.validators.auth_validator import http_validate_register, http_validate_login, http_validate_change_password
from src.app.model.user import User
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    http_validate_register(payload.email, payload.password, payload.full_name, payload.phone)
    user = auth_services.register(db, payload)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    http_validate_login(payload.email, payload.password)
    return auth_services.login(db, payload)


@router.get("/me", response_model=UserResponse)
def get_me(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return auth_services.get_me(db, user_id)

@router.post("/change-password")
def change_password(request: Request, payload: ChangePasswordRequest, db: Session = Depends(get_db)):
    http_validate_change_password(payload.new_password, payload.check_password)
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return auth_services.change_password(db, user_id, payload.password, payload.new_password)


@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_services.refresh_access_token(db, payload.refresh_token)


@router.put("/update-profile", response_model=UserResponse)
def update_profile(request: Request, payload: UPdatedProfileRequest, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return auth_services.update_profile(db, user_id, payload)