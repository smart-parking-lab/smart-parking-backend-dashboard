import hashlib
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.app.model import User,Role
from src.app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse, UPdatedProfileRequest
from src.app.core.security import create_access_token, create_refresh_token, verify_refresh_token


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register(db: Session, payload: RegisterRequest) -> UserResponse:   

    existing = db.query(User).filter(User.email == payload.email).first()
    role = db.query(Role).filter(Role.name == payload.role_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    if not role:
        raise HTTPException(status_code=404, detail="Role không tồn tại")
    hashed_pw = _hash_password(payload.password)

    new_user = User(
        email=payload.email,
        password=hashed_pw,
        full_name=payload.full_name,
        phone=payload.phone,
        role_id=role.id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        email=new_user.email,
        full_name=new_user.full_name,
        phone=new_user.phone,
        role_name=role.name
    )



def login(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    hashed_pw = _hash_password(payload.password)
    if user.password != hashed_pw:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    token_data = {"sub": str(user.id), "email": user.email, "role_id": str(user.role_id) if user.role_id else None}

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

def get_me(db: Session, user_id: str) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
        
    role = db.query(Role).filter(Role.id == user.role_id).first()
    role_name = role.name if role else None
    
    return UserResponse(
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role_name=role_name
    )
    
def change_password(db: Session, user_id: str, password: str, new_password: str) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    if user.password != _hash_password(password):
        raise HTTPException(status_code=401, detail="Mật khẩu cũ không đúng")
    user.password = _hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Đổi mật khẩu thành công"}


def refresh_access_token(db: Session, refresh_token: str) -> dict:
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token không hợp lệ hoặc đã hết hạn")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    token_data = {"sub": str(user.id), "email": user.email, "role_id": str(user.role_id) if user.role_id else None}
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def update_profile(db: Session, user_id: str, payload: UPdatedProfileRequest) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")

    has_changes = False
    
    if payload.email != user.email:
        existing_email = db.query(User).filter(User.email == payload.email, User.id != user_id).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
        user.email = payload.email
        has_changes = True
        
    if payload.full_name != user.full_name:
        user.full_name = payload.full_name
        has_changes = True
        
    if payload.phone != user.phone:
        user.phone = payload.phone
        has_changes = True
        
    if not has_changes:
        raise HTTPException(status_code=400, detail="Không có thông tin nào mới để cập nhật")
        
    db.commit()
    db.refresh(user)
    
    role = db.query(Role).filter(Role.id == user.role_id).first()
    
    return UserResponse(
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role_name=role.name if role else None
    )