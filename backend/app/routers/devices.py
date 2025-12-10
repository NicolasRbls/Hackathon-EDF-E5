from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..database import get_db

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=schemas.Device, status_code=status.HTTP_201_CREATED)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.serial_number == device.serial_number).first()
    if db_device:
        raise HTTPException(status_code=400, detail="Device with this serial number already exists")
    
    new_device = models.Device(
        serial_number=device.serial_number,
        current_location=device.current_location,
        # Default status is STOCK from model definition
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/{serial_number}", response_model=schemas.Device)
def read_device(serial_number: str, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.serial_number == serial_number).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
