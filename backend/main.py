from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routes import dashboard, cashflow, expenses, liabilities, trends, recommendations, transactions, ai
# Temporarily disabled due to dependency conflicts
# from ai.router import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create database tables.")
        print(f"Error: {e}")
    yield


app = FastAPI(
    title="Financial Intelligence API",
    description="Backend API for Financial Intelligence Platform - Exposes verified financial analytics to React frontend and AI layer",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(cashflow.router)
app.include_router(expenses.router)
app.include_router(liabilities.router)
app.include_router(trends.router)
app.include_router(recommendations.router)
app.include_router(transactions.router)
app.include_router(ai.router)
# Temporarily disabled due to dependency conflicts
# app.include_router(ai_router)


@app.get("/health", summary="Health check endpoint")
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok"}
