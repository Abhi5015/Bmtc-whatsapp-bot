"""
BMTC WhatsApp Bot - Main Application
FastAPI server with Twilio WhatsApp integration
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from config import config
from app.whatsapp_webhook import whatsapp_webhook

# -------------------------------------------------
# Ensure logs directory exists
# -------------------------------------------------
os.makedirs("logs", exist_ok=True)

# -------------------------------------------------
# Logging configuration
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Application lifecycle
# -------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting BMTC WhatsApp Bot...")

    try:
        # ---- MISTRAL VALIDATION ----
        if not config.MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is missing")

        logger.info("✅ Mistral configuration loaded")
        logger.info(f"📌 Model: {config.MISTRAL_MODEL}")

        # ---- TWILIO VALIDATION ----
        if not config.TWILIO_ACCOUNT_SID or not config.TWILIO_AUTH_TOKEN:
            raise ValueError("Twilio credentials missing")

        logger.info("✅ Twilio credentials detected")
        logger.info("✅ Server ready to receive requests")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

    yield

    logger.info("🛑 Shutting down BMTC WhatsApp Bot...")

# -------------------------------------------------
# FastAPI app
# -------------------------------------------------
app = FastAPI(
    title="BMTC WhatsApp Bot",
    description="WhatsApp bot for BMTC bus information using Twilio + Mistral",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------------------------------
# Health endpoints
# -------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "BMTC WhatsApp Bot",
        "nlp_provider": "mistral",
        "model": config.MISTRAL_MODEL,
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mistral_model": config.MISTRAL_MODEL,
    }

# -------------------------------------------------
# WhatsApp webhook
# -------------------------------------------------
@app.post("/whatsapp")
async def whatsapp_endpoint(request: Request):
    logger.info("📩 Incoming WhatsApp webhook")
    return await whatsapp_webhook.handle_incoming_message(request)

@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    return await whatsapp_webhook.handle_status_callback(request)

# -------------------------------------------------
# Global error handler
# -------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

# -------------------------------------------------
# Entry point
# -------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {config.HOST}:{config.PORT}")

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=False,
        log_level="info",
    )
