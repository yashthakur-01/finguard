import sys
import os
import yfinance as yf

def test_yfinance():
    tickers = ["AAPL", "RELIANCE.NS", "M&M.NS"]
    
    for t in tickers:
        print(f"\n--- Testing {t} with yfinance ---")
        try:
            ticker = yf.Ticker(t)
            info = ticker.info
            
            # Metrics we need:
            # PE Ratio
            pe = info.get('trailingPE') or info.get('forwardPE')
            # ROE
            roe = info.get('returnOnEquity')
            # Profit Margin
            margin = info.get('profitMargins')
            # Debt to Equity
            debt_equity = info.get('debtToEquity')
            # Sector
            sector = info.get('sector')
            
            print(f"PE: {pe}")
            print(f"ROE: {roe}")
            print(f"Margin: {margin}")
            print(f"Debt/Equity: {debt_equity}")
            print(f"Sector: {sector}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_yfinance()
