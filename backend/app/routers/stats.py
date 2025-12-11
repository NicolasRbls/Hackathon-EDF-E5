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
