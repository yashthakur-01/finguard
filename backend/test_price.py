import sys
import os
import urllib.parse
import requests

# Add current directory to path
sys.path.append(os.getcwd())

from financial_agent.pure_tools import get_latest_price

def test():
    tickers = ["AAPL", "RELIANCE.NS", "M&M.NS"]
    
    for t in tickers:
        print(f"\nTesting Price for: {t}")
        data = get_latest_price(t)
        print(f"Result: {data}")

if __name__ == "__main__":
    test()
