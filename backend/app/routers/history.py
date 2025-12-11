from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, database, security

router = APIRouter(
    prefix="/history",
    tags=["history"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.History])
def search_history(
    role: Optional[models.UserRole] = None,
    username: Optional[str] = None,
    action_type: Optional[models.ActionType] = None,
    device_serial: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Search history logs with filters (e.g., 'Logs des Magasiniers').
    Only Admins or the user themselves (if searching own logs) should access this?
    For the hackathon, we allow verified users to search (e.g. Viewer Dashboard).
    """
    
    # Security / RBAC for Logs
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.VIEWER]:
        # Rule: You can ONLY access logs for YOUR OWN Role (Department visibility)
        if role and role != current_user.role:
             raise HTTPException(status_code=403, detail=f"You are not authorized to view logs for role: {role}")
        
        # Force strict filtering to current user's role
        # Whatever the user asks, we constrain the scope to their role.
        role = current_user.role 
    
    # Base Query
    query = db.query(models.History)
    
    # Joins if we need to filter by User Role
    # Valid filter (Admin/Viewer) OR Forced filter (Regular User)
    if role:
        # Join History -> User on username
        query = query.join(models.User, models.History.user_id == models.User.username)
        query = query.filter(models.User.role == role)
    
    # Simple filters
    if username:
        query = query.filter(models.History.user_id == username)
    
    if action_type:
        query = query.filter(models.History.action_type == action_type)
        
    if device_serial:
        # Join History -> Device if serial provided (though history stores device_id, easier to join)
        query = query.join(models.Device, models.History.device_id == models.Device.id)
        query = query.filter(models.Device.serial_number == device_serial)
    
    # Sorting: Newest first
    query = query.order_by(models.History.timestamp.desc())
    
    return query.offset(skip).limit(limit).all()
