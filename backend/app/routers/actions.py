from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/actions",
    tags=["actions"],
)

@router.post("/", response_model=schemas.History, status_code=status.HTTP_201_CREATED)
def perform_action(action: schemas.ActionCreate, db: Session = Depends(get_db)):
    # 1. Find the device
    db_device = db.query(models.Device).filter(models.Device.serial_number == action.serial_number).first()
    if not db_device:
        # Option: Auto-create if not found (Reception)? For now, strict: must exist.
        raise HTTPException(status_code=404, detail="Device not found")

    # 2. Update Device Status & Location based on Action Type
    if action.action_type == models.ActionType.POSE:
        db_device.current_status = models.DeviceStatus.EN_SERVICE
        if action.location:
            db_device.current_location = action.location
            
    elif action.action_type == models.ActionType.DEPOSE:
        db_device.current_status = models.DeviceStatus.STOCK
        if action.location:
             # Usually "Depose" means it goes back to stock, location might be the Warehouse or the Tech's truck.
            db_device.current_location = action.location
            
    elif action.action_type == models.ActionType.TRANSFERT:
        db_device.current_status = models.DeviceStatus.EN_TRANSIT
        if action.location:
            db_device.current_location = action.location
            
    elif action.action_type == models.ActionType.RECEPTION:
        db_device.current_status = models.DeviceStatus.STOCK
        if action.location:
            db_device.current_location = action.location
            
    # Generic update for other fields
    db_device.last_updated = datetime.now()

    # 3. Create History Record
    new_history = models.History(
        device_id=db_device.id,
        action_type=action.action_type,
        timestamp=datetime.now(),
        user_id=action.user_id,
        location=action.location
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    
    return new_history
