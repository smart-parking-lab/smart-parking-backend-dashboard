from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ParkingSessionCreate(BaseModel):
    plate_number: str

class ParkingSessionResponse(BaseModel):
    id: UUID
    plate_number: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    status: str
    entry_image_url: str
    exit_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ParkingSessionUpdate(BaseModel):
    plate_number: str
