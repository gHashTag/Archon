#!/usr/bin/env python3
"""
Test all critical imports that Vercel needs
"""
import sys
import os

os.environ['VERCEL_DEPLOYMENT'] = '1'
sys.path.insert(0, 'python')

print("Testing critical imports for Vercel...")
print("="*60)

errors = []

# Test 1: FastAPI and core
try:
    from src.server.main import app
    print("✅ FastAPI app imported successfully")
    print(f"   Routes: {len(app.routes)}")
except Exception as e:
    print(f"❌ Failed to import FastAPI app: {e}")
    errors.append(("FastAPI app", e))

# Test 2: Database
try:
    from src.server.config.database import supabase
    print("✅ Supabase client imported")
except Exception as e:
    print(f"❌ Failed to import Supabase: {e}")
    errors.append(("Supabase", e))

# Test 3: OpenAI
try:
    import openai
    print("✅ OpenAI imported")
except Exception as e:
    print(f"❌ Failed to import OpenAI: {e}")
    errors.append(("OpenAI", e))

# Test 4: PydanticAI
try:
    import pydantic_ai
    print("✅ PydanticAI imported")
except Exception as e:
    print(f"❌ Failed to import PydanticAI: {e}")
    errors.append(("PydanticAI", e))

# Test 5: Document processing
try:
    import PyPDF2
    import pdfplumber
    import docx
    print("✅ Document processors imported")
except Exception as e:
    print(f"❌ Failed to import document processors: {e}")
    errors.append(("Document processors", e))

# Test 6: Security
try:
    from jose import jwt
    import cryptography
    print("✅ Security libraries imported")
except Exception as e:
    print(f"❌ Failed to import security libraries: {e}")
    errors.append(("Security", e))

# Test 7: MCP
try:
    import mcp
    print("✅ MCP imported")
except Exception as e:
    print(f"❌ Failed to import MCP: {e}")
    errors.append(("MCP", e))

# Test 8: Utilities
try:
    import docker
    import asyncpg
    import structlog
    print("✅ Utilities imported")
except Exception as e:
    print(f"❌ Failed to import utilities: {e}")
    errors.append(("Utilities", e))

print("="*60)

if errors:
    print(f"\n❌ FAILED: {len(errors)} import errors found:")
    for name, error in errors:
        print(f"   - {name}: {error}")
    sys.exit(1)
else:
    print("\n✅ SUCCESS: All critical imports working!")
    print("App should work on Vercel.")
    sys.exit(0)
