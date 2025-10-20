#!/bin/bash
set -e

echo "🚀 Starting Archon on Railway..."
echo "📍 PORT: ${PORT:-8080}"
echo "🌍 PYTHONPATH: $PYTHONPATH"
echo "🐍 Python: $(which python)"

# Use PORT from Railway environment or default to 8080
export APP_PORT="${PORT:-8080}"

echo "🔧 Starting uvicorn on 0.0.0.0:$APP_PORT"

# Start uvicorn
exec /app/.venv/bin/python -m uvicorn src.server.main:app \
    --host 0.0.0.0 \
    --port "$APP_PORT"
