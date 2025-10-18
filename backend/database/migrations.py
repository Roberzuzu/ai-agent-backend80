"""
Database Migration System
Handles database schema evolution, indexes, and validations
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure
from datetime import datetime, timezone
import os
import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class MigrationManager:
    """Manages database migrations, indexes, and schema validations"""
    
    def __init__(self, mongo_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        self.migrations_collection = self.db['_migrations']
    
    async def get_applied_migrations(self) -> List[str]:
        """Get list of already applied migration IDs"""
        cursor = self.migrations_collection.find({}, {'migration_id': 1})
        migrations = await cursor.to_list(length=None)
        return [m['migration_id'] for m in migrations]
    
    async def mark_migration_applied(self, migration_id: str, description: str):
        """Mark a migration as applied"""
        await self.migrations_collection.insert_one({
            'migration_id': migration_id,
            'description': description,
            'applied_at': datetime.now(timezone.utc)
        })
        logger.info(f"✅ Migration {migration_id} applied: {description}")
    
    async def create_indexes(self, collection_name: str, indexes: List[IndexModel]):
        """Create indexes for a collection"""
        collection = self.db[collection_name]
        try:
            result = await collection.create_indexes(indexes)
            logger.info(f"✅ Created {len(result)} indexes for {collection_name}")
            return result
        except Exception as e:
            logger.error(f"❌ Error creating indexes for {collection_name}: {e}")
            raise
    
    async def create_collection_with_validation(
        self, 
        collection_name: str, 
        validator: Dict[str, Any],
        validation_level: str = "strict",
        validation_action: str = "error"
    ):
        """Create collection with schema validation"""
        try:
            await self.db.create_collection(
                collection_name,
                validator=validator,
                validationLevel=validation_level,
                validationAction=validation_action
            )
            logger.info(f"✅ Created collection {collection_name} with validation")
        except CollectionInvalid:
            # Collection exists, update validation
            await self.db.command({
                'collMod': collection_name,
                'validator': validator,
                'validationLevel': validation_level,
                'validationAction': validation_action
            })
            logger.info(f"✅ Updated validation for {collection_name}")
        except Exception as e:
            logger.error(f"❌ Error creating collection {collection_name}: {e}")
            raise
    
    async def run_migration(self, migration_id: str, description: str, migration_func):
        """Run a migration if not already applied"""
        applied = await self.get_applied_migrations()
        
        if migration_id in applied:
            logger.info(f"⏭️  Skipping {migration_id} (already applied)")
            return False
        
        logger.info(f"🚀 Running migration {migration_id}: {description}")
        try:
            await migration_func(self.db)
            await self.mark_migration_applied(migration_id, description)
            return True
        except Exception as e:
            logger.error(f"❌ Migration {migration_id} failed: {e}")
            raise


# =========================
# MIGRATION DEFINITIONS
# =========================

async def migration_001_user_indexes(db):
    """Create indexes for users collection"""
    indexes = [
        IndexModel([("email", ASCENDING)], unique=True, name="email_unique"),
        IndexModel([("username", ASCENDING)], unique=True, name="username_unique"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
        IndexModel([("role", ASCENDING), ("is_active", ASCENDING)], name="role_active"),
    ]
    await db['users'].create_indexes(indexes)


async def migration_002_product_indexes(db):
    """Create indexes for products collection"""
    indexes = [
        IndexModel([("category", ASCENDING)], name="category"),
        IndexModel([("is_featured", ASCENDING)], name="is_featured"),
        IndexModel([("price", ASCENDING)], name="price"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
        IndexModel([("name", TEXT), ("description", TEXT)], name="text_search"),
    ]
    await db['products'].create_indexes(indexes)


async def migration_003_payment_indexes(db):
    """Create indexes for payment transactions"""
    indexes = [
        IndexModel([("user_email", ASCENDING)], name="user_email"),
        IndexModel([("payment_status", ASCENDING)], name="payment_status"),
        IndexModel([("session_id", ASCENDING)], unique=True, name="session_id_unique"),
        IndexModel([("user_email", ASCENDING), ("payment_status", ASCENDING)], name="user_status"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
        IndexModel([("payment_type", ASCENDING), ("payment_status", ASCENDING)], name="type_status"),
    ]
    await db['payment_transactions'].create_indexes(indexes)


async def migration_004_subscription_indexes(db):
    """Create indexes for subscriptions"""
    indexes = [
        IndexModel([("user_email", ASCENDING)], name="user_email"),
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("user_email", ASCENDING), ("status", ASCENDING)], name="user_status"),
        IndexModel([("stripe_subscription_id", ASCENDING)], unique=True, sparse=True, name="stripe_id_unique"),
        IndexModel([("current_period_end", ASCENDING)], name="period_end"),
    ]
    await db['subscriptions'].create_indexes(indexes)


async def migration_005_affiliate_indexes(db):
    """Create indexes for affiliate program"""
    # Affiliates
    affiliate_indexes = [
        IndexModel([("email", ASCENDING)], unique=True, name="email_unique"),
        IndexModel([("unique_code", ASCENDING)], unique=True, name="code_unique"),
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['affiliates'].create_indexes(affiliate_indexes)
    
    # Affiliate Links
    link_indexes = [
        IndexModel([("affiliate_id", ASCENDING)], name="affiliate_id"),
        IndexModel([("unique_code", ASCENDING)], unique=True, name="code_unique"),
        IndexModel([("product_id", ASCENDING)], sparse=True, name="product_id"),
        IndexModel([("affiliate_id", ASCENDING), ("product_id", ASCENDING)], name="affiliate_product"),
    ]
    await db['affiliate_links'].create_indexes(link_indexes)
    
    # Affiliate Commissions
    commission_indexes = [
        IndexModel([("affiliate_id", ASCENDING)], name="affiliate_id"),
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("affiliate_id", ASCENDING), ("status", ASCENDING)], name="affiliate_status"),
        IndexModel([("transaction_id", ASCENDING)], name="transaction_id"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['affiliate_commissions'].create_indexes(commission_indexes)
    
    # Affiliate Payouts
    payout_indexes = [
        IndexModel([("affiliate_id", ASCENDING)], name="affiliate_id"),
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("requested_at", DESCENDING)], name="requested_at_desc"),
    ]
    await db['affiliate_payouts'].create_indexes(payout_indexes)


async def migration_006_notification_indexes(db):
    """Create indexes for notifications"""
    indexes = [
        IndexModel([("user_email", ASCENDING)], name="user_email"),
        IndexModel([("is_read", ASCENDING)], name="is_read"),
        IndexModel([("user_email", ASCENDING), ("is_read", ASCENDING)], name="user_read"),
        IndexModel([("user_email", ASCENDING), ("created_at", DESCENDING)], name="user_created"),
        IndexModel([("type", ASCENDING)], name="type"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['notifications'].create_indexes(indexes)


async def migration_007_campaign_indexes(db):
    """Create indexes for campaigns"""
    indexes = [
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("platform", ASCENDING)], name="platform"),
        IndexModel([("start_date", ASCENDING), ("end_date", ASCENDING)], name="date_range"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['campaigns'].create_indexes(indexes)


async def migration_008_content_indexes(db):
    """Create indexes for content and trends"""
    # Content Ideas
    content_indexes = [
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("platform", ASCENDING)], name="platform"),
        IndexModel([("content_type", ASCENDING)], name="content_type"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['content_ideas'].create_indexes(content_indexes)
    
    # Trends
    trend_indexes = [
        IndexModel([("platform", ASCENDING)], name="platform"),
        IndexModel([("engagement_score", DESCENDING)], name="engagement_desc"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['trends'].create_indexes(trend_indexes)
    
    # Social Posts
    post_indexes = [
        IndexModel([("status", ASCENDING)], name="status"),
        IndexModel([("platform", ASCENDING)], name="platform"),
        IndexModel([("scheduled_time", ASCENDING)], sparse=True, name="scheduled_time"),
        IndexModel([("created_at", DESCENDING)], name="created_at_desc"),
    ]
    await db['social_posts'].create_indexes(post_indexes)


# =========================
# SCHEMA VALIDATIONS
# =========================

async def migration_100_user_validation(db):
    """Add schema validation for users"""
    validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['email', 'username', 'hashed_password', 'role'],
            'properties': {
                'email': {'bsonType': 'string', 'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'},
                'username': {'bsonType': 'string', 'minLength': 3, 'maxLength': 50},
                'role': {'enum': ['user', 'admin', 'affiliate']},
                'is_active': {'bsonType': 'bool'},
                'is_verified': {'bsonType': 'bool'},
            }
        }
    }
    await db.command({'collMod': 'users', 'validator': validator})


async def migration_101_payment_validation(db):
    """Add schema validation for payments"""
    validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['session_id', 'amount', 'payment_type', 'payment_status'],
            'properties': {
                'amount': {'bsonType': 'double', 'minimum': 0},
                'currency': {'enum': ['usd', 'eur', 'gbp']},
                'payment_type': {'enum': ['subscription', 'product', 'custom']},
                'payment_status': {'enum': ['pending', 'paid', 'failed', 'cancelled']},
                'status': {'enum': ['initiated', 'completed', 'failed']},
            }
        }
    }
    await db.command({'collMod': 'payment_transactions', 'validator': validator})


async def migration_102_affiliate_validation(db):
    """Add schema validation for affiliates"""
    validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['email', 'unique_code', 'commission_rate'],
            'properties': {
                'email': {'bsonType': 'string', 'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'},
                'unique_code': {'bsonType': 'string', 'minLength': 6, 'maxLength': 20},
                'commission_rate': {'bsonType': 'double', 'minimum': 0, 'maximum': 100},
                'status': {'enum': ['active', 'suspended', 'pending']},
                'total_earnings': {'bsonType': 'double', 'minimum': 0},
            }
        }
    }
    await db.command({'collMod': 'affiliates', 'validator': validator})


async def migration_103_notification_validation(db):
    """Add schema validation for notifications"""
    validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['user_email', 'type', 'title', 'message'],
            'properties': {
                'user_email': {'bsonType': 'string'},
                'type': {'enum': ['info', 'success', 'warning', 'error', 'payment', 'affiliate', 'campaign', 'product', 'subscription', 'system']},
                'title': {'bsonType': 'string', 'minLength': 1},
                'message': {'bsonType': 'string', 'minLength': 1},
                'is_read': {'bsonType': 'bool'},
                'is_archived': {'bsonType': 'bool'},
            }
        }
    }
    await db.command({'collMod': 'notifications', 'validator': validator})


# =========================
# MAIN MIGRATION RUNNER
# =========================

async def run_all_migrations(mongo_url: str, db_name: str):
    """Run all pending migrations"""
    manager = MigrationManager(mongo_url, db_name)
    
    migrations = [
        # Index migrations
        ("001", "User indexes", migration_001_user_indexes),
        ("002", "Product indexes", migration_002_product_indexes),
        ("003", "Payment transaction indexes", migration_003_payment_indexes),
        ("004", "Subscription indexes", migration_004_subscription_indexes),
        ("005", "Affiliate program indexes", migration_005_affiliate_indexes),
        ("006", "Notification indexes", migration_006_notification_indexes),
        ("007", "Campaign indexes", migration_007_campaign_indexes),
        ("008", "Content and trend indexes", migration_008_content_indexes),
        
        # Schema validation migrations
        ("100", "User schema validation", migration_100_user_validation),
        ("101", "Payment schema validation", migration_101_payment_validation),
        ("102", "Affiliate schema validation", migration_102_affiliate_validation),
        ("103", "Notification schema validation", migration_103_notification_validation),
    ]
    
    logger.info("=" * 60)
    logger.info("🚀 Starting database migrations...")
    logger.info("=" * 60)
    
    applied_count = 0
    for migration_id, description, migration_func in migrations:
        if await manager.run_migration(migration_id, description, migration_func):
            applied_count += 1
    
    logger.info("=" * 60)
    logger.info(f"✅ Migrations complete! Applied {applied_count} new migrations.")
    logger.info("=" * 60)
    
    # Close connection
    manager.client.close()


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    load_dotenv()
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    
    asyncio.run(run_all_migrations(mongo_url, db_name))
