# Frontend-Backend Integration Guide

## Quick Start

### 1. Start the Backend

Open a terminal and run:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Create .env from .env.example with MySQL credentials

# Load Person 1's data (first time only)
python load_person1_data.py

# Start the backend server
uvicorn main:app --reload
```

Backend will run on: **http://127.0.0.1:8000**

### 2. Start the Frontend

Open a new terminal and run:

```bash
cd frontend
npm install  # First time only
npm run dev
```

Frontend will run on: **http://localhost:5173**

### 3. Access the Application

Open your browser and navigate to: **http://localhost:5173**

The frontend will automatically fetch data from the backend API.

## API Endpoints Used by Frontend

The frontend calls these backend endpoints:

- `GET /api/dashboard` - Financial metrics (income, expenses, savings, health score)
- `GET /api/cashflow` - Monthly cashflow data
- `GET /api/expenses` - Expense breakdown by category
- `GET /api/liabilities` - Liability information
- `GET /api/recommendations` - Financial recommendations
- `POST /api/ask` - AI chat endpoint (Person 4 integration)

## Troubleshooting

### Frontend shows no data

1. Check if backend is running: Visit http://127.0.0.1:8000/health
2. Check browser console for CORS errors
3. Verify frontend `.env` has `VITE_USE_MOCK=false`
4. Check backend logs for API errors

### Backend connection errors

1. Verify MySQL database is running
2. Check `.env` file has correct database credentials
3. Ensure Person 1's data is loaded: `python load_person1_data.py`

### Port conflicts

- Backend: Change port in `uvicorn main:app --port 8001`
- Frontend: Change port in `vite.config.js` or use `npm run dev -- --port 3000`

## Development Mode

To use mock data without backend:

1. Edit `frontend/.env`: Set `VITE_USE_MOCK=true`
2. Restart frontend server
3. Frontend will use local mock data from `mockDashboard.js`

## Architecture

```
┌─────────────┐         HTTP/REST          ┌──────────────┐
│   React     │ ────────────────────────── │   FastAPI    │
│  Frontend   │  localhost:5173 → 8000     │   Backend    │
│ (Vite/Port) │                            │ (Uvicorn)    │
└─────────────┘                            └──────┬───────┘
                                                  │
                                                  │ SQLAlchemy
                                                  ↓
                                           ┌──────────────┐
                                           │   MySQL DB   │
                                           └──────────────┘
```

## Data Flow

1. **Person 1** runs analytics → Generates `financial_summary.json` and cleaned CSVs
2. **Backend** loads data via `load_person1_data.py` → Stores in MySQL
3. **Frontend** requests data from backend API → Displays in React components
4. **User** views dashboard → Interacts with charts and recommendations
5. **Person 4** (future) → AI chat via `/api/ask` endpoint
