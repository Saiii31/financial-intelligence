# Financial Intelligence Platform - Backend

FastAPI backend for the Financial Intelligence Platform. This backend exposes verified financial analytics to the React frontend (Person 3) and AI layer (Person 4).

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MySQL (with SQLite fallback for development)
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # Database connection and session management
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
│
├── models/                 # SQLAlchemy ORM models
│   ├── transaction.py
│   ├── asset.py
│   ├── liability.py
│   ├── financial_metric.py
│   ├── monthly_trend.py
│   └── recommendation.py
│
├── schemas/                # Pydantic request/response schemas
│   ├── dashboard.py
│   ├── cashflow.py
│   ├── expense.py
│   ├── liability.py
│   ├── trend.py
│   ├── recommendation.py
│   └── ai.py
│
├── routes/                 # FastAPI route handlers
│   ├── dashboard.py
│   ├── cashflow.py
│   ├── expenses.py
│   ├── liabilities.py
│   ├── trends.py
│   ├── recommendations.py
│   ├── transactions.py
│   └── ai.py
│
└── services/               # Business logic and data access
    ├── database_service.py
    ├── analytics_service.py
    └── ai_service.py
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and configure your MySQL credentials:

```bash
cp .env.example .env
```

Edit `.env` with your MySQL settings:
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=financial_intelligence
DB_USER=root
DB_PASSWORD=your_password
```

**Note**: The `.env` file is git-ignored and should never be committed.

### 5. Create MySQL Database

```sql
CREATE DATABASE financial_intelligence;
```

### 6. Run the Server

```bash
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000`

**Important**: If MySQL is not configured or the database doesn't exist, the API will return mock data for development purposes. Ensure MySQL is running and the database exists before using real data.

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Dashboard
- `GET /api/dashboard` - Get overall financial metrics (income, expenses, savings, assets, liabilities, net worth, debt-to-income, health score)

### Cashflow
- `GET /api/cashflow` - Get monthly cashflow data (income, expenses, savings by month)

### Expenses
- `GET /api/expenses` - Get expenses broken down by category with amounts and percentages

### Liabilities
- `GET /api/liabilities` - Get all liabilities with outstanding amounts, interest rates, EMI, and due dates

### Trends
- `GET /api/trends` - Get financial trends (income, expense, savings changes month-over-month)

### Recommendations
- `GET /api/recommendations` - Get financial recommendations with priority levels and categories

### Transactions
- `GET /api/transactions` - Get transactions with optional filters:
  - `category` - Filter by category
  - `type` - Filter by type (income/expense)
  - `start_date` - Filter by start date
  - `end_date` - Filter by end date

### AI
- `POST /api/ask` - Ask AI-powered questions about financial data (Person 4 will integrate LLM here)

## Database Schema

### Tables

**transactions**
- id, txn_id, date, category, description, amount, type, is_duplicate, is_anomaly, created_at

**assets**
- id, asset_id, type, value, as_of_date, created_at

**liabilities**
- id, liability_id, type, outstanding, interest_rate, emi, due_date, created_at

**financial_metrics**
- id, income, expenses, savings, savings_rate, total_assets, total_liabilities, net_worth, monthly_emi, debt_to_income, health_score, created_at

**monthly_trends**
- id, month, income, expenses, savings, created_at

**recommendations**
- id, recommendation, priority, category, created_at

## Development Notes

### Mock Data

Currently, the backend returns mock data when the database is empty. This is intentional for development and testing purposes. When Person 1's analytics are ready:

1. Update the service functions to use real database data
2. Replace mock data returns with actual database queries
3. Verify API values match Person 1's analytics results

### Database Fallback

If MySQL is not configured or unavailable, the backend automatically falls back to SQLite for development. This ensures the API remains functional during development without requiring a MySQL server.

### CORS

CORS is configured to allow requests from `http://localhost:3000` (React development server). Update the CORS origins in `main.py` if your React app runs on a different port.

### Integration with Team Members

**Person 1 (Data Engineering + Analytics)**
- Person 1 provides verified financial analytics
- Use `analytics_service.py` functions to save Person 1's results to the database
- Do not duplicate Person 1's calculation logic in the backend

**Person 3 (React Frontend)**
- All API endpoints are ready for React integration
- Refer to Swagger documentation for request/response formats
- CORS is configured for React on localhost:3000

**Person 4 (AI/LLM)**
- The `ai_service.py` provides a placeholder for LLM integration
- Backend data access functions are available for AI tools:
  - `get_dashboard_metrics()`
  - `get_cashflow()`
  - `get_expenses_by_category()`
  - `get_liabilities()`
  - `get_trends()`
  - `get_health_score()`
  - `get_anomalies()`
  - `get_recommendations()`

## Security

- Never commit `.env` file
- Never hardcode database credentials
- Database credentials come from environment variables
- AI should access financial data through controlled backend services, not direct database access

## Testing

Test all endpoints manually or use Postman:

1. Health check: `GET http://127.0.0.1:8000/health`
2. Dashboard: `GET http://127.0.0.1:8000/api/dashboard`
3. Cashflow: `GET http://127.0.0.1:8000/api/cashflow`
4. Expenses: `GET http://127.0.0.1:8000/api/expenses`
5. Liabilities: `GET http://127.0.0.1:8000/api/liabilities`
6. Trends: `GET http://127.0.0.1:8000/api/trends`
7. Recommendations: `GET http://127.0.0.1:8000/api/recommendations`
8. Transactions: `GET http://127.0.0.1:8000/api/transactions`
9. AI: `POST http://127.0.0.1:8000/api/ask` with body `{"question": "Your question here"}`

## Success Criteria

The backend is complete when:
- ✅ FastAPI starts successfully
- ✅ `/health` endpoint works
- ✅ Database connection works (MySQL or SQLite fallback)
- ✅ Swagger documentation is accessible
- ✅ All API endpoints return valid JSON responses
- ✅ Mock data works for development
- ✅ Ready for Person 1 analytics integration
- ✅ Ready for React frontend integration
- ✅ Ready for Person 4 AI integration
