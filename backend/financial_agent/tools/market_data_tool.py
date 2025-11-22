# tools/market_data_tool.py
import requests
from pydantic import BaseModel
from crewai.tools import BaseTool
from ..config import FMP_API_KEY


class MarketDataInput(BaseModel):
    ticker: str


class MarketDataTool(BaseTool):
    name: str = "market_data_tool"
    description: str = "Fetches fundamentals, ratios, financials, balance sheet, cash flow."

    args_schema: type[BaseModel] = MarketDataInput

    def _run(self, ticker: str):
        t = ticker.upper()

        def api(path):
            return f"https://financialmodelingprep.com/api/v3/{path}/{t}?apikey={FMP_API_KEY}"

        profile   = requests.get(api("profile")).json()
        ratios    = requests.get(api("ratios")).json()
        income    = requests.get(api("income-statement?limit=4")).json()
        balance   = requests.get(api("balance-sheet-statement?limit=4")).json()
        cashflow  = requests.get(api("cash-flow-statement?limit=4")).json()

        return {
            "ticker": t,
            "profile": profile,
            "ratios": ratios,
            "income": income,
            "balance": balance,
            "cashflow": cashflow
        }
