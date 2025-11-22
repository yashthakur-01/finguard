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
    print("--- Testing Currency Flow ---")
    
    # Test 1: M&M (Indian Stock) -> Should be INR
    company = "Mahindra & Mahindra"
    ticker = "M&M.NS"
    print(f"\nAnalyzing: {company} ({ticker})")
    result = run_analysis(ticker, company)
    print(f"Currency: {result.get('currency')}")
    print(f"Price: {result.get('current_stock_price')}")
    
    # Test 2: Apple (US Stock) -> Should be USD
    company_us = "Apple"
    ticker_us = "AAPL"
    print(f"\nAnalyzing: {company_us} ({ticker_us})")
    result_us = run_analysis(ticker_us, company_us)
    print(f"Currency: {result_us.get('currency')}")
    print(f"Price: {result_us.get('current_stock_price')}")

if __name__ == "__main__":
    test()
