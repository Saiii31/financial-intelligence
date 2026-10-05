from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.ai_service import process_ai_question
from schemas.ai import AIRequest, AIResponse

router = APIRouter()


@router.post("/api/ask", response_model=AIResponse, summary="Ask AI about finances")
def ask_ai(request: AIRequest, db: Session = Depends(get_db)):
    """
    Ask an AI-powered question about financial data.
    Person 4 will integrate the actual LLM here.
    Currently returns a placeholder response.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    
    response = process_ai_question(request.question, db)
    
    return response
