"""
Vercel serverless adapter for Archon FastAPI backend
"""
import os
import sys
from pathlib import Path

# Add python directory to path
python_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(python_dir))

# Set environment variable to indicate Vercel deployment
os.environ["VERCEL_DEPLOYMENT"] = "1"

# Import and export the FastAPI app
# Vercel automatically handles ASGI apps
from src.server.main import app
