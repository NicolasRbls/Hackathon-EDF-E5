from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .models import DeviceStatus

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
