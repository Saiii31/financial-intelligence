# Master Prompt for Financial Intelligence Platform PPT Generation

## Context
You are tasked with creating a professional PowerPoint presentation for a Financial Intelligence Platform hackathon project. This is a team project with 4 members, each handling different aspects of the system.

## Project Overview
**Project Name:** Financial Intelligence Platform
**Purpose:** A comprehensive financial analytics and intelligence system that provides users with insights into their financial health, spending patterns, and personalized recommendations.

## Team Structure
- **Person 1:** Data Engineering + Financial Analytics
  - Handles data processing, cleaning, and financial calculations
  - Generates financial summaries, anomaly detection, and recommendations
  - Outputs: financial_summary.json, transactions_clean.csv, assets_clean.csv, liabilities_clean.csv

- **Person 2:** Backend + MySQL + FastAPI
  - FastAPI backend with MySQL database
  - RESTful API endpoints for data access
  - Database models and services layer
  - Integration with other team members' outputs

- **Person 3:** React Frontend
  - React + Vite application
  - Interactive dashboard with visualizations
  - Recharts for data visualization
  - User interface for financial insights

- **Person 4:** AI/LLM Integration
  - LangChain-based AI agent
  - Intent-based question answering
  - Semantic search over financial data
  - Tool calling for verified financial data

## Technical Architecture

### Backend Stack
- **Framework:** FastAPI (Python)
- **Database:** MySQL with SQLAlchemy ORM (SQLite fallback for development)
- **API:** RESTful endpoints with automatic Swagger documentation
- **Authentication:** Environment-based configuration
- **CORS:** Configured for React frontend

### Database Models
- Transaction (with anomaly/duplicate detection flags)
- Asset (savings, investments, properties)
- Liability (loans, credit cards, mortgages)
- FinancialMetric (dashboard KPIs)
- MonthlyTrend (historical trends)
- Recommendation (AI-generated suggestions)

### API Endpoints
- `/health` - Health check
- `/api/dashboard` - Financial metrics and KPIs
- `/api/cashflow` - Monthly income/expense trends
- `/api/expenses` - Expense breakdown by category
- `/api/liabilities` - Liability information
- `/api/trends` - Financial trends over time
- `/api/recommendations` - Personalized recommendations
- `/api/transactions` - Transaction data with filters
- `/api/ask` - AI question answering
- `/api/chat` - Conversational AI interface
- `/api/ai-summary` - AI-generated financial summary

### Frontend Stack
- **Framework:** React with Vite
- **Visualization:** Recharts library
- **HTTP Client:** Axios
- **Features:**
  - Interactive dashboard
  - Financial metrics display
  - Cashflow charts
  - Expense category breakdown
  - Liability tracking
  - AI chat interface

### AI Layer Stack
- **Framework:** LangChain
- **LLM:** Groq API
- **Vector Store:** FAISS for semantic search
- **Embeddings:** Sentence Transformers
- **Capabilities:**
  - Intent detection and routing
  - Tool calling for verified data
  - Contextual question answering
  - Conversation history management

## Key Features

### 1. Financial Dashboard
- Real-time financial metrics (net worth, savings rate, debt-to-income ratio)
- Health score calculation (0-100 scale)
- Monthly cashflow visualization
- Expense breakdown by category (17 categories)
- Asset and liability tracking

### 2. Data Processing
- Transaction anomaly detection
- Duplicate transaction identification
- Automated data cleaning and validation
- Monthly trend calculation from actual data
- Financial metric aggregation

### 3. AI-Powered Insights
- Natural language question answering
- Semantic search over financial documents
- Personalized recommendations
- Conversational interface with context
- Verified data from backend APIs

### 4. Data Integration
- Seamless integration between all team components
- Real data from Person 1's analytics
- API-based data access for frontend and AI
- MySQL database with proper relationships
- Environment-based configuration

## Implementation Status

### Completed ✅
- Complete backend structure with FastAPI
- MySQL database with all models
- Person 1's data loaded (811 transactions, 8 assets, 3 liabilities)
- React frontend with API integration
- AI layer with LangChain and Groq
- All API endpoints functional
- Real data flowing through the system
- Health score calculation (83.2)
- 17 expense categories with percentages
- Monthly trends from actual transaction data

### Data Flow
1. Person 1 processes raw financial data
2. Outputs cleaned CSV files and JSON summary
3. Backend loads data into MySQL database
4. Frontend fetches data via REST API
5. AI layer queries backend for verified data
6. User interacts through React dashboard
7. AI provides insights via natural language

## Project Highlights

### Innovation
- Intent-based AI routing for reliable answers
- Semantic search over financial context
- Real-time anomaly detection
- Zero-income filtering for accurate trends
- Modular architecture for easy maintenance

### Technical Excellence
- Clean separation of concerns (models, schemas, routes, services)
- Proper dependency injection
- Automatic Swagger documentation
- Environment-based configuration
- Git-ignored sensitive files
- SQLite fallback for development

### User Experience
- Interactive visualizations
- Natural language interface
- Real-time financial insights
- Personalized recommendations
- Comprehensive financial health tracking

## Future Enhancements
- Multi-user authentication
- Real-time data streaming
- Advanced ML models for prediction
- Mobile application
- Integration with financial institutions
- Advanced anomaly detection algorithms

## Presentation Requirements

Create a 10-15 slide PowerPoint presentation covering:

1. **Title Slide** - Project name, team members, hackathon name
2. **Problem Statement** - Why financial intelligence is needed
3. **Solution Overview** - High-level system architecture
4. **Team Structure** - Roles and responsibilities
5. **Technical Architecture** - Stack and components
6. **Backend Implementation** - FastAPI, MySQL, API endpoints
7. **Frontend Implementation** - React, visualizations, UI
8. **AI Integration** - LangChain, intent routing, capabilities
9. **Data Flow** - How data moves through the system
10. **Key Features** - Dashboard, analytics, AI insights
11. **Demo/Screenshots** - What the system looks like
12. **Technical Challenges** - Problems solved
13. **Results/Achievements** - What was accomplished
14. **Future Scope** - Potential enhancements
15. **Thank You/Q&A** - Contact information

## Tone and Style
- Professional and technical
- Hackathon-appropriate (energetic, innovative)
- Clear and concise bullet points
- Visual diagrams where appropriate
- Focus on technical implementation and results
- Highlight team collaboration and integration

## Data Points to Include
- 811 transactions processed
- 8 assets tracked
- 3 liabilities monitored
- 17 expense categories
- Health score: 83.2
- 12+ API endpoints
- Real-time data processing
- Intent-based AI routing
- Semantic search capabilities

## Target Audience
- Hackathon judges
- Technical evaluators
- Potential users
- Industry experts

Make the presentation impressive, technically accurate, and showcase the team's collaborative effort in building a complete end-to-end financial intelligence platform.
