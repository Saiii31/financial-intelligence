from pydantic import BaseModel


class TrendResponse(BaseModel):
    income_change: float
    expense_change: float
    savings_change: float
    top_spending_increase: dict
