from financial_agent.main import run_analysis
import json

try:
    result = run_analysis('AAPL', 'Apple')
    print(json.dumps(result, indent=2))
except Exception as e:
    import traceback
    print(f"Error: {e}")
    print(traceback.format_exc())
