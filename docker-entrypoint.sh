#!/bin/bash
set -e

echo "🚀 Starting Archon on Railway..."
echo "📍 PORT: ${PORT:-8080}"
echo "🌍 PYTHONPATH: $PYTHONPATH"
echo "🐍 Python: $(which python)"

# Diagnostic: Check frontend dist
echo ""
echo "🔍 Frontend Diagnostic:"
echo "📁 Checking /app/frontend/dist..."
if [ -d "/app/frontend/dist" ]; then
    echo "✅ /app/frontend/dist EXISTS"
    echo "📄 Files in dist:"
    ls -la /app/frontend/dist/ | head -10
else
    echo "❌ /app/frontend/dist NOT FOUND"
    echo "📁 Checking /app/frontend:"
    ls -la /app/frontend/ 2>&1 | head -10 || echo "❌ /app/frontend not found"
fi
echo ""

# Use PORT from Railway environment or default to 8080
export APP_PORT="${PORT:-8080}"

echo "🔧 Starting uvicorn on 0.0.0.0:$APP_PORT"

# Start uvicorn
exec /app/.venv/bin/python -m uvicorn src.server.main:app \
    --host 0.0.0.0 \
    --port "$APP_PORT"
