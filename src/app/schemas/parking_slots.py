
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ParkingSlotResponse(BaseModel):
    id: UUID
    slot_code: str
    status: str
    position_x: int
    position_y: int
    created_at: datetime
    updated_at: datetime

class ParkingSlotCreate(BaseModel):
    slot_code: str
    status: str
    position_x: int
    position_y: int

class ParkingSlotUpdate(BaseModel):
    id: UUID
    slot_code: Optional[str]
    status: Optional[str]
    position_x: Optional[int]
    position_y: Optional[int]

class ParkingSlotStatusUpdate(BaseModel):
    id: UUID
    status: str