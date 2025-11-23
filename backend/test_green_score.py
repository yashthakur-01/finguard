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
    print("--- Testing Green Score Flow ---")
    
    # Test 1: Tesla (Should have high green score)
    company = "Tesla"
    ticker = "TSLA"
    print(f"\nAnalyzing: {company} ({ticker})")
    result = run_analysis(ticker, company)
    print(f"Green Score: {result.get('green_score')}")
    print(f"Green Summary: {result.get('green_summary')}")
    
    # Test 2: Exxon (Should have lower green score or specific notes)
    company_oil = "Exxon Mobil"
    ticker_oil = "XOM"
    print(f"\nAnalyzing: {company_oil} ({ticker_oil})")
    result_oil = run_analysis(ticker_oil, company_oil)
    print(f"Green Score: {result_oil.get('green_score')}")
    print(f"Green Summary: {result_oil.get('green_summary')}")

if __name__ == "__main__":
    test()
