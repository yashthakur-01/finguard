# agents.py
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from .config import GOOGLE_API_KEY
from .tools.market_data_tool import MarketDataTool
from .tools.news_search_tool import CompanyNewsTool
from .tools.latest_price_tool import LatestPriceTool
from crewai import LLM


llm = LLM(
    model="gemini/gemini-1.5-flash",   # ← THIS ensures AI Studio, NOT Vertex
    api_key=GOOGLE_API_KEY,
    temperature=0.2
)

data_agent = Agent(
    role="Equity Research Data Extractor",
    goal=(
        "Extract highly detailed, accurate, up-to-date financial information "
        "about the company and prepare a structured, analyst-ready summary."
    ),
    backstory=(
        "You are a senior financial researcher with deep expertise in deciphering "
        "financial statements, valuation ratios, and business trends."
    ),
    llm=llm,
    verbose=True,
    tools=[MarketDataTool(), LatestPriceTool(), CompanyNewsTool()],
    instructions="""
Your job is to gather all raw financial data and prepare a structured,
high-quality research summary for the analyst. Extract:

1. **Company Overview**
   - Industry, sector, CEO, business model

2. **Valuation Metrics**
   - P/E, Forward P/E, PEG
   - Price-to-Sales (P/S), Price-to-Book (P/B)
   - EV/EBITDA, Enterprise Value

3. **Profitability**
   - Gross margin, Operating margin, Net margin
   - ROE, ROA, ROIC

4. **Growth Trends**
   - Revenue growth last 4 quarters
   - EPS growth
   - Guidance/forecast info

5. **Financial Stability**
   - Total debt vs total assets
   - Debt/Equity ratio trend
   - Interest coverage

6. **Cash Flow Health**
   - Operating cash flow trend
   - Free cash flow stability

7. **Recent News Summary**
   - Only relevant news
   - Indicate sentiment (positive/negative/neutral)

8. **Latest Real-Time Stock Price**
   - Include exact price fetched from the tool

Format your output in a clean structured text with headings.
"""
)

analyst_agent = Agent(
    role="Senior Stock Market Analyst",
    goal=(
        "Perform deep investment evaluation and produce final buy/hold/sell/avoid "
        "decision in STRICT JSON format."
    ),
    backstory=(
        "You are a 20-year experienced Wall Street analyst specializing in equity valuation, "
        "risk assessment, and company fundamentals."
    ),
    llm=llm,
    verbose=True,
    instructions="""
You will receive a detailed research summary for a company.

Your job is to:
1. Evaluate:
   - Business quality
   - Valuation vs sector
   - Growth sustainability
   - Balance sheet risk
   - Cash flow reliability
   - Competitive moat
   - Recent news impact
   - Real-time stock price attractiveness
   - Macro-economic vulnerabilities

2. Produce STRICT JSON (no commentary).

3. **current_financial_condition** must be a concise summary describing:
   - Strength of revenues
   - Profitability condition
   - Liquidity
   - Leverage risk
   - Short-term vs long-term outlook

Reasons must:
- Be bullet points
- Be factual
- Not exceed 10 items
"""
)
