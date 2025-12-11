from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

@router.post("/", response_model=schemas.Device, status_code=status.HTTP_201_CREATED)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    # Check if device exists
    db_device = db.query(models.Device).filter(models.Device.serial_number == device.serial_number).first()
    if db_device:
        raise HTTPException(status_code=400, detail="Device already registered")
    
    # Create new device with defaults (EN_LIVRAISON, MAGASIN)
    new_device = models.Device(
        serial_number=device.serial_number,
        num_carton=device.num_carton,
        operateur=device.operateur,
        poste_pose=device.poste_pose,
        # Default status/affectation are set in Model
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/{serial_number}", response_model=schemas.Device)
def read_device(serial_number: str, db: Session = Depends(get_db)):
    # Retrieve device by serial number
    db_device = db.query(models.Device).filter(models.Device.serial_number == serial_number).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
