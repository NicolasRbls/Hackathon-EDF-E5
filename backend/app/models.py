from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqEnum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from .database import Base

class DeviceStatus(str, enum.Enum):
    STOCK = "STOCK"
    EN_SERVICE = "EN_SERVICE"
    EN_TRANSIT = "EN_TRANSIT"
    RETOUR_CONSTRUCTEUR = "RETOUR_CONSTRUCTEUR"
    REBU = "REBU"

class ActionType(str, enum.Enum):
    RECEPTION = "RECEPTION"
    POSE = "POSE"
    DEPOSE = "DEPOSE"
    TRANSFERT = "TRANSFERT"
    AUTRE = "AUTRE"

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True, nullable=False)
    current_status = Column(SqEnum(DeviceStatus), default=DeviceStatus.STOCK)
    current_location = Column(String, default="Inconnu")
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    history = relationship("History", back_populates="device")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    action_type = Column(SqEnum(ActionType), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    user_id = Column(String, default="System")
    location = Column(String, nullable=True)

    device = relationship("Device", back_populates="history")
