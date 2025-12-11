from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List, Optional

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

@router.get("/dictionaries")
def get_dictionaries():
    """
    Returns valid values for Enums to populate Frontend Dropdowns.
    """
    return {
        "status": [e.value for e in models.DeviceStatus],
        "affectation": [e.value for e in models.TypeAffectation],
        "action_type": [e.value for e in models.ActionType]
    }

@router.get("/search", response_model=List[schemas.Device])
def search_devices(
    q: Optional[str] = None, # General search (serial, carton)
    status: Optional[models.DeviceStatus] = None,
    affectation: Optional[models.TypeAffectation] = None,
    num_carton: Optional[str] = None,
    operateur: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Device)
    
    if q:
        # Simple fuzzy search
        query = query.filter(
            (models.Device.serial_number.ilike(f"%{q}%")) | 
            (models.Device.num_carton.ilike(f"%{q}%")) |
            (models.Device.poste_pose.ilike(f"%{q}%"))
        )
    
    if status:
        query = query.filter(models.Device.current_status == status)
    
    if affectation:
        query = query.filter(models.Device.affectation == affectation)
        
    if num_carton:
        query = query.filter(models.Device.num_carton == num_carton)
        
    if operateur:
        query = query.filter(models.Device.operateur == operateur)
        
    return query.limit(100).all()

@router.post("/", response_model=schemas.Device, status_code=status.HTTP_201_CREATED)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    # Check if device exists
    db_device = db.query(models.Device).filter(models.Device.serial_number == device.serial_number).first()
    if db_device:
        raise HTTPException(status_code=400, detail="Device already registered")
    
    # Create new device with defaults (EN_LIVRAISON, MAGASIN)
    # Check Carton Capacity (Max 4)
    if device.num_carton:
        count_in_carton = db.query(models.Device).filter(models.Device.num_carton == device.num_carton).count()
        if count_in_carton >= 4:
            raise HTTPException(
                status_code=400, 
                detail=f"Carton {device.num_carton} is full (Max 4 devices)."
            )

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
