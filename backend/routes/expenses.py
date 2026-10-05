from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_expenses_by_category
from schemas.expense import ExpenseResponse

router = APIRouter()


@router.get("/api/expenses", response_model=ExpenseResponse, summary="Get expenses by category")
def get_expenses_endpoint(db: Session = Depends(get_db)):
    """
    Get expenses broken down by category with amounts and percentages.
    Used for expense distribution charts.
    """
    expenses = get_expenses_by_category(db)
    
    return {"expenses": expenses}
