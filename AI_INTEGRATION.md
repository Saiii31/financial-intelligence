# AI Layer Integration Guide

## ✅ Integration Status

The AI layer has been successfully integrated into the backend:
- AI router added to FastAPI (`ai/router.py`)
- AI tools configured to call backend API endpoints
- Intent-based question routing implemented
- FAISS semantic search for contextual queries
- LangChain + Groq LLM integration ready

## 🚀 Setup Instructions

### 1. Get a Groq API Key

1. Go to https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Copy the API key

### 2. Configure Environment Variables

Add these to your `backend/.env` file:

```bash
# Database (already configured)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=financial_intelligence
DB_USER=root
DB_PASSWORD=sai123

# AI Layer Configuration
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
USE_MOCK=false
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTORSTORE_DIR=data/vectorstore/faiss_index
```

### 3. Rebuild the Vector Index (First Time)

The AI layer needs to build a semantic search index from your financial data:

```bash
cd backend
python -c "from ai.retriever import build_index; build_index(force=True)"
```

This will:
- Fetch data from all backend endpoints
- Create embeddings using sentence-transformers
- Build a FAISS vector index
- Save it to `data/vectorstore/faiss_index`

### 4. Restart the Backend

```bash
cd backend
uvicorn main:app --reload
```

## 🎯 How to Use the AI

### API Endpoints

**Chat/Ask Question:**
```bash
POST /api/ask
POST /api/chat

Body:
{
  "question": "How much did I spend on food last month?",
  "session_id": "user123"  # Optional, for conversation history
}
```

**Get AI Summary:**
```bash
GET /api/ai-summary?refresh=false
```

**Rebuild Vector Index:**
```bash
POST /api/ai/rebuild-index
```

### Example Questions

The AI can answer questions like:
- "How much did I spend on food last month?"
- "What's my debt situation?"
- "Why did my savings drop?"
- "What should I do to improve my finances?"
- "Show me my highest expense category"
- "What's my financial health score?"

### Intent Routing

The AI automatically detects intent and calls appropriate tools:
- **Monthly expense** → `/api/cashflow`
- **Category spending** → `/api/expenses`
- **Savings analysis** → `/api/cashflow`, `/api/trends`
- **Debt priority** → `/api/liabilities`
- **Financial health** → `/api/dashboard`
- **Transactions** → `/api/transactions`
- **General/complex** → FAISS semantic search + multiple tools

## 🔧 Troubleshooting

### Dependency Conflicts

There are minor dependency conflicts between langchain and existing packages. These are generally non-critical for the hackathon. If you encounter issues:

```bash
# Force reinstall compatible versions
pip install --force-reinstall fastapi==0.104.1 anyio==3.7.1 numpy==1.26.4
```

### FAISS Index Build Fails

If the vector index build fails:
1. Ensure backend is running and data is loaded
2. Check API endpoints are accessible
3. Try: `curl http://127.0.0.1:8000/api/dashboard`
4. Rebuild with: `POST /api/ai/rebuild-index`

### No GROQ API Key

Without a GROQ API key, the AI layer will fail. To test without a key temporarily:

Set `USE_MOCK=true` in `.env` - this will use mock data but still demonstrate the AI flow.

## 📊 AI Architecture

```
User Question
    ↓
Intent Detection (keyword-based)
    ↓
Tool Selection (which APIs to call)
    ↓
Data Fetching (from backend endpoints)
    ↓
[Optional] FAISS Semantic Search
    ↓
Context Assembly
    ↓
Groq LLM (LLaMA 3.3 70B)
    ↓
Natural Language Answer
```

## 🎨 Frontend Integration

The frontend already has an AI chat component (`frontend/src/components/AIChat.jsx`). To connect it:

1. Ensure backend is running with AI layer enabled
2. Frontend calls `/api/ask` endpoint
3. AI responds with answer, sources, and intent

## 📝 Notes

- The AI layer uses **deterministic intent routing** for reliability
- All financial data comes from **verified backend APIs** (not LLM hallucinations)
- The LLM only **explains** the data, doesn't calculate it
- FAISS provides **semantic search** for contextual questions
- Session history enables **follow-up questions**
