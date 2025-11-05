42
"""Main entry point for unified backend + Telegram bot service

Runs both FastAPI backend and Telegram bot simultaneously using threading
"""
import os
import sys
import logging
import threading
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
57

logger = logging.getLogger(__name__)


def run_fastapi():
    """Run FastAPI/Uvicorn server"""
    import uvicorn
    from backend.ai_agent import app
    
    port = int(os.environ.get("PORT", 10000))
    host = "0.0.0.0"
    
    logger.info(f"🚀 Starting FastAPI on {host}:{port}")
    
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()


59
():
    """Run Telegram bot"""
    # Only start Telegram bot if TELEGRAM_TOKEN is configured
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    
    if not telegram_token:
        logger.warning("⚠️ TELEGRAM_TOKEN not configured. Skipping Telegram bot.")
        # Keep running to avoid exiting
        while True:
            import time
            time.sleep(3600)
        return
    
    logger.info("🤖 Starting Telegram Bot...")
    
    from integrations.telegram_bot import main as telegram_mai
    
    # Create a new event loop for this thread
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)n
    telegram_main()    


if __name__ == "__main__":
    logger.info("="*50)
    logger.info("🧠 CEREBRO AI - Unified Service Starting")
    logger.info("📡 Mode: FastAPI + Telegram Bot")
    logger.info("="*50)
    
    # Check if we should run both or just FastAPI
    run_telegram = os.environ.get("TELEGRAM_TOKEN") is not None
    
    if run_telegram:
        logger.info("🔎 Mode: FastAPI + Telegram Bot")
        # Start FastAPI in a separate thread
        fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Run Telegram bot in main thread (it needs the event loop)
        run_telegram_bot()
    else:
        logger.info("🔎 Mode: FastAPI Only (no TELEGRAM_TOKEN)")
        # Run only FastAPI
        run_fastapi()
