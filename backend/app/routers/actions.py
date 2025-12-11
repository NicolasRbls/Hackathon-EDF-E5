from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime

router = APIRouter(
    prefix="/actions",
    tags=["actions"]
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime

router = APIRouter(
    prefix="/actions",
    tags=["actions"]
)

@router.post("/", response_model=schemas.History)
def create_action(action: schemas.ActionCreate, db: Session = Depends(get_db)):
    # 1. Verify device exists
    device = db.query(models.Device).filter(models.Device.serial_number == action.device_serial).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # 2. BUSINESS LOGIC & STATE MACHINE
    # We ignore 'new_status'/'new_affectation' from input (unless generic) and enforce rules
    
    current_status = device.current_status
    current_aff = device.affectation

    # --- PROFIL MAGASIN ---
    if action.action_type == models.ActionType.RECEPTION:
        # Livraison -> Stock Magasin
        if current_status != models.DeviceStatus.EN_LIVRAISON:
             # Permissive constraint: allow re-scan but warn? For now strict.
             pass 
        device.current_status = models.DeviceStatus.EN_STOCK
        device.affectation = models.TypeAffectation.MAGASIN
    
    # --- TRANSFERT (Magasin -> BO) ---
    elif action.action_type == models.ActionType.TRANSFERT:
        # Move stock to another location
        if not action.new_affectation:
            raise HTTPException(status_code=400, detail="Target affectation required for Transfert")
        device.affectation = action.new_affectation
        # Status remains EN_STOCK usually, or we could add EN_TRANSIT. 
        # The rules say: "commande des cartons... les K affectés à la BO".
        device.current_status = models.DeviceStatus.EN_STOCK

    # --- PROFIL BO (Pose / Dépose) ---
    elif action.action_type == models.ActionType.POSE:
        if current_status != models.DeviceStatus.EN_STOCK:
             raise HTTPException(status_code=400, detail="Device must be in STOCK to be installed")
        
        if not action.poste_pose:
             raise HTTPException(status_code=400, detail="Poste ID required for POSE")
             
        device.current_status = models.DeviceStatus.POSE
        device.poste_pose = action.poste_pose
        # Affectation remains the BO

    elif action.action_type == models.ActionType.DEPOSE:
        if current_status != models.DeviceStatus.POSE:
            raise HTTPException(status_code=400, detail="Device is not currently installed (POSE)")
            
        # Dépose -> A Tester (Labo)
        device.current_status = models.DeviceStatus.A_TESTER
        device.affectation = models.TypeAffectation.LABO
        device.poste_pose = None # Remove link to post

    # --- PROFIL LABO ---
    elif action.action_type == models.ActionType.TEST:
        if current_status != models.DeviceStatus.A_TESTER:
             raise HTTPException(status_code=400, detail="Device must be in A_TESTER state")
        
        # We use strict 'new_status' passed by Labo to determine result (EN_STOCK=OK, HS=KO)
        if action.new_status == models.DeviceStatus.EN_STOCK:
            # Test OK -> Retour Magasin
            device.current_status = models.DeviceStatus.EN_STOCK
            device.affectation = models.TypeAffectation.MAGASIN
        elif action.new_status == models.DeviceStatus.HS:
            # Test KO -> HS
            device.current_status = models.DeviceStatus.HS
            device.affectation = models.TypeAffectation.AUCUNE
        else:
            raise HTTPException(status_code=400, detail="Invalid Test Result Status")

    # --- GENERIC / ADMIN ---
    elif action.action_type == models.ActionType.AUTRE:
        if action.new_status: device.current_status = action.new_status
        if action.new_affectation: device.affectation = action.new_affectation

    device.last_updated = datetime.utcnow()

    # 3. Record History
    history_entry = models.History(
        device_id=device.id,
        action_type=action.action_type,
        user_id=action.user_id,
        details=action.details or f"Status: {device.current_status.value}, Aff: {device.affectation.value}",
        timestamp=datetime.utcnow()
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry
