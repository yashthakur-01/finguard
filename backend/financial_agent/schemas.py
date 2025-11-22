# schemas.py
from pydantic import BaseModel
from typing import List, Literal

Decision = Literal["strong_buy", "buy", "hold", "sell", "avoid"]
Risk = Literal["low", "medium", "high"]

class StockDecision(BaseModel):
    company: str
    ticker: str
    current_stock_price: float
    decision: Decision
    time_horizon: str
    risk_level: Risk
    current_financial_condition: str           # NEW FIELD
    reasons: List[str]
    key_metrics_considered: List[str]
