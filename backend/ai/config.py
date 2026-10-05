"""All settings in one place. Values come from .env - nothing is hard-coded."""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # change in .env if deprecated
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Person 2's FastAPI base URL. If AI is mounted INSIDE the same FastAPI app, keep localhost.
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# True = use built-in sample data (work before Person 2 is ready). False = call real APIs.
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "data/vectorstore/faiss_index")
