# main.py
from crew import create_stock_crew
import json

def run_analysis(ticker: str, company_name: str):
    crew = create_stock_crew()
    result = crew.kickoff(
        inputs={"ticker": ticker, "company_name": company_name}
    )
    return result.to_dict()

if __name__ == "__main__":
    ticker = input("Ticker: ")
    name = input("Company Name: ")

    output = run_analysis(ticker, name)
    print(json.dumps(output, indent=2))
