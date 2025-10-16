"""
Vercel Serverless Initialization Middleware

Handles initialization for Vercel serverless functions where lifespan events don't work.
"""

import logging
import os
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Global flag to track if initialization is complete
_INITIALIZED = False
_INITIALIZATION_LOCK = False


async def initialize_for_vercel():
    """Initialize credentials and services for Vercel deployment."""
    global _INITIALIZED, _INITIALIZATION_LOCK

    # Check if already initialized
    if _INITIALIZED:
        return

    # Prevent concurrent initialization
    if _INITIALIZATION_LOCK:
        # Wait for other initialization to complete
        import asyncio
        for _ in range(50):  # Wait up to 5 seconds
            if _INITIALIZED:
                return
            await asyncio.sleep(0.1)
        logger.warning("Initialization timeout - proceeding anyway")
        return

    try:
        _INITIALIZATION_LOCK = True
        logger.info("🚀 Initializing for Vercel serverless...")

        # On Vercel, skip database credential loading - use only env vars
        # This avoids dependency on credentials table in Supabase
        logger.info("⏭️  Skipping database credentials (using env vars only)")

        # Validate that required env vars are present
        required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_KEY"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        logger.info("✅ Environment variables validated")

        # Initialize logging (minimal setup without credentials)
        from ..config.logfire_config import setup_logfire
        setup_logfire(service_name="archon-backend")
        logger.info("✅ Logging initialized")

        # Skip crawler initialization on Vercel
        logger.info("⏭️  Skipping crawler initialization (Vercel serverless)")

        # Skip prompt service on Vercel (may require DB access)
        logger.info("⏭️  Skipping prompt service (Vercel serverless)")

        _INITIALIZED = True
        logger.info("🎉 Vercel initialization complete!")

    except Exception as e:
        logger.error(f"❌ Failed to initialize for Vercel: {e}", exc_info=True)
        raise
    finally:
        _INITIALIZATION_LOCK = False


class VercelInitMiddleware(BaseHTTPMiddleware):
    """Middleware to ensure initialization happens before first request on Vercel."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Initialize on first request if running on Vercel."""
        is_vercel = os.getenv("VERCEL_DEPLOYMENT") == "1"

        if is_vercel and not _INITIALIZED:
            try:
                await initialize_for_vercel()
            except Exception as e:
                logger.error(f"Initialization failed: {e}")
                # Return 503 Service Unavailable if initialization fails
                return Response(
                    content=f"Service initialization failed: {str(e)}",
                    status_code=503,
                    media_type="text/plain",
                )

        # Process the request
        response = await call_next(request)
        return response
