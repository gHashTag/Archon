#!/usr/bin/env python3
"""
Script to properly encrypt and add OpenAI API key to Supabase.
Uses the same Fernet encryption as credential_service.
"""
import os
import base64
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / ".env")


def get_encryption_key() -> bytes:
    """Generate encryption key from SUPABASE_SERVICE_KEY (same as credential_service)."""
    service_key = os.getenv("SUPABASE_SERVICE_KEY", "default-key-for-development")

    # Generate a proper encryption key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"static_salt_for_credentials",
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(service_key.encode()))
    return key


def encrypt_value(value: str) -> str:
    """Encrypt a sensitive value using Fernet encryption."""
    fernet = Fernet(get_encryption_key())
    encrypted_bytes = fernet.encrypt(value.encode("utf-8"))
    return base64.urlsafe_b64encode(encrypted_bytes).decode("utf-8")


async def main():
    from src.server.utils import get_supabase_client

    # OpenAI API key from .env
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env")
        return

    print(f"🔑 Found OpenAI API key: {openai_key[:10]}...")

    # Encrypt the key
    encrypted_key = encrypt_value(openai_key)
    print(f"🔐 Encrypted key: {encrypted_key[:30]}...")

    # Update in database
    supabase = get_supabase_client()
    result = supabase.table("archon_settings").update({
        "encrypted_value": encrypted_key,
        "is_encrypted": True
    }).eq("key", "OPENAI_API_KEY").execute()

    print(f"✅ OpenAI API key successfully encrypted and saved to Supabase!")
    print(f"   Rows updated: {len(result.data)}")

    # Verify
    verify = supabase.table("archon_settings").select("key, is_encrypted").eq("key", "OPENAI_API_KEY").execute()
    if verify.data:
        print(f"✅ Verification: {verify.data[0]}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
