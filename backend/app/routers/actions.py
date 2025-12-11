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

    # 1.5 CHECK PERMISSONS (RBAC)
    if not check_permissions(current_user, device, action.action_type):
        raise HTTPException(
            status_code=403, 
            detail=f"Permission Denied: Role {current_user.role.value} cannot perform {action.action_type.value} on device in {device.affectation.value}"
        )

    # 1.6 LOGISTICS RULES (Auto-Carton Policy)
    # If Moving (Transfert) or Receiving std devices, we AUTO-MOVE the whole carton.
    # Exception: Labo can process 1-by-1.
    is_logistics = action.action_type in [models.ActionType.TRANSFERT, models.ActionType.RECEPTION]
    is_labo_op = (device.affectation == models.TypeAffectation.LABO) or (action.new_affectation == models.TypeAffectation.LABO)
    
    target_devices = [device] # Default: Act on just this one
    
    if is_logistics and not is_labo_op and device.num_carton:
        # User Scanned 1 device, but it belongs to a carton -> MOVE THE WHOLE CARTON
        carton_devices = db.query(models.Device).filter(models.Device.num_carton == device.num_carton).all()
        
        # Integrity Check
        if len(carton_devices) != 4:
             # If carton is broken, we blocked it before. 
             # Now, do we block or allow partial move? 
             # User said "Carton must be 4 to change state". So strict is better.
             raise HTTPException(
                 status_code=400, 
                 detail=f"Carton {device.num_carton} is incomplete ({len(carton_devices)}/4). Cannot Auto-Move."
             )
        target_devices = carton_devices

    # 2. BUSINESS LOGIC & STATE MACHINE
    # Apply to ALL target devices
    primary_history = None
    
    for target in target_devices:
        current_status = target.current_status
        current_aff = target.affectation

        # --- PROFIL MAGASIN ---
        if action.action_type == models.ActionType.RECEPTION:
            # Livraison -> Stock Magasin
            target.current_status = models.DeviceStatus.EN_STOCK
            target.affectation = models.TypeAffectation.MAGASIN
        
        # --- TRANSFERT (Magasin -> BO) ---
        elif action.action_type == models.ActionType.TRANSFERT:
            if not action.new_affectation:
                raise HTTPException(status_code=400, detail="Target affectation required for Transfert")
            target.affectation = action.new_affectation
            target.current_status = models.DeviceStatus.EN_STOCK

        # --- PROFIL BO (Pose / Dépose) ---
        elif action.action_type == models.ActionType.POSE:
            # En stock -> Pose
            if current_status != models.DeviceStatus.EN_STOCK:
                raise HTTPException(status_code=400, detail=f"Device {target.serial_number} must be in STOCK to be POSED. Current: {current_status}")
            
            if not action.poste_pose:
                 raise HTTPException(status_code=400, detail="Poste Pose required")

            target.current_status = models.DeviceStatus.POSE
            target.poste_pose = action.poste_pose

        elif action.action_type == models.ActionType.DEPOSE:
            # Pose -> A Tester (Labo)
            if current_status != models.DeviceStatus.POSE:
                raise HTTPException(status_code=400, detail=f"Device {target.serial_number} must be installed (POSE) to be removed. Current: {current_status}")
            
            target.current_status = models.DeviceStatus.A_TESTER
            target.affectation = models.TypeAffectation.LABO

        # --- PROFIL LABO (Test) ---
        elif action.action_type == models.ActionType.TEST:
            # A Tester -> En Stock (OK) or HS (KO)
            # Logic handled usually by 1-by-1 Labo, but loop supports it if needed.
            if current_status != models.DeviceStatus.A_TESTER:
                 pass # Allow re-test?

            # We assume generic 'new_status' passed for Labo result (or specific logic)
            # For hackathon simplicity, let's say input 'details' says result or we infer?
            # User didn't specify Labo inputs yet. Let's assume passed 'new_status' if provided.
            if action.new_status:
                target.current_status = action.new_status
                if target.current_status == models.DeviceStatus.EN_STOCK:
                    target.affectation = models.TypeAffectation.MAGASIN # Back to stock

        target.last_updated = datetime.utcnow()

        # 3. Record History
        history_entry = models.History(
            device_id=target.id,
            action_type=action.action_type,
            user_id=current_user.username,
            details=action.details or f"Auto-Action: {action.action_type}",
            timestamp=datetime.utcnow()
        )
        db.add(history_entry)
        
        if target.id == device.id:
            primary_history = history_entry

    db.commit()
    return primary_history
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

