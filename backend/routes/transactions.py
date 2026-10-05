from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from services.database_service import get_transactions

router = APIRouter()


@router.get("/api/transactions", summary="Get transactions with optional filters")
def get_transactions_endpoint(
    category: str = Query(None, description="Filter by category"),
    type: str = Query(None, description="Filter by type (income/expense)"),
    start_date: date = Query(None, description="Filter by start date"),
    end_date: date = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db)
):
    """
    Get transactions with optional filtering by category, type, and date range.
    Returns up to 100 most recent transactions.
    """
    transactions = get_transactions(db, category, type, start_date, end_date)
    
    return {"transactions": transactions}
