"""
Drop-in FastAPI router. Person 2 adds ONE line in main.py:
    from ai.router import router as ai_router
    app.include_router(ai_router)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai import agent

router = APIRouter(prefix="/api", tags=["AI"])


class ChatRequest(BaseModel):
    message: str | None = None
    question: str | None = None      # supports Person 2's {"question": ...} contract too
    session_id: str = "default"


@router.post("/chat")
@router.post("/ask")
def chat(req: ChatRequest):
    text = req.message or req.question
    if not text:
        raise HTTPException(400, "message is required")
    try:
        return agent.ask(text, req.session_id)
    except Exception as e:
        raise HTTPException(500, f"AI error: {e}")


@router.get("/ai-summary")
def ai_summary(refresh: bool = False):
    try:
        return agent.dashboard_summary(refresh)
    except Exception as e:
        raise HTTPException(500, f"AI error: {e}")


@router.post("/ai/rebuild-index")
def rebuild_index():
    from ai.retriever import build_index
    build_index(force=True)
    return {"status": "rebuilt"}
