
from datetime import datetime   
from app.model.sensors import Sensor
from app.model.user import User
from app.schemas.sensors import SensorCreate, SensorUpdate, SensorUpdateStatus, SensorResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model.parking_slots import ParkingSlot
from uuid import UUID

def create_sensor(db: Session, payload: SensorCreate, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    if not payload.slot_id:
        raise HTTPException(status_code=400, detail="Slot ID is required")
    parking_slot = db.query(ParkingSlot).filter(ParkingSlot.id == payload.slot_id).first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    sensor = Sensor(**payload.dict())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

def get_all_sensors(db: Session, user_id: str)-> list[SensorResponse]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    sensors = db.query(Sensor).all()
    return [SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    ) for sensor in sensors]

def get_sensor_by_id(db: Session, sensor_id: UUID, user_id: str)-> SensorResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
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

def update_sensor(db: Session, payload: SensorUpdate, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    sensor = db.query(Sensor).filter(Sensor.id == payload.id).first()
    parking_slot = db.query(ParkingSlot).filter(ParkingSlot.id == payload.slot_id).first()
    if not parking_slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    sensor.sensor_code = payload.sensor_code
    sensor.slot_id = payload.slot_id
    sensor.status = payload.status
    sensor.last_heartbeat = datetime.utcnow()
    db.commit()
    db.refresh(sensor)
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

def update_status_sensor(db: Session, payload: SensorUpdateStatus, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="User not authorized")
    sensor = db.query(Sensor).filter(Sensor.id == payload.id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    sensor.status = payload.status
    sensor.last_heartbeat = datetime.utcnow()
    db.commit()
    db.refresh(sensor)
    return SensorResponse(
        id=sensor.id,
        sensor_code=sensor.sensor_code,
        slot_name=sensor.slot.slot_code,
        status=sensor.status,
        last_heartbeat=sensor.last_heartbeat,
        created_at=sensor.created_at,
    )

