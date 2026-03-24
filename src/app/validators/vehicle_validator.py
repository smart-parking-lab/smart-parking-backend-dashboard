import re
from fastapi import HTTPException

PLATE_NUMBER_REGEX = re.compile(r"^[0-9]{2}[A-Z]{1,2}[0-9]{5}$")

def validate_plate_number(plate_number: str) -> str:
    plate_number = plate_number.strip().upper()
    if not plate_number:
        raise ValueError("Biển số xe không được để trống")
    if not PLATE_NUMBER_REGEX.match(plate_number):
        raise ValueError("Biển số xe không hợp lệ (Ví dụ: 29A-123.45, 51-F1 1234)")
    if len(plate_number) < 5 or len(plate_number) > 15:
        raise ValueError("Biển số xe phải có từ 5 đến 15 ký tự")
    return plate_number

def validate_vehicle_type_name(vehicle_type_name: str) -> str:
    name = vehicle_type_name.strip()
    if not name:
        raise ValueError("Loại xe không được để trống")
    return name

def http_validate_vehicle(plate_number: str, vehicle_type_name: str):
    errors = []
    
    try:
        validate_plate_number(plate_number)
    except ValueError as e:
        errors.append(str(e))
        
    try:
        validate_vehicle_type_name(vehicle_type_name)
    except ValueError as e:
        errors.append(str(e))
        
    if errors:
        raise HTTPException(status_code=422, detail=errors)
