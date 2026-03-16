from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class SensorBase(BaseModel):
    sensor_code: str
    slot_id: Optional[UUID] = None
    status: str = "offline"
    

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    id: UUID
    pass

class SensorResponse(BaseModel):
    id: UUID
    created_at: datetime
    last_heartbeat: datetime
    sensor_code: str
    slot_name: str
    status: str

class SensorUpdateStatus(BaseModel):
    id: UUID    
    status: str