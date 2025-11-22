import sys
import os
import urllib.parse
from dotenv import load_dotenv
import requests

# Add current directory to path
sys.path.append(os.getcwd())

# Load env
load_dotenv('.env')

from financial_agent.config import FMP_API_KEY
from financial_agent.pure_tools import get_market_data, get_latest_price

def test_fmp_direct(ticker):
    encoded_ticker = urllib.parse.quote(ticker)
    print(f"\nTesting FMP Direct for: '{ticker}' (Encoded: '{encoded_ticker}')")
    
    url = f"https://financialmodelingprep.com/api/v3/profile/{encoded_ticker}?apikey={FMP_API_KEY}"
    # print(f"URL: {url.replace(FMP_API_KEY, 'HIDDEN')}")
    
    try:
        resp = requests.get(url)
        data = resp.json()
        if isinstance(data, dict) and data.get("Error Message"):
             print(f"API Error: {data.get('Error Message')}")
        elif isinstance(data, list) and len(data) > 0:
            print(f"Success! Company: {data[0].get('companyName')}")
        else:
            print(f"Failed or empty. Response: {str(data)[:100]}")
    except Exception as e:
        print(f"Exception: {e}")

def test_tools(ticker):
    print(f"\n--- Testing Tools for {ticker} ---")
    
    # Market Data
    md = get_market_data(ticker)
    if "error" in md:
        print(f"get_market_data Error: {md['error']}")
    else:
        prof = md.get('profile', {})
        if isinstance(prof, list) and prof:
            print(f"Market Data Profile: Found {prof[0].get('companyName')}")
        elif isinstance(prof, dict) and prof.get("Error Message"):
             print(f"Market Data API Error: {prof.get('Error Message')}")
        else:
            print(f"Market Data Profile: {prof}")

    # Price
    pd = get_latest_price(ticker)
    print(f"Price Data: {pd}")

def test():
    # Test 1: US Stock (Should work)
    test_fmp_direct("AAPL")
    test_tools("AAPL")
    
    # Test 2: Indian Stock (Standard)
    test_fmp_direct("RELIANCE.NS")
    test_tools("RELIANCE.NS")
    
    # Test 3: Indian Stock with Special Char
    test_fmp_direct("M&M.NS")
    test_tools("M&M.NS")

if __name__ == "__main__":
    test()
