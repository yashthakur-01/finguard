# tools/latest_price_tool.py
import requests
from pydantic import BaseModel
from crewai.tools import BaseTool
from config import FMP_API_KEY


class LatestPriceInput(BaseModel):
    ticker: str


class LatestPriceTool(BaseTool):
    name = "latest_price_tool"
    description = "Fetches the latest real-time stock price using FMP quote API."

    args_schema = LatestPriceInput

    def _run(self, ticker: str):
        ticker = ticker.upper().strip()
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10).json()

        if not response or isinstance(response, dict):
            return {"ticker": ticker, "price": None}

        price = response[0].get("price")
        return {"ticker": ticker, "price": price}
