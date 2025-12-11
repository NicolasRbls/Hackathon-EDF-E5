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
    # Contextual fields for state transitions
    new_affectation: Optional[TypeAffectation] = None
    new_status: Optional[DeviceStatus] = None
    poste_pose: Optional[str] = None

class History(BaseModel):
    id: int
    action_type: ActionType
    timestamp: datetime
    user_id: Optional[str]
    details: Optional[str]

    model_config = ConfigDict(from_attributes=True)
