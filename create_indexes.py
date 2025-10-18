#!/usr/bin/env python3
"""
Script to create MongoDB indexes for performance optimization
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'social_media_agent')

async def create_indexes():
    """Create indexes for all collections"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔍 Creating MongoDB indexes for performance optimization...\n")
    
    indexes_created = 0
    
    # Products collection
    print("📦 Products collection:")
    await db.products.create_index([("user_email", 1)])
    await db.products.create_index([("category", 1)])
    await db.products.create_index([("is_featured", 1)])
    await db.products.create_index([("created_at", -1)])
    await db.products.create_index([("user_email", 1), ("category", 1)])
    print("  ✅ Created 5 indexes")
    indexes_created += 5
    
    # Social posts collection
    print("📱 Social posts collection:")
    await db.social_posts.create_index([("user_email", 1)])
    await db.social_posts.create_index([("platform", 1)])
    await db.social_posts.create_index([("status", 1)])
    await db.social_posts.create_index([("created_at", -1)])
    await db.social_posts.create_index([("user_email", 1), ("created_at", -1)])
    print("  ✅ Created 5 indexes")
    indexes_created += 5
    
    # Campaigns collection
    print("📢 Campaigns collection:")
    await db.campaigns.create_index([("user_email", 1)])
    await db.campaigns.create_index([("status", 1)])
    await db.campaigns.create_index([("created_at", -1)])
    await db.campaigns.create_index([("user_email", 1), ("status", 1)])
    print("  ✅ Created 4 indexes")
    indexes_created += 4
    
    # Payment transactions collection
    print("💰 Payment transactions collection:")
    await db.payment_transactions.create_index([("user_email", 1)])
    await db.payment_transactions.create_index([("session_id", 1)])
    await db.payment_transactions.create_index([("payment_status", 1)])
    await db.payment_transactions.create_index([("created_at", -1)])
    await db.payment_transactions.create_index([("user_email", 1), ("payment_status", 1)])
    print("  ✅ Created 5 indexes")
    indexes_created += 5
    
    # Affiliates collection
    print("🤝 Affiliates collection:")
    await db.affiliates.create_index([("email", 1)], unique=True)
    await db.affiliates.create_index([("unique_code", 1)], unique=True)
    await db.affiliates.create_index([("status", 1)])
    await db.affiliates.create_index([("created_at", -1)])
    print("  ✅ Created 4 indexes")
    indexes_created += 4
    
    # Affiliate links collection
    print("🔗 Affiliate links collection:")
    await db.affiliate_links.create_index([("affiliate_email", 1)])
    await db.affiliate_links.create_index([("product_id", 1)])
    await db.affiliate_links.create_index([("affiliate_email", 1), ("product_id", 1)])
    print("  ✅ Created 3 indexes")
    indexes_created += 3
    
    # Affiliate commissions collection
    print("💵 Affiliate commissions collection:")
    await db.affiliate_commissions.create_index([("affiliate_email", 1)])
    await db.affiliate_commissions.create_index([("created_at", -1)])
    await db.affiliate_commissions.create_index([("affiliate_email", 1), ("created_at", -1)])
    print("  ✅ Created 3 indexes")
    indexes_created += 3
    
    # Subscriptions collection
    print("⭐ Subscriptions collection:")
    await db.subscriptions.create_index([("user_email", 1)])
    await db.subscriptions.create_index([("status", 1)])
    await db.subscriptions.create_index([("stripe_subscription_id", 1)])
    await db.subscriptions.create_index([("user_email", 1), ("status", 1)])
    print("  ✅ Created 4 indexes")
    indexes_created += 4
    
    # Analytics events collection
    print("📊 Analytics events collection:")
    await db.analytics_events.create_index([("user_email", 1)])
    await db.analytics_events.create_index([("session_id", 1)])
    await db.analytics_events.create_index([("event_type", 1)])
    await db.analytics_events.create_index([("created_at", -1)])
    await db.analytics_events.create_index([("user_email", 1), ("event_type", 1)])
    await db.analytics_events.create_index([("created_at", -1), ("event_type", 1)])
    print("  ✅ Created 6 indexes")
    indexes_created += 6
    
    # Notifications collection
    print("🔔 Notifications collection:")
    await db.notifications.create_index([("user_email", 1)])
    await db.notifications.create_index([("is_read", 1)])
    await db.notifications.create_index([("created_at", -1)])
    await db.notifications.create_index([("user_email", 1), ("is_read", 1)])
    await db.notifications.create_index([("user_email", 1), ("created_at", -1)])
    print("  ✅ Created 5 indexes")
    indexes_created += 5
    
    # User interactions collection (recommendations)
    print("👤 User interactions collection:")
    await db.user_interactions.create_index([("user_email", 1)])
    await db.user_interactions.create_index([("product_id", 1)])
    await db.user_interactions.create_index([("interaction_type", 1)])
    await db.user_interactions.create_index([("created_at", -1)])
    await db.user_interactions.create_index([("user_email", 1), ("product_id", 1)])
    await db.user_interactions.create_index([("user_email", 1), ("created_at", -1)])
    print("  ✅ Created 6 indexes")
    indexes_created += 6
    
    # Product embeddings collection
    print("🧠 Product embeddings collection:")
    await db.product_embeddings.create_index([("product_id", 1)], unique=True)
    await db.product_embeddings.create_index([("updated_at", -1)])
    print("  ✅ Created 2 indexes")
    indexes_created += 2
    
    # Usage tracking collection (limits)
    print("📈 Usage tracking collection:")
    await db.usage_tracking.create_index([("user_email", 1)])
    await db.usage_tracking.create_index([("resource_type", 1)])
    await db.usage_tracking.create_index([("user_email", 1), ("resource_type", 1)])
    await db.usage_tracking.create_index([("period_start", 1)])
    print("  ✅ Created 4 indexes")
    indexes_created += 4
    
    print(f"\n✅ Successfully created {indexes_created} indexes!")
    print("🚀 Database queries will be significantly faster now.\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_indexes())
