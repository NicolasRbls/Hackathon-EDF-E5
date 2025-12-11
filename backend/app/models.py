from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

# Enums based on "Dictionnaire affectation" and "Dictionnaire etat"
class TypeAffectation(str, enum.Enum):
    MAGASIN = "Magasin"
    BO_NORD = "BO Nord"
    BO_CENTRE = "BO Centre"
    BO_SUD = "BO Sud"
    LABO = "Labo"
    AUCUNE = "[vide]" 

class DeviceStatus(str, enum.Enum):
    EN_LIVRAISON = "en_livraison"
    EN_STOCK = "en_stock"
    POSE = "pose"
    A_TESTER = "a_tester"
    HS = "HS"

class ActionType(str, enum.Enum):
    RECEPTION = "RECEPTION"
    POSE = "POSE"
    DEPOSE = "DEPOSE"
    TRANSFERT = "TRANSFERT"
    TEST = "TEST" # New action for Labo
    AUTRE = "AUTRE"

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    
    # Core Status & Location
    current_status = Column(Enum(DeviceStatus), default=DeviceStatus.EN_LIVRAISON)
    affectation = Column(Enum(TypeAffectation), default=TypeAffectation.MAGASIN) # Replaces current_location
    
    # Metadata from CSV / Business Rules
    num_carton = Column(String, nullable=True, index=True)
    operateur = Column(String, nullable=True) # Bouygues, Orange...
    poste_pose = Column(String, nullable=True) # ID of the electical post (only if POSE)
    
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    history = relationship("History", back_populates="device", cascade="all, delete-orphan")

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MAGASIN = "magasin"
    BO = "bo" # Generic BO or split? User said "Profils" were explicit. Let's assume generic BO role accessing BO_NORD/SUD etc.
    LABO = "labo"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    action_type = Column(Enum(ActionType))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Context of the action
    user_id = Column(String, nullable=True)  # Who performed the action (Legacy or Link to User?)
    # ideally we link to User.id but to keep history fast/simple and supporting legacy imports, we keep String for now.
    details = Column(String, nullable=True)  # Extra info (e.g., "From Magasin to BO Nord")
    
    device = relationship("Device", back_populates="history")
