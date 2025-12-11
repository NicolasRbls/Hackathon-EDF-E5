from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime
from typing import List

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

from app import security

def check_permissions(user: models.User, device: models.Device, action_type: models.ActionType):
    if user.role == models.UserRole.ADMIN:
        return True
        
    # Mapping UserRole to TypeAffectation strings
    # TypeAffectation: "Magasin", "BO Nord", "BO Centre", "BO Sud", "Labo"
    # UserRole: "magasin", "bo_nord", "bo_centre", "bo_sud", "labo"
    
    # 1. MAGASIN
    if user.role == models.UserRole.MAGASIN:
        # Can always RECEPTION (creates stock)
        if action_type == models.ActionType.RECEPTION:
            return True
        # Can TRANSFERT if device is currently in MAGASIN
        if action_type == models.ActionType.TRANSFERT and device.affectation == models.TypeAffectation.MAGASIN:
            return True
        return False
        
    # 2. BO (Regional)
    # Define mapping
    bo_map = {
        models.UserRole.BO_NORD: models.TypeAffectation.BO_NORD,
        models.UserRole.BO_CENTRE: models.TypeAffectation.BO_CENTRE,
        models.UserRole.BO_SUD: models.TypeAffectation.BO_SUD
    }
    
    if user.role in bo_map:
        target_zone = bo_map[user.role]
        # Must be IN the zone to act (Pose, Depose)
        if device.affectation == target_zone:
            return True
        return False

    # 3. LABO
    if user.role == models.UserRole.LABO:
        if device.affectation == models.TypeAffectation.LABO:
            return True
        return False
        
    return False

@router.post("/", response_model=schemas.History)
def create_action(
    action: schemas.ActionCreate, 
    current_user: models.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    # 1. Verify device exists
    device = db.query(models.Device).filter(models.Device.serial_number == action.device_serial).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # 1.5 CHECK PERMISSONS
    if not check_permissions(current_user, device, action.action_type):
        raise HTTPException(
            status_code=403, 
            detail=f"Permission Denied: Role {current_user.role.value} cannot perform {action.action_type.value} on device in {device.affectation.value}"
        )

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
        user_id=current_user.username, # Enforce Real User
        details=action.details or f"Status: {device.current_status.value}, Aff: {device.affectation.value}",
        timestamp=datetime.utcnow()
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    
    # Explicit conversion to avoid Pydantic/SQLAlchemy Enum mismatch issues
    return schemas.History(
        id=history_entry.id,
        device_id=history_entry.device_id,
        action_type=history_entry.action_type,
        timestamp=history_entry.timestamp,
        user_id=history_entry.user_id,
        details=history_entry.details
    )
from app import security

@router.post("/bulk", response_model=List[schemas.History])
def bulk_create_action(
    action: schemas.BulkActionCreate, 
    current_user: models.User = Depends(security.require_role([models.UserRole.ADMIN, models.UserRole.MAGASIN])),
    db: Session = Depends(get_db)
):
    """
    Perform an action on multiple devices at once.
    Target by list of Serials OR by Key (Carton Number).
    """
    target_devices = []
    
    # 1. Identify Targets
    if action.device_serials:
        target_devices = db.query(models.Device).filter(models.Device.serial_number.in_(action.device_serials)).all()
        # Verify all found (Strict mode? Or permissive? Let's be permissive and return only processed)
    
    elif action.num_carton:
        target_devices = db.query(models.Device).filter(models.Device.num_carton == action.num_carton).all()
        if not target_devices:
             raise HTTPException(status_code=404, detail=f"No devices found in carton {action.num_carton}")
    else:
        raise HTTPException(status_code=400, detail="Must provide either device_serials or num_carton")

    created_history = []
    
    # 2. Process each device
    for device in target_devices:
        # State Machine Logic (Inline reused or we could extract a service function)
        # For simplicity, we apply the update logic directly here as it mirrors the single action
        
        # Apply Transitions (Simplified for Bulk - usually just Status/Aff updates)
        if action.new_status:
            device.current_status = action.new_status
        # Specific logic for Reception (Magasin default)
        if action.action_type == models.ActionType.RECEPTION:
             device.current_status = models.DeviceStatus.EN_STOCK
             device.affectation = models.TypeAffectation.MAGASIN
        elif action.new_affectation:
            device.affectation = action.new_affectation
            
        device.last_updated = datetime.utcnow()
        
        # Record History
        history = models.History(
            device_id=device.id,
            action_type=action.action_type,
            user_id=action.user_id,
            details=action.details or f"Bulk Action: {action.action_type}",
            timestamp=datetime.utcnow()
        )
        db.add(history)
        created_history.append(history)
    
    db.commit()
    # Refresh is expensive for bulk, we might skip it or just return the list
    return created_history

