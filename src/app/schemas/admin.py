from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class VehicleTypeResponse(BaseModel):
    id: UUID
    name: str
    display_name: Optional[str]
    icon: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AdminUserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str]
    role_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AdminVehicleResponse(BaseModel):
    id: UUID
    plate_number: str
    is_active: bool
    user_name: Optional[str]
    vehicle_type_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
