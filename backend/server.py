from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import random
import json
import ast
from financial_agent.main import run_analysis
from financial_agent.utils import get_ticker

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class Transaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: str
    amount: float
    type: str  # income or expense
    mode: str  # cash, card, upi, bank_transfer
    category: str
    subCategory: str
    merchant: str
    tags: List[str] = []
    taxFlags: List[str] = []  # 80C, 80D, 80G, HRA
    narration: str
    isHighValue: bool = False

# Seed dummy data
async def seed_transactions():
    dummy_file_path = ROOT_DIR / 'dummy.txt'
    if not dummy_file_path.exists():
        print(f"Dummy data file not found at {dummy_file_path}")
        return

    try:
        with open(dummy_file_path, 'r') as f:
            content = f.read().strip()
            
        # Remove variable assignment if present
        if content.startswith("AA_api ="):
            content = content.replace("AA_api =", "", 1).strip()
        
        # Parse the content
        try:
            raw_data = json.loads(content)
        except json.JSONDecodeError:
            try:
                raw_data = ast.literal_eval(content)
            except Exception as e:
                print(f"Failed to parse dummy data: {e}")
                return

        transactions = []
        
        for item in raw_data:
            # Transform data to match Transaction model
            
            # Map type
            txn_type = "income" if item.get("type") == "CREDIT" else "expense"
            
            # Map mode
            mode = item.get("mode", "").lower()
            
            # Map tax flags
            tax_flags = []
            raw_flags = item.get("taxFlags", {})
            if isinstance(raw_flags, dict):
                if raw_flags.get("is80C"): tax_flags.append("80C")
                if raw_flags.get("is80D"): tax_flags.append("80D")
                if raw_flags.get("is80G"): tax_flags.append("80G")
                if raw_flags.get("isHRA"): tax_flags.append("HRA")
            
            # Map tags
            tags = item.get("tags", [])
            
            # Create transaction object
            txn = {
                "id": item.get("txnId", str(uuid.uuid4())),
                "date": item.get("date"),
                "amount": float(item.get("amount", 0)),
                "type": txn_type,
                "mode": mode,
                "category": item.get("category", "Uncategorized"),
                "subCategory": item.get("subCategory", "General"),
                "merchant": item.get("merchant", "Unknown"),
                "tags": tags,
                "taxFlags": tax_flags,
                "narration": item.get("narration", ""),
                "isHighValue": item.get("isHighValue", False)
            }
            transactions.append(txn)

        if transactions:
            # Clear existing data to ensure we have the exact dummy set
            await db.transactions.delete_many({})
            await db.transactions.insert_many(transactions)
            print(f"Seeded {len(transactions)} transactions from dummy.txt")
            
    except Exception as e:
        print(f"Error seeding transactions: {e}")

@app.on_event("startup")
async def startup_event():
    await seed_transactions()

# API Routes
@api_router.get("/transactions", response_model=List[Transaction])
async def get_transactions(
    type: Optional[str] = None,
    mode: Optional[str] = None,
    category: Optional[str] = None,
    taxEligible: Optional[bool] = None,
    highValue: Optional[bool] = None,
    search: Optional[str] = None
):
    query = {}
    
    if type:
        query["type"] = type
    if mode:
        query["mode"] = mode
    if category:
        query["category"] = category
    if taxEligible is not None:
        query["taxFlags"] = {"$ne": []} if taxEligible else []
    if highValue is not None:
        query["isHighValue"] = highValue
    if search:
        query["$or"] = [
            {"merchant": {"$regex": search, "$options": "i"}},
            {"narration": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]
    
    transactions = await db.transactions.find(query, {"_id": 0}).sort("date", -1).to_list(1000)
    return transactions

@api_router.get("/analytics/summary")
async def get_summary():
    transactions = await db.transactions.find({}, {"_id": 0}).to_list(10000)
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    net_cash_flow = total_income - total_expenses
    high_value_count = len([t for t in transactions if t["isHighValue"]])
    
    return {
        "totalIncome": round(total_income, 2),
        "totalExpenses": round(total_expenses, 2),
        "netCashFlow": round(net_cash_flow, 2),
        "highValueCount": high_value_count,
        "totalTransactions": len(transactions)
    }

@api_router.get("/analytics/category-summary")
async def get_category_summary():
    transactions = await db.transactions.find({"type": "expense"}, {"_id": 0}).to_list(10000)
    
    category_totals = {}
    for t in transactions:
        category = t["category"]
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += t["amount"]
    
    result = [{"category": k, "amount": round(v, 2)} for k, v in category_totals.items()]
    result.sort(key=lambda x: x["amount"], reverse=True)
    
    return result

@api_router.get("/analytics/monthly-summary")
async def get_monthly_summary():
    transactions = await db.transactions.find({}, {"_id": 0}).to_list(10000)
    
    monthly_data = {}
    for t in transactions:
        date = datetime.fromisoformat(t["date"])
        month_key = date.strftime("%Y-%m")
        
        if month_key not in monthly_data:
            monthly_data[month_key] = {"month": date.strftime("%b %Y"), "income": 0, "expenses": 0}
        
        if t["type"] == "income":
            monthly_data[month_key]["income"] += t["amount"]
        else:
            monthly_data[month_key]["expenses"] += t["amount"]
    
    result = list(monthly_data.values())
    result.sort(key=lambda x: x["month"])
    
    for item in result:
        item["income"] = round(item["income"], 2)
        item["expenses"] = round(item["expenses"], 2)
    
    return result

@api_router.get("/analytics/tax-summary")
async def get_tax_summary():
    transactions = await db.transactions.find({"taxFlags": {"$ne": []}}, {"_id": 0}).to_list(10000)
    
    tax_totals = {
        "80C": 0,
        "80D": 0,
        "80G": 0,
        "HRA": 0
    }
    
    tax_transactions = []
    
    for t in transactions:
        for flag in t["taxFlags"]:
            if flag in tax_totals:
                tax_totals[flag] += t["amount"]
        
        tax_transactions.append({
            "date": t["date"],
            "merchant": t["merchant"],
            "category": t["category"],
            "amount": t["amount"],
            "taxFlags": t["taxFlags"]
        })
    
    total_deductions = sum(tax_totals.values())
    
    return {
        "taxTotals": {k: round(v, 2) for k, v in tax_totals.items()},
        "totalDeductions": round(total_deductions, 2),
        "taxTransactions": tax_transactions
    }

@api_router.get("/analytics/spend-insights")
async def get_spend_insights():
    transactions = await db.transactions.find({"type": "expense"}, {"_id": 0}).to_list(10000)
    
    # Daily spend trend
    daily_spend = {}
    for t in transactions:
        date = datetime.fromisoformat(t["date"]).strftime("%Y-%m-%d")
        if date not in daily_spend:
            daily_spend[date] = 0
        daily_spend[date] += t["amount"]
    
    daily_trend = [{"date": k, "amount": round(v, 2)} for k, v in sorted(daily_spend.items())]
    
    # Weekly average
    total_spend = sum(t["amount"] for t in transactions)
    num_weeks = len(daily_spend) / 7 if daily_spend else 1
    weekly_average = total_spend / num_weeks if num_weeks > 0 else 0
    
    # Top categories
    category_totals = {}
    for t in transactions:
        category = t["category"]
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += t["amount"]
    
    top_categories = sorted(
        [{"category": k, "amount": round(v, 2)} for k, v in category_totals.items()],
        key=lambda x: x["amount"],
        reverse=True
    )[:5]
    
    # Top merchants
    merchant_totals = {}
    for t in transactions:
        merchant = t["merchant"]
        if merchant not in merchant_totals:
            merchant_totals[merchant] = 0
        merchant_totals[merchant] += t["amount"]
    
    top_merchants = sorted(
        [{"merchant": k, "amount": round(v, 2)} for k, v in merchant_totals.items()],
        key=lambda x: x["amount"],
        reverse=True
    )[:5]
    
    # High spend alerts (days with spending > 5000)
    high_spend_days = [item for item in daily_trend if item["amount"] > 5000]
    
    return {
        "dailyTrend": daily_trend,
        "weeklyAverage": round(weekly_average, 2),
        "topCategories": top_categories,
        "topMerchants": top_merchants,
        "highSpendAlerts": high_spend_days
    }

class AnalysisRequest(BaseModel):
    company_name: str

@api_router.post("/financial-analysis")
async def financial_analysis(request: AnalysisRequest):
    try:
        # Get ticker
        ticker = get_ticker(request.company_name)
        if not ticker:
             return {"error": "Could not find ticker symbol"}
        
        # Run analysis
        import asyncio
        from functools import partial
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, partial(run_analysis, ticker, request.company_name))
        
        return result
    except Exception as e:
        logger.error(f"Error in financial analysis: {e}")
        return {"error": str(e)}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()