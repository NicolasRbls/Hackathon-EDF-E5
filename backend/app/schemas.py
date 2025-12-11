from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .models import DeviceStatus, ActionType, TypeAffectation

class DeviceBase(BaseModel):
    serial_number: str
    num_carton: Optional[str] = None
    operateur: Optional[str] = None
    poste_pose: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    current_status: DeviceStatus
    affectation: TypeAffectation
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class ActionCreate(BaseModel):
    device_serial: str
    action_type: ActionType
    user_id: str
    details: Optional[str] = None 
    # Contextual fields
    new_affectation: Optional[TypeAffectation] = None
    new_status: Optional[DeviceStatus] = None
    poste_pose: Optional[str] = None

class BulkActionCreate(BaseModel):
    action_type: ActionType
    user_id: str
    details: Optional[str] = None
    
    # Target selection (One of these must be provided)
    device_serials: Optional[List[str]] = None
    num_carton: Optional[str] = None # Apply to all devices in this carton
    
    # Context
    new_affectation: Optional[TypeAffectation] = None
    new_status: Optional[DeviceStatus] = None
    poste_pose: Optional[str] = None

class History(BaseModel):
    id: int
    device_id: int
    action_type: ActionType
    timestamp: datetime
    user_id: Optional[str] = None
    details: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

from .models import UserRole

class UserBase(BaseModel):
    username: str
    role: UserRole = UserRole.VIEWER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
