from pydantic import BaseModel, Field,field_validator, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.app.validators.vehicle_validator import validate_plate_number


class VehicleCreate(BaseModel):
    plate_number: str = Field(..., description="Biển số xe")
    vehicle_type_name: str = Field(..., description="ID của loại xe (xe máy, ô tô, v.v)")

class VehicleResponse(BaseModel):
    vehicle_type_name: Optional[str]
    plate_number: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UpdateVehicleRequest(BaseModel):
    vehicle_id: str
    vehicle_type_name : str
    plate_number : str
    is_active : bool

    @field_validator("plate_number")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        return validate_plate_number(v)
