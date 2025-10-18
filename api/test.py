"""
Minimal FastAPI test for Vercel
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
@app.get("/api/test")
async def test():
    return JSONResponse({
        "status": "ok",
        "message": "Minimal FastAPI works on Vercel!",
        "python_version": "3.9.x",
        "framework": "FastAPI"
    })

@app.get("/api/test/health")
async def health():
    return {"status": "healthy", "test": True}
