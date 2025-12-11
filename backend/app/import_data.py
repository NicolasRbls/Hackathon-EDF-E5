import csv
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Device, DeviceStatus, TypeAffectation, History, ActionType
from app.database import SQLALCHEMY_DATABASE_URL

# Setup DB connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def import_csv(file_path: str):
    db = SessionLocal()
    try:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            count = 0
            
            print("🚀 Starting Import...")
            for row in reader:
                # Map CSV fields to Model
                serial_number = row['n_serie_concentrateur']
                
                # Enum Mapping (Simple direct mapping if CSV matches exactly, else careful)
                affectation_raw = row['affectation']
                etat_raw = row['etat']
                
                # Affectation Mapping
                try:
                    # Handle specific naming differences if any
                    # The CSV seems to match the Enum values defined: "Magasin", "BO Centre", etc.
                    # We might need to handle empty or mismatch
                    if not affectation_raw:
                        affectation = TypeAffectation.AUCUNE
                    else:
                        affectation = TypeAffectation(affectation_raw)
                except ValueError:
                    print(f"⚠️ Warning: Unknown Affectation '{affectation_raw}' for {serial_number}. Defaulting to AUCUNE.")
                    affectation = TypeAffectation.AUCUNE

                # Status Mapping
                try:
                    # CSV "en_livraison" matches DeviceStatus.EN_LIVRAISON ("en_livraison")
                    status = DeviceStatus(etat_raw)
                except ValueError:
                    print(f"⚠️ Warning: Unknown Status '{etat_raw}' for {serial_number}. Defaulting to EN_LIVRAISON.")
                    status = DeviceStatus.EN_LIVRAISON

                # Create/Update Device
                device = db.query(Device).filter(Device.serial_number == serial_number).first()
                if not device:
                    device = Device(serial_number=serial_number)
                    db.add(device)
                
                device.num_carton = row['num_carton']
                device.operateur = row['operateur']
                device.affectation = affectation
                device.current_status = status
                device.poste_pose = row['poste_pose']
                
                last_update = parse_date(row['date_dernier_etat'])
                if last_update:
                    device.last_updated = last_update

                # Optional: Generate Initial History if new
                # For now, we simply ensure the device state is current.
                
                count += 1
                if count % 100 == 0:
                    print(f"⏳ Processed {count} devices...")
            
            db.commit()
            print(f"✅ Import Complete! Total processed: {count}")
            
    except Exception as e:
        print(f"❌ Error during import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Assuming script is run from backend root, and CSV is at project root
    # Project Structure:
    # /root
    #   /backend
    #   BDD_defi_EDF.csv
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "BDD_defi_EDF.csv")
    print(f"📂 Looking for CSV at: {csv_path}")
    import_csv(csv_path)
