import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend/.env
# Assuming this file is in backend/financial_agent/config.py
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
