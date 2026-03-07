from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional

from src.app.validators.auth_validator import (
    validate_password_register,
    validate_password_login,
    validate_full_name,
    validate_phone,
    validate_email_login,
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str]
    role_id: Optional[int] = 1

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return validate_password_register(v)

    @field_validator("full_name")
    @classmethod
    def full_name_valid(cls, v: str) -> str:
        return validate_full_name(v)

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        return validate_phone(v)


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_or_phone_valid(cls, v: str) -> str:
        return validate_email_login(v)

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        return validate_password_login(v)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    role_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str
    check_password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return validate_password_register(v)

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, v: str) -> str:
        return validate_password_register(v)    


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    