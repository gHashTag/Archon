"""
Vercel serverless adapter for Archon FastAPI backend
"""
import sys
from pathlib import Path

# Add python directory to path
python_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(python_dir))

# Import the FastAPI app
from src.server.main import app

# Export for Vercel
handler = app
