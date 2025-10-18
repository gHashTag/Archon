"""
Vercel serverless adapter for Archon FastAPI backend
"""
import os
import sys
import traceback
from pathlib import Path

# Add python directory to path
python_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(python_dir))

print(f"[Vercel] Python path configured: {python_dir}")
print(f"[Vercel] Python version: {sys.version}")

# Set environment variable to indicate Vercel deployment
os.environ["VERCEL_DEPLOYMENT"] = "1"

# Import and export the FastAPI app
# Vercel automatically handles ASGI apps
try:
    print("[Vercel] Importing FastAPI app...")
    from src.server.main import app
    print(f"[Vercel] ✅ App loaded successfully with {len(app.routes)} routes")
except Exception as e:
    print(f"[Vercel] ❌ FATAL ERROR loading app:")
    print(f"[Vercel] Error type: {type(e).__name__}")
    print(f"[Vercel] Error message: {str(e)}")
    print(f"[Vercel] Traceback:")
    traceback.print_exc()

    # Create a minimal error app
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Server initialization failed",
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        )
