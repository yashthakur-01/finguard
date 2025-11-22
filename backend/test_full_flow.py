import sys
import os
import asyncio
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

# Load env
load_dotenv('.env')

from financial_agent.langchain_agent import run_analysis

def test():
    print("--- Testing Full Analysis Flow ---")
    
    # Test 1: M&M (Indian Stock)
    company = "Mahindra & Mahindra"
    ticker = "M&M.NS"
    print(f"\nAnalyzing: {company} ({ticker})")
    
    result = run_analysis(ticker, company)
    
    print("\n--- Result Keys ---")
    print(result.keys())
    
    print("\n--- Essential Data ---")
    print(f"Company: {result.get('company')}")
    print(f"Ticker: {result.get('ticker')}")
    print(f"Price: {result.get('current_stock_price')}")
    print(f"Decision: {result.get('decision')}")
    
    if result.get('company') == company and result.get('ticker') == ticker:
        print("\nSUCCESS: Company and Ticker are present in result.")
    else:
        print("\nFAILURE: Company or Ticker missing/mismatch.")

    if result.get('current_stock_price') and result.get('current_stock_price') != 'N/A':
         print("SUCCESS: Price is present.")
    else:
         print("WARNING: Price is N/A (might be expected if API fails, but check logs).")

if __name__ == "__main__":
    test()
