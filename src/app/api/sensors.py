from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.services import sensors
from app.schemas.sensors import SensorCreate, SensorUpdate, SensorUpdateStatus
from app.utils.database import get_db
from uuid import UUID
router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("/")
def create_sensor(request: Request, payload: SensorCreate, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return sensors.create_sensor(db, payload, user_id)

@router.get("/")
def get_all_sensors(request: Request, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return sensors.get_all_sensors(db, user_id)

@router.get("/{sensor_id}")
def get_sensor_by_id(request: Request, sensor_id: UUID, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return sensors.get_sensor_by_id(db, sensor_id, user_id)

@router.put("/")
def update_sensor(request: Request, payload: SensorUpdate, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return sensors.update_sensor(db, payload, user_id)

@router.put("/status")
def update_status_sensor(request: Request, payload: SensorUpdateStatus, db: Session = Depends(get_db)):
    user_payload = request.state.user
    user_id = user_payload.get("sub")
    return sensors.update_status_sensor(db, payload, user_id)
