import hashlib
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.app.model.user import User
from src.app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from src.app.core.security import create_access_token, create_refresh_token, verify_refresh_token


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register(db: Session, payload: RegisterRequest) -> User:   

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")

    hashed_pw = _hash_password(payload.password)

    new_user = User(
        email=payload.email,
        password=hashed_pw,
        full_name=payload.full_name,
        phone=payload.phone,
        role_id=payload.role_id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def login(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    hashed_pw = _hash_password(payload.password)
    if user.password != hashed_pw:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    token_data = {"sub": str(user.id), "email": user.email, "role_id": user.role_id}

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

def change_password(db: Session, user_id: int, password: str, new_password: str) -> dict:
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
    
    token_data = {"sub": str(user.id), "email": user.email, "role_id": user.role_id}
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }