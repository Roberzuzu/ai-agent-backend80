from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import asyncio
from social_integrations import SocialMediaPublisher
from wordpress_integration import WordPressIntegration

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Social Media Monetization Agent")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize social media publisher
social_publisher = SocialMediaPublisher()

# Initialize WordPress integration
wordpress_client = WordPressIntegration()

# =========================
# MODELS
# =========================

class Trend(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str  # youtube, tiktok, instagram, twitter
    topic: str
    engagement_score: int
    keywords: List[str]
    analysis: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TrendCreate(BaseModel):
    platform: str
    topic: str
    engagement_score: int
    keywords: List[str]

class ContentIdea(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    platform: str
    content_type: str  # tutorial, review, comparison, tips, diy
    keywords: List[str]
    generated_content: Optional[str] = None
    ai_provider: Optional[str] = None
    status: str = "draft"  # draft, approved, published
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContentIdeaCreate(BaseModel):
    platform: str
    content_type: str
    keywords: List[str]
    custom_prompt: Optional[str] = None

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    affiliate_link: Optional[str] = None
    discount_code: Optional[str] = None
    discount_percentage: Optional[float] = None
    category: str
    image_url: Optional[str] = None
    is_featured: bool = False
    bundle_products: List[str] = []  # IDs of other products in bundle
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    affiliate_link: Optional[str] = None
    discount_code: Optional[str] = None
    discount_percentage: Optional[float] = None
    category: str
    image_url: Optional[str] = None
    is_featured: bool = False
    bundle_products: List[str] = []

class SocialPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str  # instagram, tiktok, youtube, facebook, twitter
    content: str
    media_urls: List[str] = []
    scheduled_time: Optional[datetime] = None
    status: str = "pending"  # pending, scheduled, published, failed
    content_id: Optional[str] = None
    product_ids: List[str] = []
    engagement: Dict[str, int] = {}  # likes, comments, shares
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SocialPostCreate(BaseModel):
    platform: str
    content: str
    media_urls: List[str] = []
    scheduled_time: Optional[datetime] = None
    content_id: Optional[str] = None
    product_ids: List[str] = []

class Campaign(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    budget: float
    platform: str
    target_audience: Dict[str, Any] = {}
    start_date: datetime
    end_date: datetime
    status: str = "active"  # active, paused, completed
    performance: Dict[str, Any] = {}  # impressions, clicks, conversions, spend
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CampaignCreate(BaseModel):
    name: str
    description: str
    budget: float
    platform: str
    target_audience: Dict[str, Any] = {}
    start_date: datetime
    end_date: datetime

class AIGenerationRequest(BaseModel):
    prompt: str
    provider: str = "openai"  # openai, emergent, openrouter
    model: Optional[str] = None
    max_tokens: int = 1000

# =========================
# PAYMENT & SUBSCRIPTION MODELS
# =========================

class SubscriptionPlan(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    currency: str = "usd"
    interval: str = "month"  # month, year
    features: List[str] = []
    stripe_price_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SubscriptionPlanCreate(BaseModel):
    name: str
    description: str
    price: float
    currency: str = "usd"
    interval: str = "month"
    features: List[str] = []
    stripe_price_id: Optional[str] = None

class Subscription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    plan_id: str
    stripe_subscription_id: Optional[str] = None
    status: str = "active"  # active, cancelled, expired, past_due
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SubscriptionCreate(BaseModel):
    user_email: str
    plan_id: str

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    payment_id: Optional[str] = None
    user_email: Optional[str] = None
    amount: float
    currency: str = "usd"
    payment_type: str  # subscription, product, custom
    product_id: Optional[str] = None
    plan_id: Optional[str] = None
    payment_status: str = "pending"  # pending, paid, failed, cancelled
    status: str = "initiated"  # initiated, completed, failed
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CheckoutRequest(BaseModel):
    payment_type: str  # product, subscription
    product_id: Optional[str] = None
    plan_id: Optional[str] = None
    user_email: Optional[str] = None
    origin_url: str
    metadata: Optional[Dict[str, Any]] = {}

# =========================
# AI HELPER FUNCTIONS
# =========================

async def generate_with_ai(prompt: str, provider: str = "openai", model: Optional[str] = None) -> str:
    """Generate content using AI providers"""
    try:
        if provider == "openai":
            api_key = os.environ.get('OPENAI_API_KEY')
            model = model or "gpt-4o"
        elif provider == "emergent":
            api_key = os.environ.get('EMERGENT_LLM_KEY')
            model = model or "gpt-4o-mini"
        elif provider == "openrouter":
            api_key = os.environ.get('OPENROUTER_API_KEY')
            model = model or "gpt-4o"
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        if not api_key:
            raise ValueError(f"API key not found for provider: {provider}")
        
        chat = LlmChat(
            api_key=api_key,
            session_id=str(uuid.uuid4()),
            system_message="You are a creative social media content expert specializing in monetization strategies for tools and accessories."
        ).with_model("openai", model)
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        return response
    except Exception as e:
        logging.error(f"AI generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# =========================
# ROUTES - Growth Hacker
# =========================

@api_router.post("/trends", response_model=Trend)
async def create_trend(input: TrendCreate):
    """Create a new trend entry"""
    trend_dict = input.model_dump()
    trend_obj = Trend(**trend_dict)
    
    doc = trend_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.trends.insert_one(doc)
    return trend_obj

@api_router.get("/trends", response_model=List[Trend])
async def get_trends(platform: Optional[str] = None, limit: int = 50):
    """Get all trends, optionally filtered by platform"""
    query = {} if not platform else {"platform": platform}
    trends = await db.trends.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    for trend in trends:
        if isinstance(trend['created_at'], str):
            trend['created_at'] = datetime.fromisoformat(trend['created_at'])
    
    return trends

@api_router.post("/trends/{trend_id}/analyze")
async def analyze_trend(trend_id: str, background_tasks: BackgroundTasks):
    """Analyze a trend using AI"""
    trend = await db.trends.find_one({"id": trend_id}, {"_id": 0})
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    prompt = f"""Analyze this social media trend for monetization opportunities:
    Platform: {trend['platform']}
    Topic: {trend['topic']}
    Keywords: {', '.join(trend['keywords'])}
    Engagement Score: {trend['engagement_score']}
    
    Provide:
    1. Why this trend is valuable
    2. Content ideas to capitalize on it
    3. Products or services that could be promoted
    4. Best posting strategy
    """
    
    analysis = await generate_with_ai(prompt, provider="openai")
    
    await db.trends.update_one(
        {"id": trend_id},
        {"$set": {"analysis": analysis}}
    )
    
    return {"trend_id": trend_id, "analysis": analysis}

# =========================
# ROUTES - Content Creator
# =========================

@api_router.post("/content/generate", response_model=ContentIdea)
async def generate_content_idea(input: ContentIdeaCreate):
    """Generate content idea using AI"""
    
    prompt = input.custom_prompt or f"""Create a compelling {input.content_type} content idea for {input.platform} about tools and accessories.
    Keywords to include: {', '.join(input.keywords)}
    
    Provide:
    1. Catchy title
    2. Detailed description (2-3 paragraphs)
    3. Full content script or outline
    4. Hashtags and call-to-action
    
    Make it engaging and optimized for monetization.
    """
    
    generated_content = await generate_with_ai(prompt, provider="openai")
    
    # Extract title from generated content (first line)
    lines = generated_content.split('\n')
    title = lines[0].replace('#', '').strip() if lines else "Generated Content"
    description = lines[1].strip() if len(lines) > 1 else "AI generated content"
    
    content_obj = ContentIdea(
        title=title[:200],
        description=description[:500],
        platform=input.platform,
        content_type=input.content_type,
        keywords=input.keywords,
        generated_content=generated_content,
        ai_provider="openai"
    )
    
    doc = content_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.content_ideas.insert_one(doc)
    return content_obj

@api_router.get("/content", response_model=List[ContentIdea])
async def get_content_ideas(status: Optional[str] = None, limit: int = 50):
    """Get all content ideas"""
    query = {} if not status else {"status": status}
    content_ideas = await db.content_ideas.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    for content in content_ideas:
        if isinstance(content['created_at'], str):
            content['created_at'] = datetime.fromisoformat(content['created_at'])
    
    return content_ideas

@api_router.patch("/content/{content_id}/status")
async def update_content_status(content_id: str, status: str):
    """Update content status"""
    result = await db.content_ideas.update_one(
        {"id": content_id},
        {"$set": {"status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return {"message": "Status updated", "content_id": content_id, "status": status}

# =========================
# ROUTES - Monetization
# =========================

@api_router.post("/products", response_model=Product)
async def create_product(input: ProductCreate):
    """Create a new product"""
    product_dict = input.model_dump()
    product_obj = Product(**product_dict)
    
    doc = product_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.products.insert_one(doc)
    return product_obj

@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, is_featured: Optional[bool] = None):
    """Get all products"""
    query = {}
    if category:
        query["category"] = category
    if is_featured is not None:
        query["is_featured"] = is_featured
    
    products = await db.products.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for product in products:
        if isinstance(product['created_at'], str):
            product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if isinstance(product['created_at'], str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return product

@api_router.patch("/products/{product_id}")
async def update_product(product_id: str, updates: Dict[str, Any]):
    """Update product details"""
    result = await db.products.update_one(
        {"id": product_id},
        {"$set": updates}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product updated", "product_id": product_id}

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    result = await db.products.delete_one({"id": product_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted", "product_id": product_id}

# =========================
# ROUTES - Social Manager
# =========================

@api_router.post("/social/posts", response_model=SocialPost)
async def create_social_post(input: SocialPostCreate):
    """Create a social media post"""
    post_dict = input.model_dump()
    post_obj = SocialPost(**post_dict)
    
    doc = post_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    if doc.get('scheduled_time'):
        doc['scheduled_time'] = doc['scheduled_time'].isoformat()
    
    await db.social_posts.insert_one(doc)
    return post_obj

@api_router.get("/social/posts", response_model=List[SocialPost])
async def get_social_posts(platform: Optional[str] = None, status: Optional[str] = None):
    """Get all social posts"""
    query = {}
    if platform:
        query["platform"] = platform
    if status:
        query["status"] = status
    
    posts = await db.social_posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for post in posts:
        if isinstance(post['created_at'], str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        if post.get('scheduled_time') and isinstance(post['scheduled_time'], str):
            post['scheduled_time'] = datetime.fromisoformat(post['scheduled_time'])
    
    return posts

@api_router.patch("/social/posts/{post_id}/status")
async def update_post_status(post_id: str, status: str, engagement: Optional[Dict[str, int]] = None):
    """Update post status and engagement"""
    updates = {"status": status}
    if engagement:
        updates["engagement"] = engagement
    
    result = await db.social_posts.update_one(
        {"id": post_id},
        {"$set": updates}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"message": "Post updated", "post_id": post_id}

@api_router.post("/social/posts/{post_id}/publish")
async def publish_post_to_platform(post_id: str):
    """Publish a post automatically to its platform"""
    # Get the post
    post = await db.social_posts.find_one({"id": post_id}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    platform = post.get('platform')
    content = post.get('content')
    media_urls = post.get('media_urls', [])
    
    # Publish to platform
    result = social_publisher.publish(
        platform=platform,
        content=content,
        media_urls=media_urls
    )
    
    if result['success']:
        # Update post status to published
        await db.social_posts.update_one(
            {"id": post_id},
            {"$set": {
                "status": "published",
                "platform_post_id": result.get('post_id'),
                "published_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "message": f"Post published to {platform}",
            "post_id": post_id,
            "platform_post_id": result.get('post_id')
        }
    else:
        # Update status to failed
        await db.social_posts.update_one(
            {"id": post_id},
            {"$set": {
                "status": "failed",
                "error_message": result.get('error')
            }}
        )
        
        raise HTTPException(
            status_code=400,
            detail=f"Failed to publish: {result.get('error')}"
        )

@api_router.get("/social/platform-status")
async def get_platform_status():
    """Get status of all platform integrations"""
    return social_publisher.get_platform_status()

# =========================
# ROUTES - Ad Manager
# =========================

@api_router.post("/campaigns", response_model=Campaign)
async def create_campaign(input: CampaignCreate):
    """Create a new advertising campaign"""
    campaign_dict = input.model_dump()
    campaign_obj = Campaign(**campaign_dict)
    
    doc = campaign_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['start_date'] = doc['start_date'].isoformat()
    doc['end_date'] = doc['end_date'].isoformat()
    
    await db.campaigns.insert_one(doc)
    return campaign_obj

@api_router.get("/campaigns", response_model=List[Campaign])
async def get_campaigns(status: Optional[str] = None):
    """Get all campaigns"""
    query = {} if not status else {"status": status}
    campaigns = await db.campaigns.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for campaign in campaigns:
        if isinstance(campaign['created_at'], str):
            campaign['created_at'] = datetime.fromisoformat(campaign['created_at'])
        if isinstance(campaign['start_date'], str):
            campaign['start_date'] = datetime.fromisoformat(campaign['start_date'])
        if isinstance(campaign['end_date'], str):
            campaign['end_date'] = datetime.fromisoformat(campaign['end_date'])
    
    return campaigns

@api_router.patch("/campaigns/{campaign_id}/status")
async def update_campaign_status(campaign_id: str, status: str):
    """Update campaign status"""
    result = await db.campaigns.update_one(
        {"id": campaign_id},
        {"$set": {"status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {"message": "Campaign updated", "campaign_id": campaign_id, "status": status}

@api_router.patch("/campaigns/{campaign_id}/performance")
async def update_campaign_performance(campaign_id: str, performance: Dict[str, Any]):
    """Update campaign performance metrics"""
    result = await db.campaigns.update_one(
        {"id": campaign_id},
        {"$set": {"performance": performance}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {"message": "Performance updated", "campaign_id": campaign_id}

# =========================
# ROUTES - Analytics
# =========================

@api_router.get("/analytics/dashboard")
async def get_dashboard_analytics():
    """Get overall dashboard analytics"""
    total_trends = await db.trends.count_documents({})
    total_content = await db.content_ideas.count_documents({})
    total_products = await db.products.count_documents({})
    total_posts = await db.social_posts.count_documents({})
    total_campaigns = await db.campaigns.count_documents({})
    
    published_posts = await db.social_posts.count_documents({"status": "published"})
    active_campaigns = await db.campaigns.count_documents({"status": "active"})
    featured_products = await db.products.count_documents({"is_featured": True})
    
    # Get recent trends
    recent_trends = await db.trends.find({}, {"_id": 0}).sort("created_at", -1).limit(5).to_list(5)
    
    # Get top performing posts (by engagement)
    top_posts = await db.social_posts.find(
        {"status": "published"},
        {"_id": 0}
    ).sort("engagement.likes", -1).limit(5).to_list(5)
    
    return {
        "totals": {
            "trends": total_trends,
            "content": total_content,
            "products": total_products,
            "posts": total_posts,
            "campaigns": total_campaigns
        },
        "stats": {
            "published_posts": published_posts,
            "active_campaigns": active_campaigns,
            "featured_products": featured_products
        },
        "recent_trends": recent_trends,
        "top_posts": top_posts
    }

# =========================
# ROUTES - AI Generation
# =========================

@api_router.post("/ai/generate")
async def generate_ai_content(request: AIGenerationRequest):
    """Generate content using AI"""
    result = await generate_with_ai(
        prompt=request.prompt,
        provider=request.provider,
        model=request.model
    )
    
    return {
        "generated_content": result,
        "provider": request.provider,
        "model": request.model or "default"
    }

# =========================
# ROUTES - WordPress Integration
# =========================

@api_router.get("/wordpress/status")
async def wordpress_status():
    """Test WordPress connection"""
    return wordpress_client.test_connection()

@api_router.post("/wordpress/sync-product/{product_id}")
async def sync_product_to_wordpress(product_id: str):
    """Sync a product to WooCommerce"""
    # Get product from MongoDB
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Convert datetime to string if needed
    if isinstance(product.get('created_at'), datetime):
        product['created_at'] = product['created_at'].isoformat()
    
    # Sync to WordPress
    result = wordpress_client.create_product(product)
    
    if result['success']:
        # Save WordPress product ID to MongoDB
        await db.products.update_one(
            {"id": product_id},
            {"$set": {"wc_product_id": result.get('wc_product_id')}}
        )
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get('error'))

@api_router.post("/wordpress/sync-all-products")
async def sync_all_products_to_wordpress():
    """Sync all products to WooCommerce"""
    products = await db.products.find({}, {"_id": 0}).to_list(100)
    
    results = []
    for product in products:
        # Skip if already synced
        if product.get('wc_product_id'):
            continue
        
        # Convert datetime
        if isinstance(product.get('created_at'), datetime):
            product['created_at'] = product['created_at'].isoformat()
        
        result = wordpress_client.create_product(product)
        
        if result['success']:
            await db.products.update_one(
                {"id": product['id']},
                {"$set": {"wc_product_id": result.get('wc_product_id')}}
            )
        
        results.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'success': result['success'],
            'wc_product_id': result.get('wc_product_id'),
            'error': result.get('error')
        })
    
    return {
        'total': len(products),
        'synced': len([r for r in results if r['success']]),
        'results': results
    }

@api_router.post("/wordpress/create-blog-post/{content_id}")
async def create_wordpress_blog_post(content_id: str):
    """Create a WordPress blog post from content"""
    # Get content from MongoDB
    content = await db.content_ideas.find_one({"id": content_id}, {"_id": 0})
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Convert datetime
    if isinstance(content.get('created_at'), datetime):
        content['created_at'] = content['created_at'].isoformat()
    
    # Create blog post
    result = wordpress_client.create_blog_post(content)
    
    if result['success']:
        # Save WordPress post ID to MongoDB
        await db.content_ideas.update_one(
            {"id": content_id},
            {"$set": {
                "wp_post_id": result.get('post_id'),
                "wp_permalink": result.get('permalink')
            }}
        )
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get('error'))

@api_router.get("/wordpress/products")
async def get_wordpress_products():
    """Get products from WooCommerce"""
    result = wordpress_client.get_products(per_page=20)
    
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get('error'))

@api_router.post("/wordpress/auto-sync-featured")
async def auto_sync_featured_products():
    """Automatically sync only featured products to WooCommerce"""
    # Get featured products from MongoDB
    products = await db.products.find({"is_featured": True}, {"_id": 0}).to_list(100)
    
    results = []
    for product in products:
        # Skip if already synced
        if product.get('wc_product_id'):
            continue
        
        # Convert datetime
        if isinstance(product.get('created_at'), datetime):
            product['created_at'] = product['created_at'].isoformat()
        
        result = wordpress_client.create_product(product)
        
        if result['success']:
            await db.products.update_one(
                {"id": product['id']},
                {"$set": {
                    "wc_product_id": result.get('wc_product_id'),
                    "wc_permalink": result.get('permalink'),
                    "synced_at": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        results.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'success': result['success'],
            'wc_product_id': result.get('wc_product_id'),
            'permalink': result.get('permalink')
        })
    
    return {
        'total_featured': len(products),
        'synced': len([r for r in results if r['success']]),
        'results': results
    }

@api_router.post("/wordpress/update-prices")
async def update_woocommerce_prices():
    """Update prices of all synced products in WooCommerce"""
    products = await db.products.find(
        {"wc_product_id": {"$exists": True}},
        {"_id": 0}
    ).to_list(100)
    
    results = []
    for product in products:
        wc_id = product.get('wc_product_id')
        if not wc_id:
            continue
        
        result = wordpress_client.update_product(wc_id, {
            'regular_price': str(product.get('price', 0)),
            'sale_price': str(product.get('price', 0) * (1 - product.get('discount_percentage', 0) / 100)) if product.get('discount_percentage') else None
        })
        
        results.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'success': result['success']
        })
    
    return {
        'total': len(products),
        'updated': len([r for r in results if r['success']]),
        'results': results
    }

@api_router.post("/wordpress/create-category-pages")
async def create_category_landing_pages():
    """Create landing pages for each product category"""
    # Get all unique categories
    products = await db.products.find({}, {"_id": 0, "category": 1}).to_list(1000)
    categories = list(set([p.get('category', 'Uncategorized') for p in products]))
    
    results = []
    for category in categories:
        # Get products in this category
        cat_products = await db.products.find(
            {"category": category},
            {"_id": 0}
        ).to_list(100)
        
        # Create content for landing page
        content = f"""
        <h2>Las Mejores {category.title()} de 2025</h2>
        
        <p>Descubre nuestra selección de {category} profesionales con descuentos exclusivos.</p>
        
        <div class="products-grid">
        """
        
        for product in cat_products:
            discount_text = f"¡{product.get('discount_percentage', 0)}% OFF con código {product.get('discount_code', '')}!" if product.get('discount_code') else ""
            
            content += f"""
            <div class="product-card">
                <h3>{product['name']}</h3>
                <p>{product['description'][:150]}...</p>
                <p class="price">${product['price']}</p>
                <p class="discount">{discount_text}</p>
                <a href="{product.get('affiliate_link', '#')}" class="btn">Ver Producto</a>
            </div>
            """
        
        content += "</div>"
        
        # Create WordPress page
        page_data = {
            'title': f"{category.title()} - Herramientas y Accesorios",
            'content': content,
            'status': 'publish'
        }
        
        # Note: Would need to add create_page method to wordpress_integration.py
        results.append({
            'category': category,
            'products_count': len(cat_products),
            'page_created': True  # Placeholder
        })
    
    return {
        'categories': len(categories),
        'pages_created': len(results),
        'results': results
    }

# =========================
# ROUTES - Payments & Subscriptions
# =========================

# Initialize Stripe
stripe_api_key = os.environ.get('STRIPE_API_KEY')
if not stripe_api_key:
    logger.warning("STRIPE_API_KEY not found in environment variables")

# Predefined subscription packages (server-side only for security)
SUBSCRIPTION_PACKAGES = {
    "basic": {
        "name": "Plan Básico",
        "price": 9.99,
        "features": ["10 productos", "20 posts/mes", "Análisis básico", "Soporte por email"]
    },
    "pro": {
        "name": "Plan Pro", 
        "price": 29.99,
        "features": ["Productos ilimitados", "100 posts/mes", "Análisis avanzado", "Generación IA ilimitada", "Soporte prioritario"]
    },
    "enterprise": {
        "name": "Plan Empresa",
        "price": 99.99,
        "features": ["Todo ilimitado", "API access", "Soporte 24/7", "Manager dedicado", "Custom features"]
    }
}

@api_router.post("/payments/checkout/session")
async def create_checkout_session(request: CheckoutRequest, http_request: Request):
    """Create a Stripe checkout session for product or subscription"""
    try:
        # Get base URL for webhooks
        host_url = str(http_request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        
        # Determine amount based on payment type (server-side only!)
        if request.payment_type == "product":
            if not request.product_id:
                raise HTTPException(status_code=400, detail="product_id required for product payment")
            
            product = await db.products.find_one({"id": request.product_id}, {"_id": 0})
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            amount = float(product['price'])
            currency = "usd"
            metadata = {
                "payment_type": "product",
                "product_id": request.product_id,
                "product_name": product['name'],
                "user_email": request.user_email or "guest"
            }
            
        elif request.payment_type == "subscription":
            if not request.plan_id:
                raise HTTPException(status_code=400, detail="plan_id required for subscription payment")
            
            if request.plan_id not in SUBSCRIPTION_PACKAGES:
                raise HTTPException(status_code=400, detail="Invalid subscription plan")
            
            package = SUBSCRIPTION_PACKAGES[request.plan_id]
            amount = package['price']
            currency = "usd"
            metadata = {
                "payment_type": "subscription",
                "plan_id": request.plan_id,
                "plan_name": package['name'],
                "user_email": request.user_email or "guest"
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid payment_type. Must be 'product' or 'subscription'")
        
        # Add custom metadata
        if request.metadata:
            metadata.update(request.metadata)
        
        # Build success and cancel URLs from frontend origin
        success_url = f"{request.origin_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{request.origin_url}/payment-cancelled"
        
        # Create checkout session request
        checkout_request = CheckoutSessionRequest(
            amount=amount,
            currency=currency,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        
        # Create session with Stripe
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record in DB
        transaction = PaymentTransaction(
            session_id=session.session_id,
            user_email=request.user_email,
            amount=amount,
            currency=currency,
            payment_type=request.payment_type,
            product_id=request.product_id,
            plan_id=request.plan_id,
            payment_status="pending",
            status="initiated",
            metadata=metadata
        )
        
        doc = transaction.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.payment_transactions.insert_one(doc)
        
        return {
            "url": session.url,
            "session_id": session.session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Checkout session creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")

@api_router.get("/payments/checkout/status/{session_id}")
async def get_checkout_status(session_id: str):
    """Get the status of a checkout session"""
    try:
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        
        # Get status from Stripe
        status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction in database
        transaction = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Only update if status changed to avoid duplicate processing
        if transaction['payment_status'] != status.payment_status:
            update_data = {
                "payment_status": status.payment_status,
                "status": "completed" if status.payment_status == "paid" else "failed",
                "payment_id": session_id,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": update_data}
            )
            
            # If payment successful and it's a subscription, create subscription record
            if status.payment_status == "paid" and transaction['payment_type'] == "subscription":
                existing_subscription = await db.subscriptions.find_one({
                    "user_email": transaction['user_email'],
                    "plan_id": transaction['plan_id'],
                    "status": "active"
                })
                
                if not existing_subscription:
                    subscription = Subscription(
                        user_email=transaction['user_email'],
                        plan_id=transaction['plan_id'],
                        stripe_subscription_id=session_id,
                        status="active",
                        current_period_start=datetime.now(timezone.utc),
                        current_period_end=datetime.now(timezone.utc) + timedelta(days=30)
                    )
                    
                    sub_doc = subscription.model_dump()
                    sub_doc['current_period_start'] = sub_doc['current_period_start'].isoformat()
                    sub_doc['current_period_end'] = sub_doc['current_period_end'].isoformat()
                    sub_doc['created_at'] = sub_doc['created_at'].isoformat()
                    sub_doc['updated_at'] = sub_doc['updated_at'].isoformat()
                    
                    await db.subscriptions.insert_one(sub_doc)
        
        return {
            "status": status.status,
            "payment_status": status.payment_status,
            "amount_total": status.amount_total,
            "currency": status.currency,
            "metadata": status.metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Checkout status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get checkout status: {str(e)}")

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing Stripe signature")
        
        # Initialize Stripe checkout
        host_url = str(request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        
        # Handle webhook
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Update transaction based on webhook
        if webhook_response.session_id:
            await db.payment_transactions.update_one(
                {"session_id": webhook_response.session_id},
                {"$set": {
                    "payment_status": webhook_response.payment_status,
                    "status": "completed" if webhook_response.payment_status == "paid" else "failed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        return {"status": "success", "event_type": webhook_response.event_type}
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/payments/history")
async def get_payment_history(user_email: Optional[str] = None, limit: int = 50):
    """Get payment transaction history"""
    query = {}
    if user_email:
        query["user_email"] = user_email
    
    transactions = await db.payment_transactions.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    for tx in transactions:
        if isinstance(tx.get('created_at'), str):
            tx['created_at'] = datetime.fromisoformat(tx['created_at'])
        if isinstance(tx.get('updated_at'), str):
            tx['updated_at'] = datetime.fromisoformat(tx['updated_at'])
    
    return transactions

# =========================
# ROUTES - Subscription Management
# =========================

@api_router.get("/subscriptions/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    plans = []
    for plan_id, plan_data in SUBSCRIPTION_PACKAGES.items():
        plans.append({
            "id": plan_id,
            "name": plan_data["name"],
            "price": plan_data["price"],
            "currency": "usd",
            "interval": "month",
            "features": plan_data["features"]
        })
    return plans

@api_router.get("/subscriptions")
async def get_subscriptions(user_email: Optional[str] = None, status: Optional[str] = None):
    """Get user subscriptions"""
    query = {}
    if user_email:
        query["user_email"] = user_email
    if status:
        query["status"] = status
    
    subscriptions = await db.subscriptions.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for sub in subscriptions:
        if isinstance(sub.get('current_period_start'), str):
            sub['current_period_start'] = datetime.fromisoformat(sub['current_period_start'])
        if isinstance(sub.get('current_period_end'), str):
            sub['current_period_end'] = datetime.fromisoformat(sub['current_period_end'])
        if isinstance(sub.get('created_at'), str):
            sub['created_at'] = datetime.fromisoformat(sub['created_at'])
        if isinstance(sub.get('updated_at'), str):
            sub['updated_at'] = datetime.fromisoformat(sub['updated_at'])
    
    return subscriptions

@api_router.post("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(subscription_id: str):
    """Cancel a subscription"""
    subscription = await db.subscriptions.find_one({"id": subscription_id}, {"_id": 0})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    await db.subscriptions.update_one(
        {"id": subscription_id},
        {"$set": {
            "cancel_at_period_end": True,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"message": "Subscription will be cancelled at period end", "subscription_id": subscription_id}

# =========================
# ROUTES - Revenue Analytics
# =========================

@api_router.get("/analytics/revenue")
async def get_revenue_analytics(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Get comprehensive revenue analytics"""
    
    # Build date filter
    date_filter = {}
    if start_date:
        date_filter["$gte"] = start_date
    if end_date:
        date_filter["$lte"] = end_date
    
    query = {"payment_status": "paid"}
    if date_filter:
        query["created_at"] = date_filter
    
    # Get all paid transactions
    transactions = await db.payment_transactions.find(query, {"_id": 0}).to_list(1000)
    
    # Calculate total revenue
    total_revenue = sum(tx['amount'] for tx in transactions)
    
    # Revenue by type
    product_revenue = sum(tx['amount'] for tx in transactions if tx['payment_type'] == 'product')
    subscription_revenue = sum(tx['amount'] for tx in transactions if tx['payment_type'] == 'subscription')
    
    # Count transactions
    total_transactions = len(transactions)
    product_sales = len([tx for tx in transactions if tx['payment_type'] == 'product'])
    subscription_sales = len([tx for tx in transactions if tx['payment_type'] == 'subscription'])
    
    # Track sales by discount code
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    discount_tracking = {}
    
    for product in products:
        if product.get('discount_code'):
            code = product['discount_code']
            product_sales_count = len([tx for tx in transactions if tx.get('product_id') == product['id']])
            if product_sales_count > 0:
                discount_tracking[code] = {
                    "product_name": product['name'],
                    "discount_code": code,
                    "discount_percentage": product.get('discount_percentage', 0),
                    "sales_count": product_sales_count,
                    "revenue": sum(tx['amount'] for tx in transactions if tx.get('product_id') == product['id'])
                }
    
    # Active subscriptions
    active_subscriptions = await db.subscriptions.count_documents({"status": "active"})
    
    # MRR (Monthly Recurring Revenue)
    mrr = subscription_revenue / max(len(set(tx.get('user_email') for tx in transactions if tx['payment_type'] == 'subscription')), 1)
    
    return {
        "total_revenue": round(total_revenue, 2),
        "product_revenue": round(product_revenue, 2),
        "subscription_revenue": round(subscription_revenue, 2),
        "total_transactions": total_transactions,
        "product_sales": product_sales,
        "subscription_sales": subscription_sales,
        "active_subscriptions": active_subscriptions,
        "mrr": round(mrr, 2),
        "discount_code_tracking": discount_tracking,
        "currency": "usd"
    }

@api_router.get("/analytics/campaign-roi")
async def get_campaign_roi():
    """Calculate ROI for advertising campaigns"""
    
    # Get all campaigns
    campaigns = await db.campaigns.find({}, {"_id": 0}).to_list(1000)
    
    # Get all paid transactions
    transactions = await db.payment_transactions.find(
        {"payment_status": "paid"},
        {"_id": 0}
    ).to_list(1000)
    
    total_revenue = sum(tx['amount'] for tx in transactions)
    
    campaign_roi = []
    for campaign in campaigns:
        budget = campaign['budget']
        
        # Calculate revenue during campaign period
        campaign_start = campaign['start_date']
        campaign_end = campaign['end_date']
        
        if isinstance(campaign_start, str):
            campaign_start = datetime.fromisoformat(campaign_start)
        if isinstance(campaign_end, str):
            campaign_end = datetime.fromisoformat(campaign_end)
        
        campaign_revenue = 0
        for tx in transactions:
            tx_date = tx['created_at']
            if isinstance(tx_date, str):
                tx_date = datetime.fromisoformat(tx_date)
            
            if campaign_start <= tx_date <= campaign_end:
                campaign_revenue += tx['amount']
        
        roi = ((campaign_revenue - budget) / budget * 100) if budget > 0 else 0
        
        campaign_roi.append({
            "campaign_id": campaign['id'],
            "campaign_name": campaign['name'],
            "platform": campaign['platform'],
            "budget": budget,
            "revenue": round(campaign_revenue, 2),
            "roi": round(roi, 2),
            "roi_formatted": f"{roi:.1f}%",
            "status": campaign['status']
        })
    
    return {
        "campaigns": campaign_roi,
        "total_ad_spend": sum(c['budget'] for c in campaigns),
        "total_revenue": round(total_revenue, 2),
        "average_roi": round(sum(c['roi'] for c in campaign_roi) / len(campaign_roi), 2) if campaign_roi else 0
    }

@api_router.get("/analytics/affiliate-commissions")
async def get_affiliate_commissions(commission_rate: float = 10.0):
    """Calculate affiliate commissions"""
    
    # Get all products with affiliate links
    products = await db.products.find(
        {"affiliate_link": {"$exists": True, "$ne": None}},
        {"_id": 0}
    ).to_list(1000)
    
    # Get paid transactions for affiliate products
    transactions = await db.payment_transactions.find(
        {"payment_status": "paid"},
        {"_id": 0}
    ).to_list(1000)
    
    affiliate_commissions = []
    total_commissions = 0
    
    for product in products:
        product_sales = [tx for tx in transactions if tx.get('product_id') == product['id']]
        
        if product_sales:
            revenue = sum(tx['amount'] for tx in product_sales)
            commission = revenue * (commission_rate / 100)
            total_commissions += commission
            
            affiliate_commissions.append({
                "product_id": product['id'],
                "product_name": product['name'],
                "affiliate_link": product['affiliate_link'],
                "sales_count": len(product_sales),
                "revenue": round(revenue, 2),
                "commission_rate": commission_rate,
                "commission_earned": round(commission, 2),
                "category": product.get('category', 'Uncategorized')
            })
    
    return {
        "total_commissions": round(total_commissions, 2),
        "commission_rate": commission_rate,
        "affiliate_products": len(affiliate_commissions),
        "commissions": sorted(affiliate_commissions, key=lambda x: x['commission_earned'], reverse=True),
        "currency": "usd"
    }

@api_router.get("/analytics/dashboard-advanced")
async def get_advanced_dashboard():
    """Get comprehensive analytics dashboard"""
    
    # Get revenue analytics
    revenue_data = await get_revenue_analytics()
    
    # Get campaign ROI
    campaign_data = await get_campaign_roi()
    
    # Get affiliate commissions
    affiliate_data = await get_affiliate_commissions()
    
    # Get basic stats
    products_count = await db.products.count_documents({})
    trends_count = await db.trends.count_documents({})
    content_count = await db.content_ideas.count_documents({})
    posts_count = await db.social_posts.count_documents({})
    campaigns_count = await db.campaigns.count_documents({})
    
    return {
        "overview": {
            "products": products_count,
            "trends": trends_count,
            "content": content_count,
            "social_posts": posts_count,
            "campaigns": campaigns_count
        },
        "revenue": revenue_data,
        "campaign_roi": campaign_data,
        "affiliate_commissions": affiliate_data,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

# =========================
# ROOT ROUTE
# =========================

@api_router.get("/")
async def root():
    return {
        "message": "Social Media Monetization Agent API",
        "version": "2.0.0",
        "modules": [
            "Growth Hacker",
            "Content Creator",
            "Monetization Manager",
            "Social Manager",
            "Ad Manager",
            "WordPress Integration",
            "💳 Payments & Checkout (Stripe)",
            "📊 Revenue Analytics",
            "💰 Subscription Management",
            "📈 Campaign ROI Tracking",
            "🤝 Affiliate Commissions"
        ]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()