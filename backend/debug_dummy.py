import json
import ast
from pathlib import Path

dummy_file_path = Path('dummy.txt')

if not dummy_file_path.exists():
    print(f"Dummy data file not found at {dummy_file_path}")
else:
    try:
        with open(dummy_file_path, 'r') as f:
            content = f.read().strip()
            
        # Remove variable assignment if present
        if content.startswith("AA_api ="):
            content = content.replace("AA_api =", "", 1).strip()
        
        print(f"Content start: {content[:50]}")
        print(f"Content end: {content[-50:]}")

        # Parse the content
        try:
            raw_data = json.loads(content)
            print("Successfully parsed with json.loads")
        except json.JSONDecodeError as e:
            print(f"json.loads failed: {e}")
            try:
                raw_data = ast.literal_eval(content)
                print("Successfully parsed with ast.literal_eval")
            except Exception as e:
                print(f"ast.literal_eval failed: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
