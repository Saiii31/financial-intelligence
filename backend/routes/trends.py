from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_trends
from schemas.trend import TrendResponse

router = APIRouter()


@router.get("/api/trends", response_model=TrendResponse, summary="Get financial trends")
def get_trends_endpoint(db: Session = Depends(get_db)):
    """
    Get financial trends including income, expense, and savings changes month-over-month.
    Also highlights top spending category increases.
    """
    trends = get_trends(db)
    
    return trends
