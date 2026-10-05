from pydantic import BaseModel


class ExpenseItem(BaseModel):
    category: str
    amount: float
    percentage: float


class ExpenseResponse(BaseModel):
    expenses: list[ExpenseItem]
