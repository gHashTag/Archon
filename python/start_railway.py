#!/usr/bin/env python3
"""
Railway startup wrapper that handles PORT environment variable correctly.
This ensures uvicorn always gets the correct port from Railway.
"""
import os
import subprocess
import sys

def main():
    # Get PORT from Railway (Railway always sets this)
    port = os.getenv("PORT", "8080")

    print(f"🚀 Starting Archon on Railway...")
    print(f"📍 Port: {port}")
    print(f"🐍 Python: {sys.executable}")

    # Build uvicorn command
    cmd = [
        sys.executable,  # Use current Python interpreter
        "-m", "uvicorn",
        "src.server.main:app",
        "--host", "0.0.0.0",
        "--port", port,
    ]

    print(f"🔧 Command: {' '.join(cmd)}")

    # Execute uvicorn (replace current process)
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    main()
