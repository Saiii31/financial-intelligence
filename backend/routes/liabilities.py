from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_liabilities
from schemas.liability import LiabilityResponse

router = APIRouter()


@router.get("/api/liabilities", response_model=LiabilityResponse, summary="Get liabilities")
def get_liabilities_endpoint(db: Session = Depends(get_db)):
    """
    Get all liabilities including outstanding amounts, interest rates, EMI, and due dates.
    """
    liabilities = get_liabilities(db)
    
    return {"liabilities": liabilities}
