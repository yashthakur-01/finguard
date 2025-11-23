import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

# Load env
load_dotenv('.env')

from financial_agent.langchain_agent import run_analysis

def test():
    print("--- Testing Full Analysis Flow ---")
    
    # Test 1: Apple (Should have metrics)
    company = "Apple"
    ticker = "AAPL"
    print(f"\nAnalyzing: {company} ({ticker})")
    
    result = run_analysis(ticker, company)
    
    print("\n--- Result Keys ---")
    print(result.keys())
    
    print("\n--- Analysis Result ---")
    print(f"Company: {result.get('company')}")
    print(f"Price: {result.get('current_stock_price')}")
    print(f"Green Score: {result.get('green_score')}")
    
    # Check if metrics were considered (indirectly checks if they were passed)
    print(f"Metrics Considered: {result.get('key_metrics_considered')}")
    
    # We can't easily check the intermediate 'essential_data' without modifying the code, 
    # but if the LLM mentions PE or ROE in 'key_metrics_considered' or 'reasons', it's a good sign.
    print(f"Reasons: {result.get('reasons')}")

if __name__ == "__main__":
    test()
