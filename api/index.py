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

# Import the FastAPI app
from src.server.main import app

# Vercel serverless function handler
async def handler(request):
    """Handle incoming requests via ASGI"""
    from mangum import Mangum
    asgi_handler = Mangum(app, lifespan="off")
    return await asgi_handler(request, None)
