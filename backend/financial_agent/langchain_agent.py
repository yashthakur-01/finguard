# Simplified LangChain implementation using chains
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from .config import GOOGLE_API_KEY
from .pure_tools import get_market_data, get_latest_price, get_company_news
import json

# Initialize LLM - using flash model for lower token usage
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.15
)

def run_analysis(ticker: str, company_name: str) -> dict:
    """Run financial analysis using LangChain chains"""
    try:
        # Step 1: Gather data
        market_data = get_market_data(ticker)
        price_data = get_latest_price(ticker)
        news_data = get_company_news(company_name)
        
        # Extract only essential data to reduce tokens
        price = price_data.get("price", "N/A")
        currency = price_data.get("currency", "USD")
        
        # Safely extract market data (handle different structures)
        profile_data = market_data.get("profile", [])
        if isinstance(profile_data, list) and len(profile_data) > 0:
            profile = profile_data[0]
        elif isinstance(profile_data, dict):
            profile = profile_data
        else:
            profile = {}
        
        ratios_data = market_data.get("ratios", [])
        if isinstance(ratios_data, list) and len(ratios_data) > 0:
            ratios = ratios_data[0]
        elif isinstance(ratios_data, dict):
            ratios = ratios_data
        else:
            ratios = {}
        
        essential_data = {
            "company": profile.get("companyName", company_name),
            "sector": profile.get("sector", "N/A"),
            "price": price,
            "pe_ratio": ratios.get("priceEarningsRatio", "N/A"),
            "debt_to_equity": ratios.get("debtEquityRatio", "N/A"),
            "roe": ratios.get("returnOnEquity", "N/A"),
            "profit_margin": ratios.get("netProfitMargin", "N/A")
        }
        
        # Get only first 3 news items
        news_items = news_data.get("news_results", {}).get("news", [])[:3] if isinstance(news_data.get("news_results"), dict) else []
        
        # Step 2: Create concise analysis prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a stock analyst. Analyze the data and respond with ONLY valid JSON (no markdown, no extra text):
{{
  "decision": "BUY|HOLD|SELL",
  "current_stock_price": "{price}",
  "risk_level": "LOW|MEDIUM|HIGH",
  "time_horizon": "SHORT_TERM|MEDIUM_TERM|LONG_TERM",
  "current_financial_condition": "brief summary",
  "reasons": ["reason1", "reason2", "reason3"],
  "key_metrics_considered": ["metric1", "metric2"]
}}"""),
            ("human", """Analyze {company} ({ticker}):
Price: ${price}
PE: {pe}, ROE: {roe}%, Margin: {margin}%
Debt/Equity: {debt}
Sector: {sector}
Recent news: {news}

Provide JSON analysis:""")
        ])
        
        # Step 3: Run analysis
        chain = prompt | llm
        result = chain.invoke({
            "company": company_name,
            "ticker": ticker,
            "price": price,
            "pe": essential_data.get("pe_ratio", "N/A"),
            "roe": essential_data.get("roe", "N/A"),
            "margin": essential_data.get("profit_margin", "N/A"),
            "debt": essential_data.get("debt_to_equity", "N/A"),
            "sector": essential_data.get("sector", "N/A"),
            "news": str(news_items[:2]) if news_items else "No recent news"
        })
        
        # Step 4: Parse output
        output = result.content
        print(f"LLM Output: {output}")  # Debug logging
        
        # Extract JSON from the output
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = output[start_idx:end_idx]
            try:
                analysis_result = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"JSON string: {json_str}")
                # Fallback
                analysis_result = {
                    "decision": "HOLD",
                    "current_stock_price": str(price),
                    "risk_level": "MEDIUM",
                    "time_horizon": "MEDIUM_TERM",
                    "current_financial_condition": "Unable to parse LLM response",
                    "reasons": ["JSON parsing failed"],
                    "key_metrics_considered": []
                }
        else: # If no valid JSON block is found
            analysis_result = {
                "decision": "HOLD",
                "current_stock_price": str(price),
                "risk_level": "MEDIUM",
                "time_horizon": "MEDIUM_TERM",
                "current_financial_condition": "LLM response did not contain valid JSON",
                "reasons": ["LLM response format error"],
                "key_metrics_considered": []
            }
        
        # Add metadata to result
        analysis_result["company"] = company_name
        analysis_result["ticker"] = ticker
        analysis_result["currency"] = currency
        
        return analysis_result
        
    except Exception as e:
        import traceback
        print(f"Error in run_analysis: {e}")
        print(traceback.format_exc())
        return {
            "error": str(e),
            "company": company_name,
            "ticker": ticker
        }
