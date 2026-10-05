from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_dashboard_metrics
from schemas.dashboard import DashboardResponse

router = APIRouter()


@router.get("/api/dashboard", response_model=DashboardResponse, summary="Get dashboard metrics")
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get overall financial dashboard metrics including income, expenses, savings,
    assets, liabilities, net worth, debt-to-income ratio, and health score.
    """
    metrics = get_dashboard_metrics(db)
    
    if metrics is None:
        raise HTTPException(status_code=404, detail="No financial metrics found. Please load Person 1's data.")
    
    return metrics
