from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from typing import List, Dict, Any

router = APIRouter(
    tags=["stats"]
)

@router.get("/stats/stocks")
def get_stocks(db: Session = Depends(get_db)):
    """
    Returns aggregation of devices count by Affectation and Status.
    Example: {"Magasin": {"en_stock": 12, "en_livraison": 5}, "BO Nord": {...}}
    """
    results = db.query(
        models.Device.affectation,
        models.Device.current_status,
        func.count(models.Device.id)
    ).group_by(models.Device.affectation, models.Device.current_status).all()

    stats = {}
    for affectation, status, count in results:
        # Convert Enum to string for JSON serialization
        aff_str = affectation.value if affectation else "Unknown"
        stat_str = status.value if status else "Unknown"
        
        if aff_str not in stats:
            stats[aff_str] = {}
        stats[aff_str][stat_str] = count
        
    return stats

@router.get("/dashboard/history", response_model=List[schemas.History])
def get_recent_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns the most recent actions relative to devices.
    """
    return db.query(models.History).order_by(models.History.timestamp.desc()).limit(limit).all()

from fastapi.responses import StreamingResponse
import io
import csv

@router.get("/export/csv")
def export_devices_csv(db: Session = Depends(get_db)):
    """
    Generates a CSV export of all devices and their current state.
    """
    devices = db.query(models.Device).all()
    
    # Create an in-memory file-like object
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write Header
    writer.writerow(["Serial Number", "Carton", "Operateur", "Status", "Affectation", "Poste", "Last Update"])
    
    # Write Data
    for d in devices:
        writer.writerow([
            d.serial_number,
            d.num_carton or "",
            d.operateur or "",
            d.current_status.value if d.current_status else "",
            d.affectation.value if d.affectation else "",
            d.poste_pose or "",
            d.last_updated.isoformat() if d.last_updated else ""
        ])
    
    output.seek(0)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=inventaire_edf.csv"
    return response
