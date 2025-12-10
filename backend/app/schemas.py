from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .models import DeviceStatus, ActionType

class DeviceBase(BaseModel):
    serial_number: str
    current_location: Optional[str] = "Inconnu"

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    current_status: DeviceStatus
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class ActionCreate(BaseModel):
    serial_number: str
    action_type: ActionType
    location: Optional[str] = None
    user_id: Optional[str] = "System"

class History(BaseModel):
    id: int
    action_type: ActionType
    timestamp: datetime
    user_id: str
    location: Optional[str]
    device_id: int

    model_config = ConfigDict(from_attributes=True)

