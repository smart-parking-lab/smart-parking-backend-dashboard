from datetime import datetime   
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from uuid import UUID

from app.model.sensors import Sensor
from app.model.user import User
from app.model.parking_slots import ParkingSlot
from app.schemas.sensors import SensorCreate, SensorUpdate, SensorUpdateStatus, SensorResponse

async def create_sensor(db: AsyncSession, payload: SensorCreate, user_id: str):
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    if not payload.slot_id:
        raise HTTPException(status_code=400, detail="Slot ID is required")
        
    slot_result = await db.execute(select(ParkingSlot).filter(ParkingSlot.id == payload.slot_id))
    parking_slot = slot_result.scalars().first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
        
    sensor = Sensor(**payload.dict())
    db.add(sensor)
    await db.commit()
    await db.refresh(sensor)
    
    # Reload with slot relationship for response
    result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
        .filter(Sensor.id == sensor.id)
    )
    sensor = result.scalars().first()
    
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

async def get_all_sensors(db: AsyncSession, user_id: str) -> list[SensorResponse]:
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
        
    result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
    )
    sensors = result.scalars().all()
    return [SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    ) for sensor in sensors]

async def get_sensor_by_id(db: AsyncSession, sensor_id: UUID, user_id: str) -> SensorResponse:
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    
    result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
        .filter(Sensor.id == sensor_id)
    )
    sensor = result.scalars().first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
        
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

async def update_sensor(db: AsyncSession, payload: SensorUpdate, user_id: str):
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
        
    sensor_result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
        .filter(Sensor.id == payload.id)
    )
    sensor = sensor_result.scalars().first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
        
    slot_result = await db.execute(select(ParkingSlot).filter(ParkingSlot.id == payload.slot_id))
    parking_slot = slot_result.scalars().first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
        
    sensor.sensor_code = payload.sensor_code
    sensor.slot_id = payload.slot_id
    sensor.status = payload.status
    sensor.last_heartbeat = datetime.utcnow()
    
    await db.commit()
    await db.refresh(sensor)
    
    # Reload for response
    result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
        .filter(Sensor.id == sensor.id)
    )
    sensor = result.scalars().first()
    
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

async def update_status_sensor(db: AsyncSession, payload: SensorUpdateStatus, user_id: str):
    user_result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
        
    sensor_result = await db.execute(
        select(Sensor)
        .options(selectinload(Sensor.slot))
        .filter(Sensor.id == payload.id)
    )
    sensor = sensor_result.scalars().first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
        
    sensor.status = payload.status
    sensor.last_heartbeat = datetime.utcnow()
    sensor.slot.status = "broken"
    
    await db.commit()
    await db.refresh(sensor)
    
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

