# utils.py - Simplified ticker lookup using LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from .config import GOOGLE_API_KEY

# Common company to ticker mappings as fallback
COMMON_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "disney": "DIS",
    "walmart": "WMT",
    "jpmorgan": "JPM",
    "visa": "V",
    "mastercard": "MA"
}

def get_ticker(company_name: str) -> str:
    """Get stock ticker for a company using LangChain with fallback"""
    # Try fallback first
    company_lower = company_name.lower().strip()
    if company_lower in COMMON_TICKERS:
        return COMMON_TICKERS[company_lower]
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            google_api_key=GOOGLE_API_KEY,
            temperature=0
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a financial expert. When given a company name, respond with ONLY the stock ticker symbol. For Indian companies, YOU MUST append '.NS' (e.g., RELIANCE.NS, TATAMOTORS.NS). For US companies, just the ticker (e.g., AAPL). Return ONLY the ticker string, nothing else."),
            ("human", "What is the stock ticker for {company}?")
        ])
        
        chain = prompt | llm
        result = chain.invoke({"company": company_name})
        
        # Extract ticker from response
        ticker = result.content.strip().upper()
        # Remove any extra text, keep only the ticker
        ticker = ticker.split()[0] if ticker else ""
        
        return ticker
        
    except Exception as e:
        print(f"Error getting ticker: {e}")
        return ""
