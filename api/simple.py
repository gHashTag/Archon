"""
Simplified FastAPI for Vercel - Testing if basic app works
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Archon Simple Test")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Simple FastAPI on Vercel works!"}

@app.get("/api/simple/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "service": "archon-simple",
        "vercel": True,
        "python": "3.9",
        "message": "If you see this, basic FastAPI works on Vercel!"
    })

@app.get("/api/simple/test")
async def test():
    return {
        "framework": "FastAPI",
        "deployment": "Vercel",
        "status": "working",
        "routes": len(app.routes)
    }
