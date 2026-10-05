from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_cashflow
from schemas.cashflow import CashflowResponse, CashflowItem

router = APIRouter()


@router.get("/api/cashflow", response_model=CashflowResponse, summary="Get monthly cashflow")
def get_cashflow_endpoint(db: Session = Depends(get_db)):
    """
    Get monthly cashflow data including income, expenses, and savings for each month.
    Used for cashflow charts in the dashboard.
    """
    cashflow = get_cashflow(db)
    
    return {"cashflow": cashflow}
