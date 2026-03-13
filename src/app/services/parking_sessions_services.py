import uuid
from fastapi import UploadFile
from app.utils.supabase_client import supabase
from sqlalchemy.orm import Session
from app.model import Vehicle,ParkingSession
from fastapi import HTTPException
from datetime import datetime

async def upload_image(image: UploadFile):
    file_name = f"{uuid.uuid4()}_{image.filename}"

    file_content = await  image.read()
    image.seek(0) 
    
    supabase.storage.from_("vehicle-images").upload(
        file_name,
        file_content,
        file_options={"content-type": image.content_type}
    )

    url = supabase.storage.from_("vehicle-images").get_public_url(file_name)
    return url

async def create_parking_session(db: Session, plate_number: str, entry_image: UploadFile):
    vehicle = db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    url = await upload_image(entry_image)
    parking_session = ParkingSession(
        vehicle_id=vehicle.id,
        entry_time=datetime.now(),
        status="active",
        entry_image_url=url,
    )
    db.add(parking_session)
    db.commit()
    db.refresh(parking_session)
    return parking_session

def get_all_parking_sessions(db: Session):
    return db.query(ParkingSession).all()

def get_parking_session_by_id(db: Session, session_id: uuid.UUID):
    parking_session = db.query(ParkingSession).filter(ParkingSession.id == session_id).first()
    if not parking_session:
        raise HTTPException(status_code=404, detail="Parking session not found")
    return parking_session

async def update_parking_session(db: Session, plate_number: str, exit_image: UploadFile):
    vehicle = db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    parking_session = db.query(ParkingSession).filter(
        ParkingSession.vehicle_id == vehicle.id, 
        ParkingSession.status == "active"
    ).order_by(ParkingSession.entry_time.desc()).first()
    
    if not parking_session:
        raise HTTPException(status_code=404, detail="Active parking session not found")

    url = await upload_image(exit_image)
    parking_session.exit_time = datetime.now()
    parking_session.status = "completed"
    parking_session.exit_image_url = url
    
    db.commit()
    db.refresh(parking_session)
    
    time_total = (parking_session.exit_time - parking_session.entry_time).total_seconds() / 60
    return int(time_total) 