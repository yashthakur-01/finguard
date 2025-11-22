# Pure Python tools without CrewAI dependencies
import requests
import json
import urllib.parse
from .config import FMP_API_KEY, SERPER_API_KEY


def get_market_data(ticker: str) -> dict:
    """Fetch market data for a stock ticker using the Financial Modeling Prep API.
    Returns a dict with profile, ratios, income, balance, and cashflow data.
    """
    t = ticker.upper().strip()
    encoded_t = urllib.parse.quote(t)
    
    def api(path: str) -> str:
        return f"https://financialmodelingprep.com/api/v3/{path}/{encoded_t}?apikey={FMP_API_KEY}"
    try:
        profile = requests.get(api("profile")).json()
        ratios = requests.get(api("ratios")).json()
        income = requests.get(api("income-statement?limit=4")).json()
        balance = requests.get(api("balance-sheet-statement?limit=4")).json()
        cashflow = requests.get(api("cash-flow-statement?limit=4")).json()
        return {
            "ticker": t,
            "profile": profile,
            "ratios": ratios,
            "income": income,
            "balance": balance,
            "cashflow": cashflow,
        }
    except Exception as e:
        return {"error": str(e), "ticker": t}


def get_latest_price(ticker: str) -> dict:
    """Fetch the latest stock price using Yahoo Finance (free, no API key).
    Returns a dict with the price and the currency reported by Yahoo Finance.
    If the price cannot be retrieved, the function retries with a '.NS' suffix for Indian NSE symbols.
    """
    original = ticker.upper().strip()

    def fetch(tkr: str):
        encoded_tkr = urllib.parse.quote(tkr)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded_tkr}?interval=1d&range=1d"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(url, headers=headers, timeout=10).json()
            if resp and "chart" in resp and resp["chart"].get("result"):
                result = resp["chart"]["result"][0]
                price = result.get("meta", {}).get("regularMarketPrice")
                currency = result.get("meta", {}).get("currency")
                return price, currency
        except Exception:
            pass
        return None, None

    price, currency = fetch(original)
    if price is None and "." not in original:
        price, currency = fetch(f"{original}.NS")
    return {"ticker": original, "price": price, "currency": currency}


def get_company_news(company: str) -> dict:
    """Fetch recent news for a company using the Serper.dev news API.
    Returns a dict with the raw API response under the key "news_results".
    """
    try:
        url = "https://google.serper.dev/news"
        query = f"{company} latest stock news earnings updates"
        payload = json.dumps({"q": query})
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        result = response.json()
        return {"company": company, "news_results": result}
    except Exception as e:
        return {"error": str(e), "company": company}
