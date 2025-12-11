import json
import random
import sys
import os

# Add backend to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import SQLALCHEMY_DATABASE_URL
from app import models

# Setup DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_coords():
    db = SessionLocal()
    try:
        # Load Coords
        with open("scripts/corsica_gps.json", "r") as f:
            coords_pool = json.load(f)
            
        print(f"🌍 Loaded {len(coords_pool)} coordinates.")
        
        # Correct Logic: Only update devices that are "POSE" (Deployed)
        devices = db.query(models.Device).filter(models.Device.current_status == models.DeviceStatus.POSE).all()
        print(f"🔧 Found {len(devices)} deployed (POSE) devices.")
        
        updated_count = 0
        for device in devices:
            if not coords_pool:
                print("⚠️ Ran out of coordinates!")
                break
                
            # Randomly pick a coord or just pop? Pop to avoid collision implies unique location
            coord = coords_pool.pop(random.randint(0, len(coords_pool) - 1))
            
            device.latitude = coord["latitude"]
            device.longitude = coord["longitude"]
            updated_count += 1
            
        db.commit()
        print(f"✅ Successfully updated {updated_count} devices with GPS coordinates.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_coords()
