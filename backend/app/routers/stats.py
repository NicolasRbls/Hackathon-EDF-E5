from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas, database
from ..database import get_db

router = APIRouter(
    tags=["dashboard"],
)

@router.get("/stats/stocks")
def get_stock_stats(db: Session = Depends(get_db)):
    """
    Returns aggregation of devices by location and status.
    Example: [{'location': 'Bastia', 'status': 'Stock', 'count': 12}, ...]
    """
    results = db.query(
        models.Device.current_location,
        models.Device.current_status,
        func.count(models.Device.id).label("count")
    ).group_by(
        models.Device.current_location,
        models.Device.current_status
    ).all()
    
    # Format for easy frontend consumption
    stats = []
    for loc, stat, count in results:
        stats.append({
            "location": loc,
            "status": stat,
            "count": count
        })
    return stats

@router.get("/dashboard/history", response_model=List[schemas.History])
def get_dashboard_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns the most recent actions across all devices.
    """
    return db.query(models.History).order_by(models.History.timestamp.desc()).limit(limit).all()
