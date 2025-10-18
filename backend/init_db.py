"""
Database initialization script
Runs migrations on application startup
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')


async def initialize_database():
    """Initialize database with migrations"""
    try:
        from database.migrations import run_all_migrations
        
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME')
        
        if not mongo_url or not db_name:
            logger.error("❌ MONGO_URL and DB_NAME must be set")
            return False
        
        logger.info("🚀 Initializing database...")
        await run_all_migrations(mongo_url, db_name)
        logger.info("✅ Database initialization complete")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(initialize_database())
    exit(0 if success else 1)
