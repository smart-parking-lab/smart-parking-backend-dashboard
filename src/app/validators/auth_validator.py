import re
from fastapi import HTTPException


PASSWORD_MIN_LEN = 8
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_\-]{8,}$"
)
PHONE_REGEX = re.compile(r"^\+?[0-9]{9,15}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
FULL_NAME_MIN_LEN = 2
FULL_NAME_MAX_LEN = 100


def validate_email(email: str) -> str:
    email = email.strip()
    if not email:
        raise ValueError("Email không được để trống")
    if not EMAIL_REGEX.match(email):
        raise ValueError("Email không hợp lệ")
    return email 

def validate_email_login(email: str) -> str:
    email = email.strip()
    if not email:
        raise ValueError("Email không được để trống")
    if not EMAIL_REGEX.match(email) and not PHONE_REGEX.match(email):
        raise ValueError("Email hoặc số điện thoại không hợp lệ")
    return email

def validate_password_register(password: str) -> str:
    password = password.strip()
    if not password:
        raise ValueError("Mật khẩu không được để trống")
    if len(password) < PASSWORD_MIN_LEN:
        raise ValueError(f"Mật khẩu phải có ít nhất {PASSWORD_MIN_LEN} ký tự")
    if not PASSWORD_REGEX.match(password):
        raise ValueError(
            "Mật khẩu phải có ít nhất 1 chữ hoa, 1 chữ thường, 1 số "
            "và 1 ký tự đặc biệt (@$!%*?&_-)"
        )
    return password

def validate_password_login(password: str) -> str:
    password = password.strip()
    if not password:
        raise ValueError("Mật khẩu không được để trống")
    return password

def validate_password_change(new_password: str, check_password: str) -> str:
    new_password = new_password.strip()
    check_password = check_password.strip()
    if not new_password or not check_password:
        raise ValueError("Mật khẩu không được để trống")
    if new_password != check_password:
        raise ValueError("Mật khẩu không khớp")
    return new_password

def validate_full_name(full_name: str) -> str:
    name = full_name.strip()
    if not name:
        raise ValueError("Họ tên không được để trống")
    if len(name) < FULL_NAME_MIN_LEN:
        raise ValueError(f"Họ tên phải có ít nhất {FULL_NAME_MIN_LEN} ký tự")
    if len(name) > FULL_NAME_MAX_LEN:
        raise ValueError(f"Họ tên không được vượt quá {FULL_NAME_MAX_LEN} ký tự")
    return name


def validate_phone(phone: str | None) -> str | None:
    if phone is None:
        return None
    phone = phone.strip()
    if not PHONE_REGEX.match(phone):
        raise ValueError("Số điện thoại không hợp lệ (9–15 số, có thể bắt đầu bằng '+')")
    return phone



def http_validate_register(email: str, password: str, full_name: str, phone: str | None = None):
    errors = []

    try:
        validate_email(email)
    except ValueError as e:
        errors.append(str(e))

    try:
        validate_password_register(password)
    except ValueError as e:
        errors.append(str(e))

    try:
        validate_full_name(full_name)
    except ValueError as e:
        errors.append(str(e))

    try:
        validate_phone(phone)
    except ValueError as e:
        errors.append(str(e))

    if errors:
        raise HTTPException(status_code=422, detail=errors)

def http_validate_login(email: str, password: str):
    errors = []

    try:
        validate_email_login(email)
    except ValueError as e:
        errors.append(str(e))

    try:
        validate_password_login(password)
    except ValueError as e:
        errors.append(str(e))

    if errors:
        raise HTTPException(status_code=422, detail=errors)

def http_validate_change_password(new_password: str, check_password: str):
    errors = []

    try:
        validate_password_change(new_password, check_password)
    except ValueError as e:
        errors.append(str(e))

    if errors:
        raise HTTPException(status_code=422, detail=errors)