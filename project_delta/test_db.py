
import sys
from pathlib import Path

# Add the src directory to sys.path so we can import models and database
sys.path.append("/app/projects/project_delta/src")

try:
    from database import init_db
    from models import Category, Product
    print("Import successful.")
    
    print("Initializing Database via SQLModel...")
    init_db()
    print("Database initialized successfully.")
    print("Models verified.")
except Exception as e:
    print(f"Error encountered: {e}")
    import traceback
    traceback.print_exc()
