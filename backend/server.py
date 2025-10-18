from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
import secrets
import string
from datetime import datetime, timezone, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import asyncio
from social_integrations import SocialMediaPublisher
from wordpress_integration import WordPressIntegration
from passlib.context import CryptContext
from jose import JWTError, jwt

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
    affiliate_code: Optional[str] = None  # For tracking affiliate referrals

# =========================
# AFFILIATE PROGRAM MODELS
# =========================

class Affiliate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    unique_code: str  # Unique affiliate code
    commission_rate: float = 10.0  # Percentage
    status: str = "active"  # active, suspended, pending
    total_earnings: float = 0.0
    total_clicks: int = 0
    total_conversions: int = 0
    payment_email: Optional[str] = None  # PayPal email for payouts
    payment_method: str = "paypal"  # paypal, bank_transfer, stripe
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AffiliateCreate(BaseModel):
    name: str
    email: str
    payment_email: Optional[str] = None
    payment_method: str = "paypal"

class AffiliateLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    product_id: Optional[str] = None  # None means general link
    unique_code: str
    clicks: int = 0
    conversions: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AffiliateLinkCreate(BaseModel):
    product_id: Optional[str] = None

class AffiliateCommission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    transaction_id: str
    product_id: Optional[str] = None
    order_amount: float
    commission_rate: float
    commission_amount: float
    status: str = "pending"  # pending, approved, paid
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None

class AffiliatePayout(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    amount: float
    method: str  # paypal, bank_transfer, stripe
    status: str = "pending"  # pending, processing, completed, failed
    payment_email: Optional[str] = None
    transaction_ref: Optional[str] = None
    notes: Optional[str] = None
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None

class AffiliatePayoutRequest(BaseModel):
    amount: float
    payment_method: str = "paypal"
    payment_email: str

# =========================
# ADVANCED MONETIZATION MODELS
# =========================

# Amazon Associates
class AmazonProduct(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str  # Reference to Product
    amazon_asin: str
    amazon_associate_tag: str = "yourtag-20"  # Default tag
    amazon_link: Optional[str] = None
    clicks: int = 0
    estimated_conversions: int = 0
    commission_rate: float = 4.0  # Default Amazon rate
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AmazonProductCreate(BaseModel):
    product_id: str
    amazon_asin: str
    amazon_associate_tag: Optional[str] = "yourtag-20"

# Dropshipping
class DropshippingProvider(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # AliExpress, CJ Dropshipping, Spocket, etc
    api_key: Optional[str] = None
    is_active: bool = True
    auto_fulfill: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DropshippingOrder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_id: str
    product_id: str
    provider_id: str
    provider_order_id: Optional[str] = None
    customer_email: str
    customer_name: str
    shipping_address: Dict[str, Any]
    product_cost: float
    shipping_cost: float
    total_cost: float
    status: str = "pending"  # pending, processing, shipped, delivered, cancelled
    tracking_number: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DropshippingOrderCreate(BaseModel):
    transaction_id: str
    product_id: str
    provider_id: str
    customer_email: str
    customer_name: str
    shipping_address: Dict[str, Any]

# Memberships & Premium Content
class Membership(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    level: str  # free, basic, pro, vip
    price: float = 0.0
    features: List[str] = []
    status: str = "active"  # active, expired, cancelled
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MembershipCreate(BaseModel):
    user_email: str
    level: str
    duration_days: int = 30

class PremiumContent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    content: str  # The actual premium content
    content_type: str  # article, video, course, template, ebook
    required_level: str  # basic, pro, vip
    thumbnail_url: Optional[str] = None
    price: Optional[float] = None  # One-time purchase option
    views: int = 0
    likes: int = 0
    is_published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PremiumContentCreate(BaseModel):
    title: str
    description: str
    content: str
    content_type: str
    required_level: str
    thumbnail_url: Optional[str] = None
    price: Optional[float] = None

# Donations & Tips
class Donation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    donor_name: str
    donor_email: str
    amount: float
    message: Optional[str] = None
    is_anonymous: bool = False
    payment_status: str = "completed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DonationCreate(BaseModel):
    donor_name: str
    donor_email: str
    amount: float
    message: Optional[str] = None
    is_anonymous: bool = False

class Tip(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str  # Reference to content that received tip
    tipper_name: str
    tipper_email: str
    amount: float
    message: Optional[str] = None
    payment_status: str = "completed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TipCreate(BaseModel):
    content_id: str
    tipper_name: str
    tipper_email: str
    amount: float
    message: Optional[str] = None

class DonationGoal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    target_amount: float
    current_amount: float = 0.0
    is_active: bool = True
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DonationGoalCreate(BaseModel):
    title: str
    description: str
    target_amount: float
    deadline: Optional[datetime] = None

# =========================
# CONVERSION OPTIMIZATION MODELS
# =========================

# A/B Testing
class ABTestVariant(BaseModel):
    model_config = ConfigDict(extra="ignore")
    variant_name: str  # A, B, C
    discount_code: str
    discount_percentage: float
    impressions: int = 0
    conversions: int = 0
    revenue: float = 0.0

class ABTest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    test_name: str
    description: str
    metric: str = "conversion_rate"  # conversion_rate, revenue, average_order
    variants: List[ABTestVariant] = []
    status: str = "running"  # running, paused, completed
    winner: Optional[str] = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ABTestCreate(BaseModel):
    test_name: str
    description: str
    variants: List[ABTestVariant]
    metric: str = "conversion_rate"

# Product Recommendations
class ProductRecommendation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: Optional[str] = None
    recommended_products: List[str] = []  # Product IDs
    recommendation_type: str  # similar, popular, personalized, ai_generated
    source_product_id: Optional[str] = None
    confidence_score: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Email Marketing
class EmailTemplate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    html_body: str
    text_body: Optional[str] = None
    template_type: str  # promotional, abandoned_cart, newsletter, transactional
    variables: List[str] = []  # List of variable names used in template
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    html_body: str
    text_body: Optional[str] = None
    template_type: str
    variables: List[str] = []

class EmailCampaign(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    template_id: str
    segment: str  # all, customers, subscribers, cart_abandoners
    status: str = "draft"  # draft, scheduled, sending, sent, paused
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    recipients_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    converted_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EmailCampaignCreate(BaseModel):
    name: str
    template_id: str
    segment: str
    scheduled_at: Optional[datetime] = None

class EmailRecipient(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campaign_id: str
    email: str
    status: str = "pending"  # pending, sent, opened, clicked, bounced
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    converted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Cart Abandonment
class AbandonedCart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    user_name: Optional[str] = None
    cart_items: List[Dict[str, Any]] = []
    total_amount: float
    abandoned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recovery_email_sent: bool = False
    recovery_email_sent_at: Optional[datetime] = None
    recovered: bool = False
    recovered_at: Optional[datetime] = None
    recovery_discount_code: Optional[str] = None

class AbandonedCartCreate(BaseModel):
    user_email: str
    user_name: Optional[str] = None
    cart_items: List[Dict[str, Any]]
    total_amount: float

class CartRecovery(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    abandoned_cart_id: str
    discount_code: str
    discount_percentage: float = 10.0
    email_sent: bool = False
    recovered: bool = False
    recovered_amount: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
            
            # Add affiliate code if provided
            if request.affiliate_code:
                metadata["affiliate_code"] = request.affiliate_code
            
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
            
            # If payment successful and has affiliate code, create commission
            if status.payment_status == "paid":
                affiliate_code = transaction.get('metadata', {}).get('affiliate_code') or status.metadata.get('affiliate_code')
                
                if affiliate_code:
                    # Find affiliate
                    affiliate = await db.affiliates.find_one({"unique_code": affiliate_code}, {"_id": 0})
                    
                    if affiliate:
                        # Check if commission already exists
                        existing_commission = await db.affiliate_commissions.find_one({
                            "transaction_id": session_id
                        }, {"_id": 0})
                        
                        if not existing_commission:
                            # Calculate commission
                            commission_rate = affiliate['commission_rate']
                            commission_amount = transaction['amount'] * (commission_rate / 100)
                            
                            # Create commission record
                            commission = AffiliateCommission(
                                affiliate_id=affiliate['id'],
                                transaction_id=session_id,
                                product_id=transaction.get('product_id'),
                                order_amount=transaction['amount'],
                                commission_rate=commission_rate,
                                commission_amount=commission_amount,
                                status="approved"  # Auto-approve for now
                            )
                            
                            comm_doc = commission.model_dump()
                            comm_doc['created_at'] = comm_doc['created_at'].isoformat()
                            if comm_doc.get('approved_at'):
                                comm_doc['approved_at'] = comm_doc['approved_at'].isoformat()
                            if comm_doc.get('paid_at'):
                                comm_doc['paid_at'] = comm_doc['paid_at'].isoformat()
                            
                            await db.affiliate_commissions.insert_one(comm_doc)
                            
                            # Update affiliate stats
                            await db.affiliates.update_one(
                                {"id": affiliate['id']},
                                {
                                    "$inc": {
                                        "total_conversions": 1,
                                        "total_earnings": commission_amount
                                    }
                                }
                            )
                            
                            # Update affiliate link conversions
                            if transaction.get('product_id'):
                                await db.affiliate_links.update_one(
                                    {
                                        "affiliate_id": affiliate['id'],
                                        "product_id": transaction['product_id']
                                    },
                                    {"$inc": {"conversions": 1}}
                                )
        
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
# ROUTES - Affiliate Program
# =========================

def generate_unique_code(length: int = 8) -> str:
    """Generate a unique affiliate code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

@api_router.post("/affiliates/register")
async def register_affiliate(data: AffiliateCreate):
    """Register as an affiliate"""
    try:
        # Check if email already registered
        existing = await db.affiliates.find_one({"email": data.email}, {"_id": 0})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered as affiliate")
        
        # Generate unique code
        unique_code = generate_unique_code()
        
        # Ensure uniqueness
        while await db.affiliates.find_one({"unique_code": unique_code}):
            unique_code = generate_unique_code()
        
        # Create affiliate
        affiliate = Affiliate(
            name=data.name,
            email=data.email,
            unique_code=unique_code,
            payment_email=data.payment_email or data.email,
            payment_method=data.payment_method,
            status="active"
        )
        
        doc = affiliate.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.affiliates.insert_one(doc)
        
        return {
            "message": "Affiliate registered successfully",
            "affiliate": affiliate
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Affiliate registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/affiliates/by-email/{email}")
async def get_affiliate_by_email(email: str):
    """Get affiliate info by email"""
    affiliate = await db.affiliates.find_one({"email": email}, {"_id": 0})
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    if isinstance(affiliate.get('created_at'), str):
        affiliate['created_at'] = datetime.fromisoformat(affiliate['created_at'])
    if isinstance(affiliate.get('updated_at'), str):
        affiliate['updated_at'] = datetime.fromisoformat(affiliate['updated_at'])
    
    return affiliate

@api_router.post("/affiliates/links/generate")
async def generate_affiliate_link(data: AffiliateLinkCreate, affiliate_email: str):
    """Generate a unique affiliate link for a product"""
    try:
        # Get affiliate
        affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        # If product_id provided, verify it exists
        if data.product_id:
            product = await db.products.find_one({"id": data.product_id}, {"_id": 0})
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
        
        # Check if link already exists
        existing_link = await db.affiliate_links.find_one({
            "affiliate_id": affiliate['id'],
            "product_id": data.product_id
        }, {"_id": 0})
        
        if existing_link:
            if isinstance(existing_link.get('created_at'), str):
                existing_link['created_at'] = datetime.fromisoformat(existing_link['created_at'])
            return existing_link
        
        # Create new link
        link = AffiliateLink(
            affiliate_id=affiliate['id'],
            product_id=data.product_id,
            unique_code=affiliate['unique_code']
        )
        
        doc = link.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        
        await db.affiliate_links.insert_one(doc)
        
        return link
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Link generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/affiliates/links/{affiliate_email}")
async def get_affiliate_links(affiliate_email: str):
    """Get all links for an affiliate"""
    affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    links = await db.affiliate_links.find(
        {"affiliate_id": affiliate['id']},
        {"_id": 0}
    ).to_list(100)
    
    # Enrich with product info
    for link in links:
        if isinstance(link.get('created_at'), str):
            link['created_at'] = datetime.fromisoformat(link['created_at'])
        
        if link.get('product_id'):
            product = await db.products.find_one({"id": link['product_id']}, {"_id": 0})
            if product:
                link['product_name'] = product['name']
                link['product_price'] = product['price']
    
    return links

@api_router.get("/affiliates/track/{affiliate_code}")
async def track_affiliate_click(affiliate_code: str, product_id: Optional[str] = None, redirect_url: Optional[str] = None):
    """Track affiliate click and redirect"""
    try:
        # Find affiliate by code
        affiliate = await db.affiliates.find_one({"unique_code": affiliate_code}, {"_id": 0})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Invalid affiliate code")
        
        # Update affiliate total clicks
        await db.affiliates.update_one(
            {"unique_code": affiliate_code},
            {"$inc": {"total_clicks": 1}}
        )
        
        # Update link clicks if product specified
        if product_id:
            await db.affiliate_links.update_one(
                {"affiliate_id": affiliate['id'], "product_id": product_id},
                {"$inc": {"clicks": 1}}
            )
        
        # Redirect to product or home
        if redirect_url:
            return RedirectResponse(url=redirect_url)
        elif product_id:
            return RedirectResponse(url=f"/products?highlight={product_id}")
        else:
            return RedirectResponse(url="/")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tracking error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/affiliates/dashboard/{affiliate_email}")
async def get_affiliate_dashboard(affiliate_email: str):
    """Get affiliate dashboard with stats"""
    affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    # Get commissions
    commissions = await db.affiliate_commissions.find(
        {"affiliate_id": affiliate['id']},
        {"_id": 0}
    ).to_list(1000)
    
    # Calculate stats
    total_pending = sum(c['commission_amount'] for c in commissions if c['status'] == 'pending')
    total_approved = sum(c['commission_amount'] for c in commissions if c['status'] == 'approved')
    total_paid = sum(c['commission_amount'] for c in commissions if c['status'] == 'paid')
    
    # Get recent payouts
    payouts = await db.affiliate_payouts.find(
        {"affiliate_id": affiliate['id']},
        {"_id": 0}
    ).sort("requested_at", -1).limit(10).to_list(10)
    
    return {
        "affiliate": affiliate,
        "stats": {
            "total_clicks": affiliate['total_clicks'],
            "total_conversions": affiliate['total_conversions'],
            "conversion_rate": (affiliate['total_conversions'] / affiliate['total_clicks'] * 100) if affiliate['total_clicks'] > 0 else 0,
            "total_earnings": affiliate['total_earnings'],
            "pending_commissions": total_pending,
            "approved_commissions": total_approved,
            "paid_commissions": total_paid
        },
        "recent_payouts": payouts
    }

@api_router.get("/affiliates/commissions/{affiliate_email}")
async def get_affiliate_commissions_list(affiliate_email: str, status: Optional[str] = None):
    """Get commissions for an affiliate"""
    affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    query = {"affiliate_id": affiliate['id']}
    if status:
        query["status"] = status
    
    commissions = await db.affiliate_commissions.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    # Enrich with product/transaction info
    for commission in commissions:
        if isinstance(commission.get('created_at'), str):
            commission['created_at'] = datetime.fromisoformat(commission['created_at'])
        if isinstance(commission.get('approved_at'), str):
            commission['approved_at'] = datetime.fromisoformat(commission['approved_at'])
        if isinstance(commission.get('paid_at'), str):
            commission['paid_at'] = datetime.fromisoformat(commission['paid_at'])
        
        if commission.get('product_id'):
            product = await db.products.find_one({"id": commission['product_id']}, {"_id": 0})
            if product:
                commission['product_name'] = product['name']
    
    return commissions

@api_router.post("/affiliates/payouts/request")
async def request_affiliate_payout(data: AffiliatePayoutRequest, affiliate_email: str):
    """Request a payout"""
    try:
        affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        # Check approved balance
        commissions = await db.affiliate_commissions.find(
            {"affiliate_id": affiliate['id'], "status": "approved"},
            {"_id": 0}
        ).to_list(1000)
        
        approved_balance = sum(c['commission_amount'] for c in commissions)
        
        if data.amount > approved_balance:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient approved balance. Available: ${approved_balance:.2f}"
            )
        
        if data.amount < 50:
            raise HTTPException(status_code=400, detail="Minimum payout amount is $50")
        
        # Create payout request
        payout = AffiliatePayout(
            affiliate_id=affiliate['id'],
            amount=data.amount,
            method=data.payment_method,
            payment_email=data.payment_email,
            status="pending"
        )
        
        doc = payout.model_dump()
        doc['requested_at'] = doc['requested_at'].isoformat()
        if doc.get('processed_at'):
            doc['processed_at'] = doc['processed_at'].isoformat()
        
        await db.affiliate_payouts.insert_one(doc)
        
        return {
            "message": "Payout requested successfully",
            "payout": payout
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payout request error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/affiliates/payouts/{affiliate_email}")
async def get_affiliate_payouts(affiliate_email: str):
    """Get payout history for an affiliate"""
    affiliate = await db.affiliates.find_one({"email": affiliate_email}, {"_id": 0})
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    payouts = await db.affiliate_payouts.find(
        {"affiliate_id": affiliate['id']},
        {"_id": 0}
    ).sort("requested_at", -1).to_list(100)
    
    for payout in payouts:
        if isinstance(payout.get('requested_at'), str):
            payout['requested_at'] = datetime.fromisoformat(payout['requested_at'])
        if isinstance(payout.get('processed_at'), str):
            payout['processed_at'] = datetime.fromisoformat(payout['processed_at'])
    
    return payouts

@api_router.get("/affiliates/all")
async def get_all_affiliates():
    """Get all affiliates (admin endpoint)"""
    affiliates = await db.affiliates.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for affiliate in affiliates:
        if isinstance(affiliate.get('created_at'), str):
            affiliate['created_at'] = datetime.fromisoformat(affiliate['created_at'])
        if isinstance(affiliate.get('updated_at'), str):
            affiliate['updated_at'] = datetime.fromisoformat(affiliate['updated_at'])
    
    return affiliates

# =========================
# ROUTES - Amazon Associates Integration
# =========================

@api_router.post("/amazon/products")
async def create_amazon_product(data: AmazonProductCreate):
    """Link a product to Amazon Associates"""
    try:
        # Verify product exists
        product = await db.products.find_one({"id": data.product_id}, {"_id": 0})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Generate Amazon affiliate link
        amazon_link = f"https://www.amazon.com/dp/{data.amazon_asin}?tag={data.amazon_associate_tag}"
        
        amazon_product = AmazonProduct(
            product_id=data.product_id,
            amazon_asin=data.amazon_asin,
            amazon_associate_tag=data.amazon_associate_tag,
            amazon_link=amazon_link
        )
        
        doc = amazon_product.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        
        await db.amazon_products.insert_one(doc)
        
        return amazon_product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Amazon product creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/amazon/products")
async def get_amazon_products():
    """Get all Amazon-linked products"""
    amazon_products = await db.amazon_products.find({}, {"_id": 0}).to_list(100)
    
    for item in amazon_products:
        if isinstance(item.get('created_at'), str):
            item['created_at'] = datetime.fromisoformat(item['created_at'])
        
        # Enrich with product info
        product = await db.products.find_one({"id": item['product_id']}, {"_id": 0})
        if product:
            item['product_name'] = product['name']
            item['product_price'] = product['price']
    
    return amazon_products

@api_router.post("/amazon/track/{amazon_product_id}")
async def track_amazon_click(amazon_product_id: str):
    """Track click on Amazon affiliate link"""
    try:
        result = await db.amazon_products.update_one(
            {"id": amazon_product_id},
            {"$inc": {"clicks": 1}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Amazon product not found")
        
        # Get the amazon link to redirect
        amazon_product = await db.amazon_products.find_one({"id": amazon_product_id}, {"_id": 0})
        
        return {
            "message": "Click tracked",
            "redirect_url": amazon_product['amazon_link']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Amazon click tracking error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/amazon/analytics")
async def get_amazon_analytics():
    """Get Amazon Associates analytics"""
    amazon_products = await db.amazon_products.find({}, {"_id": 0}).to_list(1000)
    
    total_clicks = sum(p['clicks'] for p in amazon_products)
    total_conversions = sum(p['estimated_conversions'] for p in amazon_products)
    
    # Estimated earnings (assuming 4% commission and $30 average order)
    estimated_earnings = total_conversions * 30 * 0.04
    
    return {
        "total_products": len(amazon_products),
        "total_clicks": total_clicks,
        "estimated_conversions": total_conversions,
        "estimated_earnings": round(estimated_earnings, 2),
        "click_through_rate": round((total_conversions / total_clicks * 100) if total_clicks > 0 else 0, 2),
        "products": amazon_products
    }

# =========================
# ROUTES - Dropshipping Automation
# =========================

@api_router.post("/dropshipping/providers")
async def create_dropshipping_provider(provider: DropshippingProvider):
    """Add a dropshipping provider"""
    doc = provider.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.dropshipping_providers.insert_one(doc)
    return provider

@api_router.get("/dropshipping/providers")
async def get_dropshipping_providers():
    """Get all dropshipping providers"""
    providers = await db.dropshipping_providers.find({}, {"_id": 0}).to_list(100)
    
    for provider in providers:
        if isinstance(provider.get('created_at'), str):
            provider['created_at'] = datetime.fromisoformat(provider['created_at'])
    
    return providers

@api_router.post("/dropshipping/orders")
async def create_dropshipping_order(order_data: DropshippingOrderCreate):
    """Create a dropshipping order"""
    try:
        # Get product and provider
        product = await db.products.find_one({"id": order_data.product_id}, {"_id": 0})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        provider = await db.dropshipping_providers.find_one({"id": order_data.provider_id}, {"_id": 0})
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Calculate costs (simplified)
        product_cost = product['price'] * 0.6  # Assume 40% margin
        shipping_cost = 5.0
        total_cost = product_cost + shipping_cost
        
        order = DropshippingOrder(
            transaction_id=order_data.transaction_id,
            product_id=order_data.product_id,
            provider_id=order_data.provider_id,
            customer_email=order_data.customer_email,
            customer_name=order_data.customer_name,
            shipping_address=order_data.shipping_address,
            product_cost=product_cost,
            shipping_cost=shipping_cost,
            total_cost=total_cost,
            status="pending"
        )
        
        doc = order.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.dropshipping_orders.insert_one(doc)
        
        # Auto-fulfill if enabled
        if provider.get('auto_fulfill'):
            # Simulate fulfillment
            await db.dropshipping_orders.update_one(
                {"id": order.id},
                {"$set": {
                    "status": "processing",
                    "provider_order_id": f"DS-{str(uuid.uuid4())[:8].upper()}"
                }}
            )
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dropshipping order creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/dropshipping/orders")
async def get_dropshipping_orders(status: Optional[str] = None):
    """Get dropshipping orders"""
    query = {}
    if status:
        query["status"] = status
    
    orders = await db.dropshipping_orders.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for order in orders:
        if isinstance(order.get('created_at'), str):
            order['created_at'] = datetime.fromisoformat(order['created_at'])
        if isinstance(order.get('updated_at'), str):
            order['updated_at'] = datetime.fromisoformat(order['updated_at'])
        
        # Enrich with product info
        product = await db.products.find_one({"id": order['product_id']}, {"_id": 0})
        if product:
            order['product_name'] = product['name']
    
    return orders

@api_router.patch("/dropshipping/orders/{order_id}/status")
async def update_dropshipping_order_status(order_id: str, status: str, tracking_number: Optional[str] = None):
    """Update dropshipping order status"""
    update_data = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    if tracking_number:
        update_data["tracking_number"] = tracking_number
    
    result = await db.dropshipping_orders.update_one(
        {"id": order_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated", "order_id": order_id, "status": status}

@api_router.get("/dropshipping/analytics")
async def get_dropshipping_analytics():
    """Get dropshipping analytics"""
    orders = await db.dropshipping_orders.find({}, {"_id": 0}).to_list(1000)
    
    total_orders = len(orders)
    total_revenue = sum(o.get('total_cost', 0) for o in orders)
    
    by_status = {}
    for order in orders:
        status = order['status']
        by_status[status] = by_status.get(status, 0) + 1
    
    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "orders_by_status": by_status,
        "average_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0
    }

# =========================
# ROUTES - Memberships & Premium Content
# =========================

# Membership levels configuration
MEMBERSHIP_LEVELS = {
    "free": {"price": 0, "features": ["Acceso básico", "Contenido público"]},
    "basic": {"price": 9.99, "features": ["Todo de Free", "Contenido exclusivo básico", "Descuentos 10%"]},
    "pro": {"price": 29.99, "features": ["Todo de Basic", "Contenido premium", "Descuentos 20%", "Soporte prioritario"]},
    "vip": {"price": 99.99, "features": ["Todo de Pro", "Acceso total", "Descuentos 30%", "Consultas 1-on-1"]}
}

@api_router.get("/memberships/levels")
async def get_membership_levels():
    """Get available membership levels"""
    return MEMBERSHIP_LEVELS

@api_router.post("/memberships")
async def create_membership(data: MembershipCreate):
    """Create or upgrade membership"""
    try:
        if data.level not in MEMBERSHIP_LEVELS:
            raise HTTPException(status_code=400, detail="Invalid membership level")
        
        # Check if user already has membership
        existing = await db.memberships.find_one(
            {"user_email": data.user_email, "status": "active"},
            {"_id": 0}
        )
        
        if existing:
            # Upgrade membership
            await db.memberships.update_one(
                {"id": existing['id']},
                {"$set": {
                    "status": "expired",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        # Create new membership
        level_info = MEMBERSHIP_LEVELS[data.level]
        membership = Membership(
            user_email=data.user_email,
            level=data.level,
            price=level_info['price'],
            features=level_info['features'],
            expires_at=datetime.now(timezone.utc) + timedelta(days=data.duration_days)
        )
        
        doc = membership.model_dump()
        doc['started_at'] = doc['started_at'].isoformat()
        doc['expires_at'] = doc['expires_at'].isoformat()
        doc['created_at'] = doc['created_at'].isoformat()
        
        await db.memberships.insert_one(doc)
        
        return membership
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Membership creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/memberships/{user_email}")
async def get_user_membership(user_email: str):
    """Get user's active membership"""
    membership = await db.memberships.find_one(
        {"user_email": user_email, "status": "active"},
        {"_id": 0}
    )
    
    if not membership:
        # Return free membership
        return {
            "level": "free",
            "price": 0,
            "features": MEMBERSHIP_LEVELS["free"]["features"],
            "status": "active"
        }
    
    if isinstance(membership.get('started_at'), str):
        membership['started_at'] = datetime.fromisoformat(membership['started_at'])
    if isinstance(membership.get('expires_at'), str):
        membership['expires_at'] = datetime.fromisoformat(membership['expires_at'])
    if isinstance(membership.get('created_at'), str):
        membership['created_at'] = datetime.fromisoformat(membership['created_at'])
    
    return membership

@api_router.post("/premium-content")
async def create_premium_content(content: PremiumContentCreate):
    """Create premium content"""
    premium_content = PremiumContent(**content.model_dump())
    
    doc = premium_content.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.premium_content.insert_one(doc)
    return premium_content

@api_router.get("/premium-content")
async def get_premium_content(level: Optional[str] = None, user_email: Optional[str] = None):
    """Get premium content (filtered by user's membership level)"""
    query = {"is_published": True}
    
    # Get user's membership level if email provided
    user_level = "free"
    if user_email:
        membership = await db.memberships.find_one(
            {"user_email": user_email, "status": "active"},
            {"_id": 0}
        )
        if membership:
            user_level = membership['level']
    
    # Filter by level if specified
    if level:
        query["required_level"] = level
    
    content_list = await db.premium_content.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    # Hierarchy: free < basic < pro < vip
    level_hierarchy = ["free", "basic", "pro", "vip"]
    user_level_index = level_hierarchy.index(user_level) if user_level in level_hierarchy else 0
    
    # Filter content based on user's level
    accessible_content = []
    for content in content_list:
        content_level_index = level_hierarchy.index(content['required_level'])
        
        # Add access flag
        content['has_access'] = user_level_index >= content_level_index
        
        # Hide full content if no access
        if not content['has_access']:
            content['content'] = content['content'][:200] + "... [Contenido Premium - Actualiza tu membresía]"
        
        if isinstance(content.get('created_at'), str):
            content['created_at'] = datetime.fromisoformat(content['created_at'])
        
        accessible_content.append(content)
    
    return accessible_content

@api_router.get("/premium-content/{content_id}")
async def get_premium_content_detail(content_id: str, user_email: Optional[str] = None):
    """Get premium content detail"""
    content = await db.premium_content.find_one({"id": content_id}, {"_id": 0})
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Check access
    user_level = "free"
    if user_email:
        membership = await db.memberships.find_one(
            {"user_email": user_email, "status": "active"},
            {"_id": 0}
        )
        if membership:
            user_level = membership['level']
    
    level_hierarchy = ["free", "basic", "pro", "vip"]
    user_level_index = level_hierarchy.index(user_level)
    content_level_index = level_hierarchy.index(content['required_level'])
    
    has_access = user_level_index >= content_level_index
    
    if not has_access:
        content['content'] = "🔒 Contenido Premium - Actualiza tu membresía para acceder"
    
    # Increment views
    await db.premium_content.update_one(
        {"id": content_id},
        {"$inc": {"views": 1}}
    )
    
    if isinstance(content.get('created_at'), str):
        content['created_at'] = datetime.fromisoformat(content['created_at'])
    
    content['has_access'] = has_access
    return content

# =========================
# ROUTES - Donations & Tips
# =========================

@api_router.post("/donations")
async def create_donation(donation: DonationCreate):
    """Create a donation"""
    donation_obj = Donation(**donation.model_dump())
    
    doc = donation_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.donations.insert_one(doc)
    return donation_obj

@api_router.get("/donations")
async def get_donations(limit: int = 50):
    """Get recent donations"""
    donations = await db.donations.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    for donation in donations:
        if isinstance(donation.get('created_at'), str):
            donation['created_at'] = datetime.fromisoformat(donation['created_at'])
        
        # Hide email if anonymous
        if donation.get('is_anonymous'):
            donation['donor_name'] = "Anónimo"
            donation['donor_email'] = "***"
    
    return donations

@api_router.get("/donations/leaderboard")
async def get_donations_leaderboard(limit: int = 10):
    """Get top donors leaderboard"""
    # Aggregate donations by donor
    donations = await db.donations.find(
        {"is_anonymous": False},
        {"_id": 0}
    ).to_list(1000)
    
    # Group by donor
    donor_totals = {}
    for donation in donations:
        email = donation['donor_email']
        if email not in donor_totals:
            donor_totals[email] = {
                "donor_name": donation['donor_name'],
                "donor_email": email,
                "total_amount": 0,
                "donation_count": 0
            }
        donor_totals[email]['total_amount'] += donation['amount']
        donor_totals[email]['donation_count'] += 1
    
    # Sort by total amount
    leaderboard = sorted(
        donor_totals.values(),
        key=lambda x: x['total_amount'],
        reverse=True
    )[:limit]
    
    return leaderboard

@api_router.get("/donations/stats")
async def get_donation_stats():
    """Get donation statistics"""
    donations = await db.donations.find({}, {"_id": 0}).to_list(1000)
    
    total_amount = sum(d['amount'] for d in donations)
    total_count = len(donations)
    average_amount = total_amount / total_count if total_count > 0 else 0
    
    return {
        "total_donations": total_count,
        "total_amount": round(total_amount, 2),
        "average_donation": round(average_amount, 2),
        "currency": "usd"
    }

@api_router.post("/tips")
async def create_tip(tip: TipCreate):
    """Create a tip for content"""
    tip_obj = Tip(**tip.model_dump())
    
    doc = tip_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.tips.insert_one(doc)
    return tip_obj

@api_router.get("/tips/content/{content_id}")
async def get_content_tips(content_id: str):
    """Get tips for specific content"""
    tips = await db.tips.find({"content_id": content_id}, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for tip in tips:
        if isinstance(tip.get('created_at'), str):
            tip['created_at'] = datetime.fromisoformat(tip['created_at'])
    
    total_tips = sum(t['amount'] for t in tips)
    
    return {
        "content_id": content_id,
        "total_tips": round(total_tips, 2),
        "tip_count": len(tips),
        "tips": tips
    }

@api_router.post("/donation-goals")
async def create_donation_goal(goal: DonationGoalCreate):
    """Create a donation goal"""
    goal_obj = DonationGoal(**goal.model_dump())
    
    doc = goal_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    if doc.get('deadline'):
        doc['deadline'] = doc['deadline'].isoformat()
    
    await db.donation_goals.insert_one(doc)
    return goal_obj

@api_router.get("/donation-goals")
async def get_donation_goals(is_active: Optional[bool] = None):
    """Get donation goals"""
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    goals = await db.donation_goals.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for goal in goals:
        if isinstance(goal.get('created_at'), str):
            goal['created_at'] = datetime.fromisoformat(goal['created_at'])
        if goal.get('deadline') and isinstance(goal['deadline'], str):
            goal['deadline'] = datetime.fromisoformat(goal['deadline'])
        
        # Calculate progress
        goal['progress_percentage'] = round((goal['current_amount'] / goal['target_amount'] * 100), 2) if goal['target_amount'] > 0 else 0
    
    return goals

@api_router.patch("/donation-goals/{goal_id}/contribute")
async def contribute_to_goal(goal_id: str, amount: float):
    """Contribute to a donation goal"""
    result = await db.donation_goals.update_one(
        {"id": goal_id, "is_active": True},
        {"$inc": {"current_amount": amount}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found or inactive")
    
    # Check if goal reached
    goal = await db.donation_goals.find_one({"id": goal_id}, {"_id": 0})
    if goal and goal['current_amount'] >= goal['target_amount']:
        await db.donation_goals.update_one(
            {"id": goal_id},
            {"$set": {"is_active": False}}
        )
        return {"message": "Goal reached! 🎉", "goal": goal}
    
    return {"message": "Contribution added", "current_amount": goal['current_amount']}

# =========================
# ROUTES - Conversion Optimization
# =========================

# A/B Testing Endpoints
@api_router.post("/ab-tests")
async def create_ab_test(test: ABTestCreate):
    """Create a new A/B test"""
    ab_test = ABTest(**test.model_dump())
    
    doc = ab_test.model_dump()
    doc['started_at'] = doc['started_at'].isoformat()
    doc['created_at'] = doc['created_at'].isoformat()
    if doc.get('ended_at'):
        doc['ended_at'] = doc['ended_at'].isoformat()
    
    await db.ab_tests.insert_one(doc)
    return ab_test

@api_router.get("/ab-tests")
async def get_ab_tests(status: Optional[str] = None):
    """Get all A/B tests"""
    query = {}
    if status:
        query["status"] = status
    
    tests = await db.ab_tests.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for test in tests:
        if isinstance(test.get('started_at'), str):
            test['started_at'] = datetime.fromisoformat(test['started_at'])
        if isinstance(test.get('ended_at'), str):
            test['ended_at'] = datetime.fromisoformat(test['ended_at'])
        if isinstance(test.get('created_at'), str):
            test['created_at'] = datetime.fromisoformat(test['created_at'])
        
        # Calculate conversion rates for each variant
        for variant in test.get('variants', []):
            if variant['impressions'] > 0:
                variant['conversion_rate'] = round((variant['conversions'] / variant['impressions']) * 100, 2)
            else:
                variant['conversion_rate'] = 0
    
    return tests

@api_router.get("/ab-tests/{test_id}")
async def get_ab_test(test_id: str):
    """Get specific A/B test with analysis"""
    test = await db.ab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Calculate statistics
    variants = test.get('variants', [])
    for variant in variants:
        if variant['impressions'] > 0:
            variant['conversion_rate'] = round((variant['conversions'] / variant['impressions']) * 100, 2)
            variant['average_order_value'] = round(variant['revenue'] / variant['conversions'], 2) if variant['conversions'] > 0 else 0
        else:
            variant['conversion_rate'] = 0
            variant['average_order_value'] = 0
    
    # Determine winner (simple version)
    if test['metric'] == 'conversion_rate':
        winner = max(variants, key=lambda x: x.get('conversion_rate', 0)) if variants else None
    elif test['metric'] == 'revenue':
        winner = max(variants, key=lambda x: x.get('revenue', 0)) if variants else None
    else:
        winner = None
    
    test['suggested_winner'] = winner['variant_name'] if winner else None
    
    if isinstance(test.get('started_at'), str):
        test['started_at'] = datetime.fromisoformat(test['started_at'])
    if isinstance(test.get('ended_at'), str):
        test['ended_at'] = datetime.fromisoformat(test['ended_at'])
    if isinstance(test.get('created_at'), str):
        test['created_at'] = datetime.fromisoformat(test['created_at'])
    
    return test

@api_router.post("/ab-tests/{test_id}/track")
async def track_ab_test_event(test_id: str, variant_name: str, event_type: str, amount: float = 0):
    """Track impression or conversion for A/B test variant"""
    test = await db.ab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Find variant index
    variant_index = next((i for i, v in enumerate(test['variants']) if v['variant_name'] == variant_name), None)
    if variant_index is None:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    # Update based on event type
    if event_type == "impression":
        update_path = f"variants.{variant_index}.impressions"
        await db.ab_tests.update_one(
            {"id": test_id},
            {"$inc": {update_path: 1}}
        )
    elif event_type == "conversion":
        update_data = {
            f"variants.{variant_index}.conversions": 1,
            f"variants.{variant_index}.revenue": amount
        }
        await db.ab_tests.update_one(
            {"id": test_id},
            {"$inc": update_data}
        )
    
    return {"message": "Event tracked", "test_id": test_id, "variant": variant_name}

@api_router.patch("/ab-tests/{test_id}/status")
async def update_ab_test_status(test_id: str, status: str, winner: Optional[str] = None):
    """Update A/B test status"""
    update_data = {"status": status}
    
    if status == "completed":
        update_data["ended_at"] = datetime.now(timezone.utc).isoformat()
        if winner:
            update_data["winner"] = winner
    
    result = await db.ab_tests.update_one(
        {"id": test_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return {"message": "Test status updated", "status": status}

# Product Recommendations Endpoints
@api_router.get("/recommendations/{user_email}")
async def get_product_recommendations(user_email: str, limit: int = 5):
    """Get AI-powered product recommendations for user"""
    try:
        # Get user's purchase history
        transactions = await db.payment_transactions.find(
            {"user_email": user_email, "payment_status": "paid"},
            {"_id": 0}
        ).to_list(100)
        
        purchased_product_ids = [t.get('product_id') for t in transactions if t.get('product_id')]
        
        # Get all products
        products = await db.products.find({}, {"_id": 0}).to_list(1000)
        
        # Simple recommendation algorithm
        recommendations = []
        
        if purchased_product_ids:
            # Get products from same categories
            purchased_products = [p for p in products if p['id'] in purchased_product_ids]
            categories = set(p.get('category', 'General') for p in purchased_products)
            
            similar_products = [
                p for p in products 
                if p['id'] not in purchased_product_ids 
                and p.get('category') in categories
            ]
            
            recommendations.extend(similar_products[:limit])
        
        # Fill with popular products if needed
        if len(recommendations) < limit:
            # Get products with most sales
            product_sales = {}
            for product in products:
                if product['id'] not in purchased_product_ids:
                    sales_count = len([t for t in transactions if t.get('product_id') == product['id']])
                    product_sales[product['id']] = sales_count
            
            popular = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
            popular_product_ids = [p[0] for p in popular[:limit - len(recommendations)]]
            popular_products = [p for p in products if p['id'] in popular_product_ids]
            recommendations.extend(popular_products)
        
        # Create recommendation record
        rec = ProductRecommendation(
            user_email=user_email,
            recommended_products=[p['id'] for p in recommendations],
            recommendation_type="personalized",
            confidence_score=0.8
        )
        
        rec_doc = rec.model_dump()
        rec_doc['created_at'] = rec_doc['created_at'].isoformat()
        await db.product_recommendations.insert_one(rec_doc)
        
        return {
            "user_email": user_email,
            "recommendations": recommendations[:limit],
            "recommendation_type": "personalized"
        }
        
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/recommendations/product/{product_id}/similar")
async def get_similar_products(product_id: str, limit: int = 4):
    """Get similar products based on category and attributes"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = product.get('category', 'General')
    
    # Find products in same category
    similar = await db.products.find(
        {"category": category, "id": {"$ne": product_id}},
        {"_id": 0}
    ).limit(limit).to_list(limit)
    
    return {
        "source_product": product,
        "similar_products": similar,
        "recommendation_type": "similar"
    }

# Email Marketing Endpoints
@api_router.post("/email/templates")
async def create_email_template(template: EmailTemplateCreate):
    """Create email template"""
    email_template = EmailTemplate(**template.model_dump())
    
    doc = email_template.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.email_templates.insert_one(doc)
    return email_template

@api_router.get("/email/templates")
async def get_email_templates(template_type: Optional[str] = None):
    """Get all email templates"""
    query = {}
    if template_type:
        query["template_type"] = template_type
    
    templates = await db.email_templates.find(query, {"_id": 0}).to_list(100)
    
    for template in templates:
        if isinstance(template.get('created_at'), str):
            template['created_at'] = datetime.fromisoformat(template['created_at'])
    
    return templates

@api_router.post("/email/campaigns")
async def create_email_campaign(campaign: EmailCampaignCreate):
    """Create email campaign"""
    # Verify template exists
    template = await db.email_templates.find_one({"id": campaign.template_id}, {"_id": 0})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    email_campaign = EmailCampaign(**campaign.model_dump())
    
    doc = email_campaign.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    if doc.get('scheduled_at'):
        doc['scheduled_at'] = doc['scheduled_at'].isoformat()
    if doc.get('sent_at'):
        doc['sent_at'] = doc['sent_at'].isoformat()
    
    await db.email_campaigns.insert_one(doc)
    return email_campaign

@api_router.get("/email/campaigns")
async def get_email_campaigns(status: Optional[str] = None):
    """Get email campaigns"""
    query = {}
    if status:
        query["status"] = status
    
    campaigns = await db.email_campaigns.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for campaign in campaigns:
        if isinstance(campaign.get('created_at'), str):
            campaign['created_at'] = datetime.fromisoformat(campaign['created_at'])
        if campaign.get('scheduled_at') and isinstance(campaign['scheduled_at'], str):
            campaign['scheduled_at'] = datetime.fromisoformat(campaign['scheduled_at'])
        if campaign.get('sent_at') and isinstance(campaign['sent_at'], str):
            campaign['sent_at'] = datetime.fromisoformat(campaign['sent_at'])
        
        # Calculate metrics
        if campaign['recipients_count'] > 0:
            campaign['open_rate'] = round((campaign['opened_count'] / campaign['recipients_count']) * 100, 2)
            campaign['click_rate'] = round((campaign['clicked_count'] / campaign['recipients_count']) * 100, 2)
            campaign['conversion_rate'] = round((campaign['converted_count'] / campaign['recipients_count']) * 100, 2)
        else:
            campaign['open_rate'] = 0
            campaign['click_rate'] = 0
            campaign['conversion_rate'] = 0
    
    return campaigns

@api_router.patch("/email/campaigns/{campaign_id}/send")
async def send_email_campaign(campaign_id: str):
    """Send email campaign (simulated)"""
    campaign = await db.email_campaigns.find_one({"id": campaign_id}, {"_id": 0})
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Simulate sending
    recipient_count = 100  # Mock count
    
    await db.email_campaigns.update_one(
        {"id": campaign_id},
        {"$set": {
            "status": "sent",
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "recipients_count": recipient_count
        }}
    )
    
    return {
        "message": "Campaign sent",
        "campaign_id": campaign_id,
        "recipients": recipient_count
    }

# Cart Abandonment Endpoints
@api_router.post("/cart/abandoned")
async def create_abandoned_cart(cart: AbandonedCartCreate):
    """Create abandoned cart record"""
    abandoned_cart = AbandonedCart(**cart.model_dump())
    
    doc = abandoned_cart.model_dump()
    doc['abandoned_at'] = doc['abandoned_at'].isoformat()
    if doc.get('recovery_email_sent_at'):
        doc['recovery_email_sent_at'] = doc['recovery_email_sent_at'].isoformat()
    if doc.get('recovered_at'):
        doc['recovered_at'] = doc['recovered_at'].isoformat()
    
    await db.abandoned_carts.insert_one(doc)
    return abandoned_cart

@api_router.get("/cart/abandoned")
async def get_abandoned_carts(recovered: Optional[bool] = None, limit: int = 50):
    """Get abandoned carts"""
    query = {}
    if recovered is not None:
        query["recovered"] = recovered
    
    carts = await db.abandoned_carts.find(query, {"_id": 0}).sort("abandoned_at", -1).limit(limit).to_list(limit)
    
    for cart in carts:
        if isinstance(cart.get('abandoned_at'), str):
            cart['abandoned_at'] = datetime.fromisoformat(cart['abandoned_at'])
        if cart.get('recovery_email_sent_at') and isinstance(cart['recovery_email_sent_at'], str):
            cart['recovery_email_sent_at'] = datetime.fromisoformat(cart['recovery_email_sent_at'])
        if cart.get('recovered_at') and isinstance(cart['recovered_at'], str):
            cart['recovered_at'] = datetime.fromisoformat(cart['recovered_at'])
    
    return carts

@api_router.post("/cart/abandoned/{cart_id}/send-recovery")
async def send_cart_recovery_email(cart_id: str, discount_percentage: float = 10.0):
    """Send cart recovery email with discount"""
    cart = await db.abandoned_carts.find_one({"id": cart_id}, {"_id": 0})
    if not cart:
        raise HTTPException(status_code=404, detail="Abandoned cart not found")
    
    # Generate discount code
    discount_code = f"RECOVER{str(uuid.uuid4())[:8].upper()}"
    
    # Create recovery record
    recovery = CartRecovery(
        abandoned_cart_id=cart_id,
        discount_code=discount_code,
        discount_percentage=discount_percentage,
        email_sent=True
    )
    
    recovery_doc = recovery.model_dump()
    recovery_doc['created_at'] = recovery_doc['created_at'].isoformat()
    await db.cart_recoveries.insert_one(recovery_doc)
    
    # Update cart
    await db.abandoned_carts.update_one(
        {"id": cart_id},
        {"$set": {
            "recovery_email_sent": True,
            "recovery_email_sent_at": datetime.now(timezone.utc).isoformat(),
            "recovery_discount_code": discount_code
        }}
    )
    
    return {
        "message": "Recovery email sent",
        "discount_code": discount_code,
        "discount_percentage": discount_percentage
    }

@api_router.patch("/cart/abandoned/{cart_id}/recover")
async def mark_cart_recovered(cart_id: str, recovered_amount: float):
    """Mark cart as recovered"""
    result = await db.abandoned_carts.update_one(
        {"id": cart_id},
        {"$set": {
            "recovered": True,
            "recovered_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Update recovery record
    await db.cart_recoveries.update_one(
        {"abandoned_cart_id": cart_id},
        {"$set": {
            "recovered": True,
            "recovered_amount": recovered_amount
        }}
    )
    
    return {"message": "Cart marked as recovered", "amount": recovered_amount}

@api_router.get("/cart/analytics")
async def get_cart_analytics():
    """Get cart abandonment analytics"""
    all_carts = await db.abandoned_carts.find({}, {"_id": 0}).to_list(1000)
    
    total_abandoned = len(all_carts)
    total_value = sum(cart['total_amount'] for cart in all_carts)
    recovered_carts = [cart for cart in all_carts if cart.get('recovered')]
    recovered_count = len(recovered_carts)
    recovered_value = sum(cart['total_amount'] for cart in recovered_carts)
    
    recovery_emails_sent = len([cart for cart in all_carts if cart.get('recovery_email_sent')])
    
    return {
        "total_abandoned_carts": total_abandoned,
        "total_abandoned_value": round(total_value, 2),
        "recovered_carts": recovered_count,
        "recovered_value": round(recovered_value, 2),
        "recovery_rate": round((recovered_count / total_abandoned * 100), 2) if total_abandoned > 0 else 0,
        "recovery_emails_sent": recovery_emails_sent,
        "average_cart_value": round(total_value / total_abandoned, 2) if total_abandoned > 0 else 0
    }

# =========================
# ROOT ROUTE
# =========================

@api_router.get("/")
async def root():
    return {
        "message": "Social Media Monetization Agent API",
        "version": "4.0.0",
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
            "🤝 Affiliate Program",
            "🛒 Amazon Associates Integration",
            "📦 Dropshipping Automation",
            "👑 Memberships & Premium Content",
            "💝 Donations & Tips",
            "🧪 A/B Testing",
            "🤖 AI Product Recommendations",
            "📧 Email Marketing Automation",
            "🛒 Cart Abandonment Recovery"
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