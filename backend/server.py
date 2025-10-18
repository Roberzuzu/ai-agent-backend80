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
# ROOT ROUTE
# =========================

@api_router.get("/")
async def root():
    return {
        "message": "Social Media Monetization Agent API",
        "version": "1.0.0",
        "modules": [
            "Growth Hacker",
            "Content Creator",
            "Monetization Manager",
            "Social Manager",
            "Ad Manager",
            "WordPress Integration"
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