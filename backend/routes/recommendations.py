from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.database_service import get_recommendations
from schemas.recommendation import RecommendationResponse

router = APIRouter()


@router.get("/api/recommendations", response_model=RecommendationResponse, summary="Get recommendations")
def get_recommendations_endpoint(db: Session = Depends(get_db)):
    """
    Get financial recommendations with priority levels and categories.
    Recommendations come from Person 1's analytics engine.
    """
    recommendations = get_recommendations(db)
    
    return {"recommendations": recommendations}
