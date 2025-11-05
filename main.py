"""Main entry point for unified backend + Telegram bot service

Runs both FastAPI backend and Telegram bot simultaneously
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def run_fastapi_server():
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
    await server.serve()


async def run_telegram_bot():
    """Run Telegram bot"""
    # Only start Telegram bot if TELEGRAM_TOKEN is configured
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    
    if not telegram_token:
        logger.warning("⚠️ TELEGRAM_TOKEN not configured. Skipping Telegram bot.")
        # Keep running to avoid exiting
        while True:
            await asyncio.sleep(3600)
        return
    
    logger.info("🤖 Starting Telegram Bot...")
    
    from integrations.telegram_bot import main as telegram_main
    
    # Run telegram bot
    await telegram_main()


async def main():
    """Main function to run both services"""
    logger.info("="*50)
    logger.info("🧠 CEREBRO AI - Unified Service Starting")
    logger.info("="*50)
    
    # Check if we should run both or just FastAPI
    run_telegram = os.environ.get("TELEGRAM_TOKEN") is not None
    
    if run_telegram:
        logger.info("📡 Mode: FastAPI + Telegram Bot")
        # Create tasks for both services to run concurrently
        fastapi_task = asyncio.create_task(run_fastapi_server())
        telegram_task = asyncio.create_task(run_telegram_bot())
        
        # Wait for both tasks (they should run forever)
        await asyncio.gather(fastapi_task, telegram_task)
    else:
        logger.info("📡 Mode: FastAPI Only (no TELEGRAM_TOKEN)")
        # Run only FastAPI
        await run_fastapi_server()


if __name__ == "__main__":
    
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
