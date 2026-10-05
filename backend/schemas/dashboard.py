from pydantic import BaseModel


class DashboardResponse(BaseModel):
    income: float
    expenses: float
    savings: float
    savings_rate: float
    assets: float
    liabilities: float
    net_worth: float
    debt_to_income: float
    health_score: float
