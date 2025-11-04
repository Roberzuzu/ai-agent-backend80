from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Request, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from agent_core import CerebroUncensored
import aiohttp
from fastapi import HTTPException
from fastapi import HTTPException, Request
from pydantic import BaseModel
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
import secrets
import string
from datetime import datetime, timezone, timedelta
# STANDALONE VERSION - No Emergent dependencies
from llm_client import LlmChat, UserMessage
from stripe_client import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import asyncio
from social_integrations import SocialMediaPublisher
from wordpress_integration import WordPressIntegration
from passlib.context import CryptContext
from jose import JWTError, jwt
import stripe
import requests
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class IAQuery(BaseModel):
    user_id: str
    message: str

@app.post("/api/ai/ask")
async def ask_ai(query: IAQuery):
    # (Aquí irá la lógica de IA real)
    respuesta_ia = f"Respuesta IA simulada a: {query.message}"
    return {"reply": respuesta_ia}
# Load Telegram configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Inicializar Cerebro AI Agent
ADMIN_TELEGRAM_ID = os.environ.get('ADMIN_TELEGRAM_ID', '7202793910')
agente = CerebroUncensored(db, ADMIN_TELEGRAM_ID)
import httpx

class CerebroUncensored:
    def __init__(self, db, admin_id):
        ...
    async def procesarcomando(self, command, userid):
        ...
    async def crear_producto_inteligente(self, command: str) -> dict:
        ...
    
# =========================
# SECURITY SYSTEMS
# =========================
from security.rate_limiter import RateLimiter
from security.api_keys import APIKeyManager
from security.audit_logs import AuditLogger
from security.two_factor import TwoFactorManager
from security.headers import (
    SecurityHeadersMiddleware,
    IPWhitelistMiddleware,
    CSRFProtectionMiddleware
)

# Initialize security managers
rate_limiter = RateLimiter()
api_key_manager = APIKeyManager(db)
audit_logger = AuditLogger(db, retention_days=90)
two_factor_manager = TwoFactorManager(db, app_name="Social Media Monetization")

# Configure trusted IPs for rate limiting (from environment)
trusted_ips = os.environ.get('TRUSTED_IPS', '').split(',')
for ip in trusted_ips:
    if ip.strip():
        rate_limiter.add_trusted_ip(ip.strip())

# Configure IP whitelist for admin endpoints (from environment)
admin_whitelist_ips = os.environ.get('ADMIN_WHITELIST_IPS', '').split(',')
admin_whitelist = [ip.strip() for ip in admin_whitelist_ips if ip.strip()]

# =========================
# MONITORING SYSTEMS
# =========================
from monitoring.health_checks import HealthChecker
from monitoring.metrics import MetricsCollector, metrics_collector
from monitoring.sentry_integration import initialize_sentry

# Initialize monitoring
health_checker = HealthChecker(
    db=db,
    stripe_enabled=bool(os.environ.get('STRIPE_API_KEY')),
    openai_enabled=bool(os.environ.get('OPENAI_API_KEY'))
)

# Initialize Sentry (if DSN is configured)
sentry = initialize_sentry(
    dsn=os.environ.get('SENTRY_DSN'),
    environment=os.environ.get('ENVIRONMENT', 'development')
)

# Configure logging
logger = logging.getLogger(__name__)

# Create the main app without a prefix
app = FastAPI(title="Social Media Monetization Agent")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize social media publisher
social_publisher = SocialMediaPublisher()

# Initialize WordPress integration
wordpress_client = WordPressIntegration()

# =========================
# SECURITY CONFIGURATION
# =========================

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production-please-make-it-very-secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# =========================
# AUTH MODELS
# =========================

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    full_name: str
    hashed_password: str
    role: str = "user"  # user, admin, affiliate
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

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
# NOTIFICATION MODELS
# =========================

class Notification(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    type: str  # info, success, warning, error, payment, affiliate, campaign, product
    title: str
    message: str
    link: Optional[str] = None  # Link to related resource
    icon: Optional[str] = None  # Icon name for frontend
    is_read: bool = False
    is_archived: bool = False
    metadata: Dict[str, Any] = {}  # Additional data
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    read_at: Optional[datetime] = None

class NotificationCreate(BaseModel):
    user_email: str
    type: str
    title: str
    message: str
    link: Optional[str] = None
    icon: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class NotificationPreferences(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    email_notifications: bool = True
    push_notifications: bool = True
    telegram_notifications: bool = True  # NEW
    # Specific notification types
    notify_payments: bool = True
    notify_affiliates: bool = True
    notify_campaigns: bool = True
    notify_products: bool = True
    notify_subscriptions: bool = True
    notify_system: bool = True
    # Email digest
    email_digest: str = "daily"  # none, daily, weekly, monthly
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationPreferencesUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    telegram_notifications: Optional[bool] = None  # NEW
    notify_payments: Optional[bool] = None
    notify_affiliates: Optional[bool] = None
    notify_campaigns: Optional[bool] = None
    notify_products: Optional[bool] = None
    notify_subscriptions: Optional[bool] = None
    notify_system: Optional[bool] = None
    email_digest: Optional[str] = None

# =========================
# AI RECOMMENDATIONS MODELS
# =========================

class UserInteraction(BaseModel):
    """Track user interactions for collaborative filtering"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    product_id: str
    interaction_type: str  # view, click, purchase, add_to_cart, wishlist
    interaction_score: float = 1.0  # Different weights for different interactions
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductEmbedding(BaseModel):
    """Store OpenAI embeddings for products"""
    model_config = ConfigDict(extra="ignore")
    product_id: str
    embedding: List[float]  # 1536 dimensions for text-embedding-ada-002
    text_used: str  # The text that was embedded
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RecommendationRequest(BaseModel):
    user_email: str
    limit: int = 10
    algorithm: str = "hybrid"  # similarity, collaborative, hybrid
    exclude_purchased: bool = True
    category: Optional[str] = None

class RecommendationResponse(BaseModel):
    product_id: str
    product_name: str
    product_description: str
    product_price: float
    product_image: Optional[str] = None
    product_category: str
    score: float
    reason: str  # Why this was recommended
    algorithm_used: str

# =========================
# ADVANCED ANALYTICS MODELS
# =========================

class AnalyticsEvent(BaseModel):
    """Track all user events for analytics"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: Optional[str] = None
    session_id: str
    event_type: str  # page_view, click, purchase, signup, etc.
    event_category: str  # engagement, conversion, revenue
    page_url: Optional[str] = None
    referrer: Optional[str] = None
    device_type: Optional[str] = None  # mobile, desktop, tablet
    browser: Optional[str] = None
    country: Optional[str] = None
    metadata: Dict[str, Any] = {}
    value: Optional[float] = None  # For revenue events
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FunnelStep(BaseModel):
    """Define steps in a conversion funnel"""
    step_number: int
    step_name: str
    event_type: str  # What event triggers this step
    required: bool = True

class Funnel(BaseModel):
    """Conversion funnel definition"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    steps: List[FunnelStep]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CohortDefinition(BaseModel):
    """Define a user cohort"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    criteria: Dict[str, Any]  # Criteria to include users
    start_date: datetime
    end_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CustomerMetrics(BaseModel):
    """Customer lifetime value and metrics"""
    model_config = ConfigDict(extra="ignore")
    user_email: str
    total_revenue: float = 0.0
    total_orders: int = 0
    average_order_value: float = 0.0
    lifetime_value: float = 0.0
    churn_probability: float = 0.0
    last_purchase_date: Optional[datetime] = None
    days_since_last_purchase: int = 0
    predicted_next_purchase_days: Optional[int] = None
    customer_segment: str = "new"  # new, active, at_risk, churned
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AnalyticsConfig(BaseModel):
    """Store analytics integration configs"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ga4_measurement_id: Optional[str] = None
    ga4_api_secret: Optional[str] = None
    meta_pixel_id: Optional[str] = None
    meta_access_token: Optional[str] = None
    hotjar_site_id: Optional[str] = None
    clarity_project_id: Optional[str] = None
    is_ga4_enabled: bool = False
    is_meta_pixel_enabled: bool = False
    is_heatmap_enabled: bool = False
    heatmap_provider: str = "clarity"  # clarity or hotjar
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# =========================
# MEMBERSHIP LIMITS MODELS
# =========================

class MembershipTier(BaseModel):
    """Membership tier configuration"""
    tier: str  # basic, pro, vip
    name: str
    limits: Dict[str, Any]  # Limits configuration

class UsageTracking(BaseModel):
    """Track user usage for limits"""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    resource_type: str  # products, posts, campaigns, etc.
    count: int = 0
    period_start: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    period_end: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LimitCheckResponse(BaseModel):
    """Response for limit check"""
    allowed: bool
    current_usage: int
    limit: int
    percentage: float
    remaining: int
    tier: str
    message: str
    needs_upgrade: bool = False

# Membership limits configuration
MEMBERSHIP_LIMITS = {
    "basic": {
        "name": "Básico",
        "products_limit": 10,
        "posts_per_month": 20,
        "campaigns_limit": 3,
        "affiliates_limit": 5,
        "email_campaigns_per_month": 10,
        "ab_tests_concurrent": 2,
        "storage_mb": 100,
        "api_calls_per_day": 1000
    },
    "pro": {
        "name": "Pro",
        "products_limit": -1,  # -1 means unlimited
        "posts_per_month": 100,
        "campaigns_limit": 10,
        "affiliates_limit": 25,
        "email_campaigns_per_month": 50,
        "ab_tests_concurrent": 5,
        "storage_mb": 1000,
        "api_calls_per_day": 10000
    },
    "vip": {
        "name": "VIP",
        "products_limit": -1,
        "posts_per_month": -1,
        "campaigns_limit": -1,
        "affiliates_limit": -1,
        "email_campaigns_per_month": -1,
        "ab_tests_concurrent": -1,
        "storage_mb": -1,
        "api_calls_per_day": -1
    }
}

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

# Stripe Webhooks
class WebhookLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str  # Stripe event ID
    event_type: str  # checkout.session.completed, etc
    payload: Dict[str, Any]
    status: str = "received"  # received, processed, failed, retrying
    error_message: Optional[str] = None
    retry_count: int = 0
    processed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
# AUTH UTILITIES
# =========================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if user is None:
        raise credentials_exception
    
    # Convert datetime strings back to datetime objects
    if isinstance(user.get('created_at'), str):
        user['created_at'] = datetime.fromisoformat(user['created_at'])
    if isinstance(user.get('updated_at'), str):
        user['updated_at'] = datetime.fromisoformat(user['updated_at'])
    
    return User(**user)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_roles: List[str]):
    """Dependency to require specific roles"""
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {current_user.role} not authorized. Required: {required_roles}"
            )
        return current_user
    return role_checker

# =========================
# ROUTES - Authentication
# =========================

@api_router.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_username = await db.users.find_one({"username": user.username}, {"_id": 0})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    
    user_doc = new_user.model_dump()
    user_doc['created_at'] = user_doc['created_at'].isoformat()
    user_doc['updated_at'] = user_doc['updated_at'].isoformat()
    
    await db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.email})
    
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        role=new_user.role,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@api_router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password"""
    # Find user by email (form_data.username is actually email in our case)
    user = await db.users.find_one({"email": form_data.username}, {"_id": 0})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})
    
    # Convert datetime strings
    if isinstance(user.get('created_at'), str):
        user['created_at'] = datetime.fromisoformat(user['created_at'])
    
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        full_name=user["full_name"],
        role=user["role"],
        is_active=user["is_active"],
        is_verified=user.get("is_verified", False),
        created_at=user['created_at']
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current logged in user info"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@api_router.post("/auth/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should remove token)"""
    return {"message": "Successfully logged out"}

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

@api_router.get("/campaigns")
async def get_campaigns(status: Optional[str] = None):
    """Get all campaigns"""
    query = {} if not status else {"status": status}
    campaigns = await db.campaigns.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for campaign in campaigns:
        if 'created_at' in campaign and isinstance(campaign['created_at'], str):
            campaign['created_at'] = datetime.fromisoformat(campaign['created_at'])
        if 'start_date' in campaign and isinstance(campaign['start_date'], str):
            campaign['start_date'] = datetime.fromisoformat(campaign['start_date'])
        if 'end_date' in campaign and isinstance(campaign['end_date'], str):
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
# MEMBERSHIP LIMITS HELPERS
# =========================

async def get_user_tier(user_email: str) -> str:
    """Get user's membership tier"""
    # Check if user has active subscription
    subscription = await db.subscriptions.find_one(
        {"user_email": user_email, "status": "active"},
        {"_id": 0}
    )
    
    if subscription:
        plan = subscription.get('plan', 'basic').lower()
        if 'vip' in plan or 'enterprise' in plan:
            return 'vip'
        elif 'pro' in plan:
            return 'pro'
    
    return 'basic'

async def get_current_usage(user_email: str, resource_type: str) -> int:
    """Get current usage for a resource type"""
    now = datetime.now(timezone.utc)
    
    # Calculate period based on resource type
    if 'per_month' in resource_type:
        # Monthly limit - check this month
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif 'per_day' in resource_type:
        # Daily limit - check today
        period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Total limit - no period
        period_start = None
    
    # Get usage tracking
    if period_start:
        usage = await db.usage_tracking.find_one({
            "user_email": user_email,
            "resource_type": resource_type,
            "period_start": {"$gte": period_start.isoformat()}
        }, {"_id": 0})
    else:
        usage = await db.usage_tracking.find_one({
            "user_email": user_email,
            "resource_type": resource_type
        }, {"_id": 0})
    
    if usage:
        return usage.get('count', 0)
    
    # Fallback: count directly from collections
    if resource_type == 'products':
        return await db.products.count_documents({"user_email": user_email})
    elif resource_type == 'posts_per_month':
        return await db.social_posts.count_documents({
            "user_email": user_email,
            "created_at": {"$gte": period_start.isoformat()}
        })
    elif resource_type == 'campaigns':
        return await db.campaigns.count_documents({"user_email": user_email})
    elif resource_type == 'affiliates':
        return await db.affiliates.count_documents({"email": user_email})
    
    return 0

async def check_limit(user_email: str, resource_type: str) -> LimitCheckResponse:
    """Check if user has reached limit for a resource"""
    tier = await get_user_tier(user_email)
    limits = MEMBERSHIP_LIMITS[tier]
    
    # Get limit for this resource
    limit_key = f"{resource_type}_limit" if not resource_type.endswith('_limit') and not 'per_' in resource_type else resource_type
    if limit_key not in limits:
        limit_key = resource_type
    
    limit = limits.get(limit_key, -1)
    
    # -1 means unlimited
    if limit == -1:
        return LimitCheckResponse(
            allowed=True,
            current_usage=0,
            limit=-1,
            percentage=0,
            remaining=-1,
            tier=tier,
            message="Ilimitado",
            needs_upgrade=False
        )
    
    # Get current usage
    current_usage = await get_current_usage(user_email, resource_type)
    
    # Check if limit reached
    allowed = current_usage < limit
    percentage = (current_usage / limit * 100) if limit > 0 else 0
    remaining = max(0, limit - current_usage)
    
    # Generate message
    if not allowed:
        message = f"Has alcanzado el límite de {limit} para tu plan {limits['name']}"
    elif percentage >= 80:
        message = f"Estás cerca del límite ({current_usage}/{limit})"
    else:
        message = f"Uso actual: {current_usage}/{limit}"
    
    return LimitCheckResponse(
        allowed=allowed,
        current_usage=current_usage,
        limit=limit,
        percentage=round(percentage, 1),
        remaining=remaining,
        tier=tier,
        message=message,
        needs_upgrade=not allowed
    )

async def increment_usage(user_email: str, resource_type: str) -> bool:
    """Increment usage counter for a resource"""
    now = datetime.now(timezone.utc)
    
    # Calculate period
    if 'per_month' in resource_type:
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    elif 'per_day' in resource_type:
        period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_end = period_start + timedelta(days=1) - timedelta(seconds=1)
    else:
        period_start = now
        period_end = now + timedelta(days=365)  # Far future
    
    # Update or create usage tracking
    result = await db.usage_tracking.update_one(
        {
            "user_email": user_email,
            "resource_type": resource_type,
            "period_start": {"$gte": period_start.isoformat(), "$lte": period_end.isoformat()}
        },
        {
            "$inc": {"count": 1},
            "$set": {"updated_at": now.isoformat()},
            "$setOnInsert": {
                "id": str(uuid.uuid4()),
                "user_email": user_email,
                "resource_type": resource_type,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "created_at": now.isoformat()
            }
        },
        upsert=True
    )
    
    return True

# =========================
# ROUTES - Membership Limits
# =========================

@api_router.get("/limits/check/{resource_type}")
async def check_resource_limit(resource_type: str, user_email: str):
    """Check if user can create more of a resource"""
    try:
        result = await check_limit(user_email, resource_type)
        return result
    except Exception as e:
        logger.error(f"Error checking limit: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/limits/usage")
async def get_all_usage(user_email: str):
    """Get usage stats for all resources"""
    try:
        tier = await get_user_tier(user_email)
        limits = MEMBERSHIP_LIMITS[tier]
        
        usage_data = {}
        
        for resource_type in ['products', 'posts_per_month', 'campaigns', 'affiliates']:
            limit_check = await check_limit(user_email, resource_type)
            usage_data[resource_type] = {
                "current": limit_check.current_usage,
                "limit": limit_check.limit,
                "percentage": limit_check.percentage,
                "remaining": limit_check.remaining
            }
        
        return {
            "tier": tier,
            "tier_name": limits['name'],
            "usage": usage_data,
            "limits": limits
        }
    except Exception as e:
        logger.error(f"Error getting usage: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/limits/tiers")
async def get_membership_tiers():
    """Get all membership tiers and their limits"""
    return {
        "tiers": [
            {
                "tier": "basic",
                "name": MEMBERSHIP_LIMITS["basic"]["name"],
                "price": 0,
                "limits": MEMBERSHIP_LIMITS["basic"]
            },
            {
                "tier": "pro",
                "name": MEMBERSHIP_LIMITS["pro"]["name"],
                "price": 29.99,
                "limits": MEMBERSHIP_LIMITS["pro"]
            },
            {
                "tier": "vip",
                "name": MEMBERSHIP_LIMITS["vip"]["name"],
                "price": 99.99,
                "limits": MEMBERSHIP_LIMITS["vip"]
            }
        ]
    }

# =========================
# ROUTES - Advanced Analytics
# =========================

@api_router.post("/analytics/event")
async def track_analytics_event(
    session_id: str,
    event_type: str,
    event_category: str,
    user_email: Optional[str] = None,
    page_url: Optional[str] = None,
    referrer: Optional[str] = None,
    device_type: Optional[str] = None,
    browser: Optional[str] = None,
    value: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Track analytics event"""
    try:
        event = {
            "id": str(uuid.uuid4()),
            "user_email": user_email,
            "session_id": session_id,
            "event_type": event_type,
            "event_category": event_category,
            "page_url": page_url,
            "referrer": referrer,
            "device_type": device_type,
            "browser": browser,
            "country": None,  # Could use IP geolocation
            "metadata": metadata or {},
            "value": value,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.analytics_events.insert_one(event)
        
        # Send to GA4 if enabled
        config = await db.analytics_config.find_one({}, {"_id": 0})
        if config and config.get('is_ga4_enabled') and config.get('ga4_measurement_id'):
            # TODO: Send to GA4 Measurement Protocol
            pass
        
        # Send to Meta Pixel if enabled
        if config and config.get('is_meta_pixel_enabled') and config.get('meta_pixel_id'):
            # TODO: Send to Meta Conversion API
            pass
        
        return {"message": "Event tracked", "event_id": event['id']}
        
    except Exception as e:
        logger.error(f"Error tracking event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/config")
async def get_analytics_config():
    """Get analytics configuration"""
    try:
        config = await db.analytics_config.find_one({}, {"_id": 0})
        
        if not config:
            # Create default config
            default_config = {
                "id": str(uuid.uuid4()),
                "is_ga4_enabled": False,
                "is_meta_pixel_enabled": False,
                "is_heatmap_enabled": False,
                "heatmap_provider": "clarity",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await db.analytics_config.insert_one(default_config)
            return default_config
        
        return config
        
    except Exception as e:
        logger.error(f"Error getting config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.patch("/analytics/config")
async def update_analytics_config(
    ga4_measurement_id: Optional[str] = None,
    ga4_api_secret: Optional[str] = None,
    meta_pixel_id: Optional[str] = None,
    meta_access_token: Optional[str] = None,
    hotjar_site_id: Optional[str] = None,
    clarity_project_id: Optional[str] = None,
    is_ga4_enabled: Optional[bool] = None,
    is_meta_pixel_enabled: Optional[bool] = None,
    is_heatmap_enabled: Optional[bool] = None,
    heatmap_provider: Optional[str] = None
):
    """Update analytics configuration"""
    try:
        update_data = {}
        
        if ga4_measurement_id is not None:
            update_data['ga4_measurement_id'] = ga4_measurement_id
        if ga4_api_secret is not None:
            update_data['ga4_api_secret'] = ga4_api_secret
        if meta_pixel_id is not None:
            update_data['meta_pixel_id'] = meta_pixel_id
        if meta_access_token is not None:
            update_data['meta_access_token'] = meta_access_token
        if hotjar_site_id is not None:
            update_data['hotjar_site_id'] = hotjar_site_id
        if clarity_project_id is not None:
            update_data['clarity_project_id'] = clarity_project_id
        if is_ga4_enabled is not None:
            update_data['is_ga4_enabled'] = is_ga4_enabled
        if is_meta_pixel_enabled is not None:
            update_data['is_meta_pixel_enabled'] = is_meta_pixel_enabled
        if is_heatmap_enabled is not None:
            update_data['is_heatmap_enabled'] = is_heatmap_enabled
        if heatmap_provider is not None:
            update_data['heatmap_provider'] = heatmap_provider
        
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        await db.analytics_config.update_one(
            {},
            {"$set": update_data},
            upsert=True
        )
        
        return {"message": "Configuration updated", "updated_fields": list(update_data.keys())}
        
    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/funnel/{funnel_id}")
async def analyze_funnel(funnel_id: str, days: int = 30):
    """Analyze conversion funnel"""
    try:
        # Get funnel definition
        funnel = await db.funnels.find_one({"id": funnel_id}, {"_id": 0})
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Funnel not found")
        
        # Calculate date range
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # Analyze each step
        results = []
        previous_users = None
        
        for step in funnel['steps']:
            # Get users who completed this step
            events = await db.analytics_events.find({
                "event_type": step['event_type'],
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }, {"_id": 0}).to_list(10000)
            
            unique_users = set([e.get('user_email') or e['session_id'] for e in events])
            
            # Calculate conversion from previous step
            if previous_users is not None:
                conversion_rate = (len(unique_users) / len(previous_users) * 100) if len(previous_users) > 0 else 0
                drop_off_rate = 100 - conversion_rate
            else:
                conversion_rate = 100
                drop_off_rate = 0
            
            results.append({
                "step_number": step['step_number'],
                "step_name": step['step_name'],
                "users": len(unique_users),
                "conversion_rate": round(conversion_rate, 2),
                "drop_off_rate": round(drop_off_rate, 2)
            })
            
            previous_users = unique_users
        
        return {
            "funnel_id": funnel_id,
            "funnel_name": funnel['name'],
            "period_days": days,
            "steps": results,
            "overall_conversion": round((results[-1]['users'] / results[0]['users'] * 100) if results[0]['users'] > 0 else 0, 2)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing funnel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/cohorts")
async def analyze_cohorts(cohort_type: str = "monthly", metric: str = "retention"):
    """Analyze user cohorts"""
    try:
        # Get all users grouped by signup month
        users_cursor = db.analytics_events.aggregate([
            {"$match": {"event_type": "signup"}},
            {"$group": {
                "_id": {
                    "year": {"$year": {"$dateFromString": {"dateString": "$created_at"}}},
                    "month": {"$month": {"$dateFromString": {"dateString": "$created_at"}}}
                },
                "users": {"$addToSet": "$user_email"}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}},
            {"$limit": 12}
        ])
        
        cohorts = await users_cursor.to_list(12)
        
        # Calculate retention for each cohort
        cohort_analysis = []
        
        for cohort in cohorts:
            cohort_month = f"{cohort['_id']['year']}-{cohort['_id']['month']:02d}"
            cohort_users = set(cohort['users'])
            
            # Calculate retention for next 6 months
            retention_data = []
            for month_offset in range(6):
                # Simulate retention data (in production, query actual user activity)
                retention_rate = max(0, 100 - (month_offset * 15))  # Simulated decay
                retention_data.append({
                    "month": month_offset,
                    "retention_rate": retention_rate,
                    "active_users": int(len(cohort_users) * retention_rate / 100)
                })
            
            cohort_analysis.append({
                "cohort": cohort_month,
                "initial_users": len(cohort_users),
                "retention": retention_data
            })
        
        return {
            "cohort_type": cohort_type,
            "metric": metric,
            "cohorts": cohort_analysis
        }
        
    except Exception as e:
        logger.error(f"Error analyzing cohorts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/clv")
async def calculate_customer_lifetime_value(user_email: Optional[str] = None):
    """Calculate Customer Lifetime Value"""
    try:
        query = {}
        if user_email:
            query["user_email"] = user_email
        
        # Get all payment transactions
        transactions = await db.payment_transactions.find(
            {**query, "payment_status": "paid"},
            {"_id": 0}
        ).to_list(10000)
        
        # Group by user
        user_metrics = {}
        
        for txn in transactions:
            email = txn.get('user_email')
            if not email:
                continue
            
            if email not in user_metrics:
                user_metrics[email] = {
                    "total_revenue": 0,
                    "total_orders": 0,
                    "first_purchase": None,
                    "last_purchase": None
                }
            
            user_metrics[email]['total_revenue'] += txn.get('amount', 0)
            user_metrics[email]['total_orders'] += 1
            
            created_at = txn.get('created_at')
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            
            if user_metrics[email]['first_purchase'] is None or created_at < user_metrics[email]['first_purchase']:
                user_metrics[email]['first_purchase'] = created_at
            
            if user_metrics[email]['last_purchase'] is None or created_at > user_metrics[email]['last_purchase']:
                user_metrics[email]['last_purchase'] = created_at
        
        # Calculate CLV metrics
        clv_data = []
        now = datetime.now(timezone.utc)
        
        for email, metrics in user_metrics.items():
            aov = metrics['total_revenue'] / metrics['total_orders'] if metrics['total_orders'] > 0 else 0
            
            # Days since last purchase
            days_since_last = (now - metrics['last_purchase']).days if metrics['last_purchase'] else 999
            
            # Customer lifetime (days)
            lifetime_days = (metrics['last_purchase'] - metrics['first_purchase']).days if metrics['first_purchase'] and metrics['last_purchase'] else 0
            
            # Predict churn (simple rule-based)
            if days_since_last > 90:
                churn_probability = 0.8
                segment = "churned"
            elif days_since_last > 60:
                churn_probability = 0.5
                segment = "at_risk"
            elif days_since_last > 30:
                churn_probability = 0.2
                segment = "active"
            else:
                churn_probability = 0.05
                segment = "very_active"
            
            # Simple CLV = AOV * Purchase Frequency * Customer Lifetime
            purchase_frequency = metrics['total_orders'] / max(lifetime_days / 30, 1)  # Orders per month
            predicted_lifetime_months = 12 * (1 - churn_probability)  # Predicted remaining lifetime
            clv = aov * purchase_frequency * predicted_lifetime_months
            
            clv_data.append({
                "user_email": email,
                "total_revenue": round(metrics['total_revenue'], 2),
                "total_orders": metrics['total_orders'],
                "average_order_value": round(aov, 2),
                "lifetime_value": round(clv, 2),
                "days_since_last_purchase": days_since_last,
                "churn_probability": round(churn_probability, 2),
                "customer_segment": segment,
                "lifetime_days": lifetime_days
            })
        
        # Sort by CLV descending
        clv_data.sort(key=lambda x: x['lifetime_value'], reverse=True)
        
        if user_email:
            return clv_data[0] if clv_data else {}
        
        # Return summary statistics
        total_clv = sum(c['lifetime_value'] for c in clv_data)
        avg_clv = total_clv / len(clv_data) if clv_data else 0
        
        return {
            "total_customers": len(clv_data),
            "total_clv": round(total_clv, 2),
            "average_clv": round(avg_clv, 2),
            "top_customers": clv_data[:10],
            "segments": {
                "very_active": len([c for c in clv_data if c['customer_segment'] == 'very_active']),
                "active": len([c for c in clv_data if c['customer_segment'] == 'active']),
                "at_risk": len([c for c in clv_data if c['customer_segment'] == 'at_risk']),
                "churned": len([c for c in clv_data if c['customer_segment'] == 'churned'])
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating CLV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/dashboard")
async def get_analytics_dashboard(days: int = 30):
    """Get comprehensive analytics dashboard"""
    try:
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # Get event counts by type
        events_cursor = db.analytics_events.aggregate([
            {"$match": {
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }},
            {"$group": {
                "_id": "$event_type",
                "count": {"$sum": 1}
            }}
        ])
        
        events_by_type = {e['_id']: e['count'] for e in await events_cursor.to_list(100)}
        
        # Get unique users/sessions
        unique_users = await db.analytics_events.distinct(
            "user_email",
            {
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                },
                "user_email": {"$ne": None}
            }
        )
        
        unique_sessions = await db.analytics_events.distinct(
            "session_id",
            {
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }
        )
        
        return {
            "period_days": days,
            "total_events": sum(events_by_type.values()),
            "events_by_type": events_by_type,
            "unique_users": len(unique_users),
            "unique_sessions": len(unique_sessions),
            "avg_events_per_session": round(sum(events_by_type.values()) / len(unique_sessions), 2) if unique_sessions else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
            
            # Send notification for successful payment
            if status.payment_status == "paid" and transaction.get('user_email'):
                await create_notification_internal(
                    user_email=transaction['user_email'],
                    notification_type="payment",
                    title="💰 ¡Pago Recibido!",
                    message=f"Tu pago de ${transaction['amount']} ha sido procesado exitosamente.",
                    link="/revenue",
                    icon="payment"
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
                            
                            # Send notification to affiliate
                            await create_notification_internal(
                                user_email=affiliate['email'],
                                notification_type="affiliate",
                                title=" ¡Nueva Comisión Ganada!",
                                message=f"Has ganado ${commission_amount:.2f} en comisiones por una nueva venta.",
                                link="/affiliate-dashboard",
                                icon="affiliate"
                            )
                            
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
    """
    Handle Stripe webhooks with full event processing, logging and retry logic
    
    Supported Events:
    - checkout.session.completed
    - payment_intent.succeeded
    - payment_intent.payment_failed
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    # Get webhook secret
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        # Get request body and signature
        body = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        if not sig_header:
            logger.warning("Webhook received without signature")
            raise HTTPException(status_code=400, detail="Missing Stripe signature")
        
        # Verify webhook signature (only if webhook_secret is configured)
        event = None
        if webhook_secret and webhook_secret != "whsec_your_webhook_secret_here":
            try:
                event = stripe.Webhook.construct_event(
                    body, sig_header, webhook_secret
                )
                logger.info(f"✓ Webhook signature verified for event: {event['id']}")
            except stripe.error.SignatureVerificationError as e:
                logger.error(f" Webhook signature verification failed: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid signature")
        else:
            # Parse event without verification (development only)
            logger.warning(" Webhook secret not configured - skipping signature verification")
            import json
            event = json.loads(body)
        
        # Extract event data
        event_id = event['id']
        event_type = event['type']
        event_data = event['data']['object']
        
        logger.info(f" Processing webhook: {event_type} (ID: {event_id})")
        
        # Log webhook to database
        webhook_log = WebhookLog(
            event_id=event_id,
            event_type=event_type,
            payload=event,
            status="received"
        )
        
        log_doc = webhook_log.model_dump()
        log_doc['created_at'] = log_doc['created_at'].isoformat()
        log_doc['updated_at'] = log_doc['updated_at'].isoformat()
        
        # Check for duplicate events
        existing_log = await db.webhook_logs.find_one({"event_id": event_id}, {"_id": 0})
        if existing_log:
            logger.info(f"  Duplicate event {event_id} - already processed")
            return {"status": "success", "message": "Duplicate event ignored"}
        
        await db.webhook_logs.insert_one(log_doc)
        
        # Process event based on type
        try:
            if event_type == 'checkout.session.completed':
                await handle_checkout_completed(event_data, event_id)
                
            elif event_type == 'payment_intent.succeeded':
                await handle_payment_succeeded(event_data, event_id)
                
            elif event_type == 'payment_intent.payment_failed':
                await handle_payment_failed(event_data, event_id)
                
            elif event_type == 'customer.subscription.created':
                await handle_subscription_created(event_data, event_id)
                
            elif event_type == 'customer.subscription.updated':
                await handle_subscription_updated(event_data, event_id)
                
            elif event_type == 'customer.subscription.deleted':
                await handle_subscription_deleted(event_data, event_id)
                
            elif event_type == 'invoice.payment_succeeded':
                await handle_invoice_paid(event_data, event_id)
                
            elif event_type == 'invoice.payment_failed':
                await handle_invoice_failed(event_data, event_id)
            
            else:
                logger.info(f"  Unhandled event type: {event_type}")
            
            # Mark webhook as processed
            await db.webhook_logs.update_one(
                {"event_id": event_id},
                {"$set": {
                    "status": "processed",
                    "processed_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            logger.info(f" Successfully processed webhook: {event_type}")
            return {"status": "success", "event_type": event_type, "event_id": event_id}
            
        except Exception as processing_error:
            # Mark webhook as failed
            error_msg = str(processing_error)
            logger.error(f" Error processing webhook {event_id}: {error_msg}")
            
            await db.webhook_logs.update_one(
                {"event_id": event_id},
                {"$set": {
                    "status": "failed",
                    "error_message": error_msg,
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            # Don't return error to Stripe - we logged it and will retry manually
            return {"status": "error", "message": "Processing failed but logged for retry"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f" Webhook endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Webhook event handlers
async def handle_checkout_completed(session_data: dict, event_id: str):
    """Handle checkout.session.completed event"""
    session_id = session_data.get('id')
    payment_status = session_data.get('payment_status')
    
    logger.info(f" Checkout completed: {session_id} - Status: {payment_status}")
    
    # Update transaction
    result = await db.payment_transactions.update_one(
        {"session_id": session_id},
        {"$set": {
            "payment_status": "paid" if payment_status == "paid" else payment_status,
            "status": "completed" if payment_status == "paid" else "pending",
            "payment_id": session_id,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    if result.modified_count > 0:
        logger.info(f"✓ Transaction updated for session {session_id}")
    else:
        logger.warning(f" No transaction found for session {session_id}")

async def handle_payment_succeeded(payment_intent: dict, event_id: str):
    """Handle payment_intent.succeeded event"""
    payment_id = payment_intent.get('id')
    amount = payment_intent.get('amount', 0) / 100  # Convert from cents
    
    logger.info(f" Payment succeeded: {payment_id} - Amount: ${amount}")
    
    # Additional processing if needed
    # This is more for direct PaymentIntents not through Checkout

async def handle_payment_failed(payment_intent: dict, event_id: str):
    """Handle payment_intent.payment_failed event"""
    payment_id = payment_intent.get('id')
    error = payment_intent.get('last_payment_error', {})
    
    logger.warning(f" Payment failed: {payment_id} - Error: {error.get('message', 'Unknown')}")

async def handle_subscription_created(subscription: dict, event_id: str):
    """Handle customer.subscription.created event"""
    subscription_id = subscription.get('id')
    customer_email = subscription.get('customer_email')
    
    logger.info(f" Subscription created: {subscription_id} for {customer_email}")
    
    # Create or update subscription record
    # This is backup in case checkout didn't create it

async def handle_subscription_updated(subscription: dict, event_id: str):
    """Handle customer.subscription.updated event"""
    subscription_id = subscription.get('id')
    status = subscription.get('status')
    
    logger.info(f" Subscription updated: {subscription_id} - Status: {status}")
    
    # Update subscription status in our database
    await db.subscriptions.update_one(
        {"stripe_subscription_id": subscription_id},
        {"$set": {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )

async def handle_subscription_deleted(subscription: dict, event_id: str):
    """Handle customer.subscription.deleted event"""
    subscription_id = subscription.get('id')
    
    logger.info(f" Subscription deleted: {subscription_id}")
    
    # Mark subscription as cancelled
    await db.subscriptions.update_one(
        {"stripe_subscription_id": subscription_id},
        {"$set": {
            "status": "cancelled",
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )

async def handle_invoice_paid(invoice: dict, event_id: str):
    """Handle invoice.payment_succeeded event"""
    invoice_id = invoice.get('id')
    amount = invoice.get('amount_paid', 0) / 100
    
    logger.info(f"📄 Invoice paid: {invoice_id} - Amount: ${amount}")

async def handle_invoice_failed(invoice: dict, event_id: str):
    """Handle invoice.payment_failed event"""
    invoice_id = invoice.get('id')
    
    logger.warning(f" Invoice payment failed: {invoice_id}")

@api_router.get("/webhooks/logs")
async def get_webhook_logs(status: Optional[str] = None, limit: int = 50):
    """Get webhook logs for monitoring"""
    query = {}
    if status:
        query["status"] = status
    
    logs = await db.webhook_logs.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    for log in logs:
        if isinstance(log.get('created_at'), str):
            log['created_at'] = datetime.fromisoformat(log['created_at'])
        if log.get('processed_at') and isinstance(log['processed_at'], str):
            log['processed_at'] = datetime.fromisoformat(log['processed_at'])
        if isinstance(log.get('updated_at'), str):
            log['updated_at'] = datetime.fromisoformat(log['updated_at'])
 @apirouter.post("/agent/chat")
async def agentexecutecommand(request: AgentExecuteRequest):
    resultado = await agente.procesarcomando(command=request.command, userid=request.userid)
    acciones = resultado.get("acciones", [])
    ai_response = resultado.get("response") or "Sin respuesta generada."
    if acciones:
        resumen_acciones = []
        for accion in acciones:
            herramienta = accion.get("herramienta", "desconocida")
            exito = accion.get("success", False)
            if exito:
                resumen_acciones.append(
                    f"✅ {herramienta}: Éxito real. Detalle: {accion.get('detalle', accion)}"
                )
            else:
                resumen_acciones.append(
                    f"❌ {herramienta}: Fallo. Motivo: {accion.get('error', 'No especificado')}"
                )
        ai_response += "\n\n" + "\n".join(resumen_acciones)
    return {
        "success": resultado.get("success", True),
        "response": ai_response,
        "acciones": acciones,
        "accionesejecutadas": len(acciones),
        "timestamp": resultado.get("timestamp", datetime.now(timezone.utc).isoformat())
    }
   
    return logs

@api_router.post("/webhooks/{event_id}/retry")
async def retry_webhook(event_id: str):
    """Manually retry a failed webhook"""
    webhook_log = await db.webhook_logs.find_one({"event_id": event_id}, {"_id": 0})
    
    if not webhook_log:
        raise HTTPException(status_code=404, detail="Webhook log not found")
    
    if webhook_log['status'] not in ['failed', 'retrying']:
        raise HTTPException(status_code=400, detail="Webhook not in failed state")
    
    # Update retry count
    retry_count = webhook_log.get('retry_count', 0) + 1
    
    await db.webhook_logs.update_one(
        {"event_id": event_id},
        {"$set": {
            "status": "retrying",
            "retry_count": retry_count,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    # Re-process the event
    try:
        event_data = webhook_log['payload']['data']['object']
        event_type = webhook_log['event_type']
        
        # Call appropriate handler
        if event_type == 'checkout.session.completed':
            await handle_checkout_completed(event_data, event_id)
        # Add other handlers as needed
        
        # Mark as processed
        await db.webhook_logs.update_one(
            {"event_id": event_id},
            {"$set": {
                "status": "processed",
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {"message": "Webhook retried successfully", "retry_count": retry_count}
        
    except Exception as e:
        # Mark as failed again
        await db.webhook_logs.update_one(
            {"event_id": event_id},
            {"$set": {
                "status": "failed",
                "error_message": str(e),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        raise HTTPException(status_code=500, detail=f"Retry failed: {str(e)}")

@api_router.get("/webhooks/stats")
async def get_webhook_stats():
    """Get webhook statistics"""
    all_logs = await db.webhook_logs.find({}, {"_id": 0}).to_list(1000)
    
    total = len(all_logs)
    by_status = {}
    by_type = {}
    
    for log in all_logs:
        status = log['status']
        event_type = log['event_type']
        
        by_status[status] = by_status.get(status, 0) + 1
        by_type[event_type] = by_type.get(event_type, 0) + 1
    
    failed = by_status.get('failed', 0)
    success_rate = round(((total - failed) / total * 100), 2) if total > 0 else 0
    
    return {
        "total_webhooks": total,
        "by_status": by_status,
        "by_type": by_type,
        "success_rate": success_rate,
        "failed_count": failed
    }

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
        budget = campaign.get('budget', 0)
        
        # Calculate revenue during campaign period
        campaign_start = campaign.get('start_date')
        campaign_end = campaign.get('end_date')
        
        if not campaign_start or not campaign_end:
            continue
        
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

@api_router.get("/analytics/dashboard-enhanced")
async def get_enhanced_dashboard(days: int = 30):
    """
    Get enhanced dashboard with time-series data for charts
    Supports filtering by number of days (7, 30, 90, etc.)
    """
    try:
        # Calculate date range
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # Previous period for comparison
        previous_start = start_date - timedelta(days=days)
        previous_end = start_date
        
        # Query filters
        current_filter = {"created_at": {"$gte": start_date.isoformat(), "$lte": end_date.isoformat()}}
        previous_filter = {"created_at": {"$gte": previous_start.isoformat(), "$lte": previous_end.isoformat()}}
        
        # === REVENUE METRICS ===
        current_transactions = await db.payment_transactions.find({
            **current_filter,
            "payment_status": "paid"
        }, {"_id": 0}).to_list(1000)
        
        previous_transactions = await db.payment_transactions.find({
            **previous_filter,
            "payment_status": "paid"
        }, {"_id": 0}).to_list(1000)
        
        current_revenue = sum(t.get('amount', 0) for t in current_transactions)
        previous_revenue = sum(t.get('amount', 0) for t in previous_transactions)
        
        revenue_change = 0
        if previous_revenue > 0:
            revenue_change = round(((current_revenue - previous_revenue) / previous_revenue) * 100, 2)
        
        # === AFFILIATE METRICS ===
        total_affiliates = await db.affiliates.count_documents({})
        active_affiliates = await db.affiliates.count_documents({"status": "active"})
        
        current_commissions = await db.affiliate_commissions.find(current_filter, {"_id": 0}).to_list(1000)
        previous_commissions = await db.affiliate_commissions.find(previous_filter, {"_id": 0}).to_list(1000)
        
        current_commission_amount = sum(c.get('commission_amount', 0) for c in current_commissions)
        previous_commission_amount = sum(c.get('commission_amount', 0) for c in previous_commissions)
        
        commission_change = 0
        if previous_commission_amount > 0:
            commission_change = round(((current_commission_amount - previous_commission_amount) / previous_commission_amount) * 100, 2)
        
        # Total clicks from affiliate links
        all_links = await db.affiliate_links.find({}, {"_id": 0}).to_list(1000)
        total_clicks = sum(link.get('clicks', 0) for link in all_links)
        
        # === CART ABANDONMENT (Simulated for now) ===
        # In a real scenario, you'd track cart sessions
        simulated_carts = {
            "total_carts": 150,
            "abandoned": 95,
            "recovered": 12,
            "abandonment_rate": 63.3,
            "recovery_rate": 12.6
        }
        
        # === A/B TESTS (Simulated) ===
        simulated_ab_tests = {
            "active_tests": 3,
            "completed_tests": 12,
            "total_tests": 15,
            "avg_improvement": 18.5
        }
        
        # === EMAIL CAMPAIGNS (Simulated) ===
        simulated_email = {
            "active_campaigns": 2,
            "emails_sent": 5420,
            "open_rate": 24.5,
            "click_rate": 3.8,
            "conversion_rate": 1.2
        }
        
        # === PRODUCTS & CAMPAIGNS ===
        products_count = await db.products.count_documents({})
        featured_products = await db.products.count_documents({"is_featured": True})
        
        active_campaigns = await db.campaigns.count_documents({"status": "active"})
        total_campaigns = await db.campaigns.count_documents({})
        
        # === TIME-SERIES DATA FOR CHARTS ===
        # Revenue over time (daily for last period)
        revenue_timeline = []
        for i in range(days):
            day = start_date + timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_transactions = [t for t in current_transactions 
                              if day_start.isoformat() <= t.get('created_at', '') < day_end.isoformat()]
            
            day_revenue = sum(t.get('amount', 0) for t in day_transactions)
            
            revenue_timeline.append({
                "date": day.strftime("%Y-%m-%d"),
                "revenue": round(day_revenue, 2),
                "transactions": len(day_transactions)
            })
        
        # === CONVERSION SOURCES (for pie chart) ===
        conversion_sources = {
            "organic": 45,
            "paid_ads": 30,
            "affiliates": 15,
            "email": 7,
            "social": 3
        }
        
        # === TOP PERFORMING CAMPAIGNS ===
        campaigns = await db.campaigns.find({}, {"_id": 0}).sort("created_at", -1).limit(5).to_list(5)
        campaign_performance = []
        for campaign in campaigns:
            perf = campaign.get('performance', {})
            campaign_performance.append({
                "name": campaign.get('name', 'Campaign'),
                "impressions": perf.get('impressions', 0),
                "clicks": perf.get('clicks', 0),
                "conversions": perf.get('conversions', 0),
                "spend": campaign.get('budget', 0)
            })
        
        return {
            "period": {
                "days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "metrics": {
                "revenue": {
                    "current": round(current_revenue, 2),
                    "previous": round(previous_revenue, 2),
                    "change_percent": revenue_change,
                    "is_positive": revenue_change >= 0
                },
                "transactions": {
                    "current": len(current_transactions),
                    "previous": len(previous_transactions),
                    "change_percent": round(((len(current_transactions) - len(previous_transactions)) / max(len(previous_transactions), 1)) * 100, 2) if len(previous_transactions) > 0 else 0
                },
                "affiliates": {
                    "total": total_affiliates,
                    "active": active_affiliates,
                    "total_clicks": total_clicks,
                    "commission_amount": round(current_commission_amount, 2),
                    "change_percent": commission_change
                },
                "products": {
                    "total": products_count,
                    "featured": featured_products
                },
                "campaigns": {
                    "active": active_campaigns,
                    "total": total_campaigns
                },
                "cart_abandonment": simulated_carts,
                "ab_tests": simulated_ab_tests,
                "email_campaigns": simulated_email
            },
            "charts": {
                "revenue_timeline": revenue_timeline,
                "conversion_sources": conversion_sources,
                "campaign_performance": campaign_performance
            },
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Enhanced dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get enhanced dashboard: {str(e)}")

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
# ROUTES - Notifications System
# =========================

async def send_telegram_notification(title: str, message: str, link: Optional[str] = None):
    """Send notification to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured")
        return False
    
    try:
        # Format message with HTML
        text = f"<b>{title}</b>\n\n{message}"
        
        if link:
            # Add link if provided
            base_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
            full_link = f"{base_url}{link}"
            text += f"\n\n🔗 <a href='{full_link}'>Ver más</a>"
        
        # Send message via Telegram Bot API
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Telegram notification sent successfully: {title}")
            return True
        else:
            logger.error(f"Telegram API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {str(e)}")
        return False

async def create_notification_internal(
    user_email: str,
    notification_type: str,
    title: str,
    message: str,
    link: Optional[str] = None,
    icon: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Internal helper to create notifications"""
    try:
        # Check user preferences
        prefs = await db.notification_preferences.find_one({"user_email": user_email}, {"_id": 0})
        
        if not prefs:
            # Create default preferences
            default_prefs = NotificationPreferences(user_email=user_email)
            prefs_doc = default_prefs.model_dump()
            prefs_doc['created_at'] = prefs_doc['created_at'].isoformat()
            prefs_doc['updated_at'] = prefs_doc['updated_at'].isoformat()
            await db.notification_preferences.insert_one(prefs_doc)
            prefs = default_prefs.model_dump()
        
        # Check if user wants this type of notification
        type_map = {
            "payment": prefs.get('notify_payments', True),
            "affiliate": prefs.get('notify_affiliates', True),
            "campaign": prefs.get('notify_campaigns', True),
            "product": prefs.get('notify_products', True),
            "subscription": prefs.get('notify_subscriptions', True),
            "system": prefs.get('notify_system', True)
        }
        
        if notification_type in type_map and not type_map[notification_type]:
            logger.info(f"Notification type {notification_type} disabled for {user_email}")
            return None
        
        # Create notification
        notification = Notification(
            user_email=user_email,
            type=notification_type,
            title=title,
            message=message,
            link=link,
            icon=icon,
            metadata=metadata or {}
        )
        
        doc = notification.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        if doc.get('read_at'):
            doc['read_at'] = doc['read_at'].isoformat()
        
        await db.notifications.insert_one(doc)
        
        # Send Telegram notification if enabled
        if prefs.get('telegram_notifications', True):
            await send_telegram_notification(title, message, link)
        
        # TODO: Send email if email_notifications enabled
        # TODO: Send push notification if push_notifications enabled
        
        logger.info(f"Created notification for {user_email}: {title}")
        return notification
        
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        return None

@api_router.post("/notifications", response_model=Notification)
async def create_notification(data: NotificationCreate):
    """Create a new notification (admin/system endpoint)"""
    try:
        notification = await create_notification_internal(
            user_email=data.user_email,
            notification_type=data.type,
            title=data.title,
            message=data.message,
            link=data.link,
            icon=data.icon,
            metadata=data.metadata
        )
        
        if not notification:
            raise HTTPException(status_code=400, detail="Notification could not be created")
        
        return notification
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Notification creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/notifications")
async def get_notifications(
    user_email: str,
    unread_only: bool = False,
    limit: int = 50,
    skip: int = 0
):
    """Get user notifications"""
    try:
        query = {"user_email": user_email, "is_archived": False}
        
        if unread_only:
            query["is_read"] = False
        
        notifications = await db.notifications.find(
            query,
            {"_id": 0}
        ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Parse dates
        for notif in notifications:
            if isinstance(notif.get('created_at'), str):
                notif['created_at'] = datetime.fromisoformat(notif['created_at'])
            if notif.get('read_at') and isinstance(notif['read_at'], str):
                notif['read_at'] = datetime.fromisoformat(notif['read_at'])
        
        return notifications
        
    except Exception as e:
        logger.error(f"Get notifications error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/notifications/count")
async def get_unread_count(user_email: str):
    """Get count of unread notifications"""
    try:
        count = await db.notifications.count_documents({
            "user_email": user_email,
            "is_read": False,
            "is_archived": False
        })
        
        return {"unread_count": count}
        
    except Exception as e:
        logger.error(f"Get unread count error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.patch("/notifications/{notification_id}/read")
async def mark_as_read(notification_id: str):
    """Mark notification as read"""
    try:
        result = await db.notifications.update_one(
            {"id": notification_id},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"message": "Notification marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Mark as read error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.patch("/notifications/read-all")
async def mark_all_as_read(user_email: str):
    """Mark all notifications as read"""
    try:
        result = await db.notifications.update_many(
            {"user_email": user_email, "is_read": False},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        return {
            "message": f"Marked {result.modified_count} notifications as read",
            "count": result.modified_count
        }
        
    except Exception as e:
        logger.error(f"Mark all as read error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: str):
    """Delete (archive) a notification"""
    try:
        result = await db.notifications.update_one(
            {"id": notification_id},
            {"$set": {"is_archived": True}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"message": "Notification archived"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete notification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/notifications/preferences")
async def get_notification_preferences(user_email: str):
    """Get user notification preferences"""
    try:
        prefs = await db.notification_preferences.find_one({"user_email": user_email}, {"_id": 0})
        
        if not prefs:
            # Create default preferences
            default_prefs = NotificationPreferences(user_email=user_email)
            prefs_doc = default_prefs.model_dump()
            prefs_doc['created_at'] = prefs_doc['created_at'].isoformat()
            prefs_doc['updated_at'] = prefs_doc['updated_at'].isoformat()
            await db.notification_preferences.insert_one(prefs_doc)
            return default_prefs
        
        # Parse dates
        if isinstance(prefs.get('created_at'), str):
            prefs['created_at'] = datetime.fromisoformat(prefs['created_at'])
        if isinstance(prefs.get('updated_at'), str):
            prefs['updated_at'] = datetime.fromisoformat(prefs['updated_at'])
        
        return prefs
        
    except Exception as e:
        logger.error(f"Get preferences error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.patch("/notifications/preferences")
async def update_notification_preferences(
    user_email: str,
    preferences: NotificationPreferencesUpdate
):
    """Update user notification preferences"""
    try:
        # Get existing preferences
        existing = await db.notification_preferences.find_one({"user_email": user_email}, {"_id": 0})
        
        if not existing:
            # Create new preferences
            new_prefs = NotificationPreferences(user_email=user_email)
            prefs_dict = new_prefs.model_dump()
        else:
            prefs_dict = existing
        
        # Update with provided values
        update_data = preferences.model_dump(exclude_unset=True)
        prefs_dict.update(update_data)
        prefs_dict['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        # Upsert
        await db.notification_preferences.update_one(
            {"user_email": user_email},
            {"$set": prefs_dict},
            upsert=True
        )
        
        return {"message": "Preferences updated successfully", "preferences": prefs_dict}
        
    except Exception as e:
        logger.error(f"Update preferences error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# ROUTES - AI Recommendations System
# =========================

async def generate_product_embedding(product: dict) -> List[float]:
    """Generate OpenAI embedding for a product"""
    if not openai_client:
        logger.warning("OpenAI client not configured")
        return []
    
    try:
        # Create text representation of product
        text = f"{product['name']} {product['description']} {product.get('category', '')}"
        
        # Generate embedding
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        
        embedding = response.data[0].embedding
        
        # Store in database
        embedding_doc = {
            "product_id": product['id'],
            "embedding": embedding,
            "text_used": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.product_embeddings.update_one(
            {"product_id": product['id']},
            {"$set": embedding_doc},
            upsert=True
        )
        
        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return []

async def get_similarity_recommendations(
    user_email: str,
    limit: int = 10,
    category: Optional[str] = None
) -> List[dict]:
    """Get recommendations based on embedding similarity"""
    try:
        # Get user's recent interactions
        interactions = await db.user_interactions.find(
            {"user_email": user_email},
            {"_id": 0}
        ).sort("created_at", -1).limit(5).to_list(5)
        
        if not interactions:
            # No interactions, return popular products
            return await get_popular_products(limit, category)
        
        # Get products user interacted with
        interacted_product_ids = [i['product_id'] for i in interactions]
        interacted_products = await db.products.find(
            {"id": {"$in": interacted_product_ids}},
            {"_id": 0}
        ).to_list(len(interacted_product_ids))
        
        if not interacted_products:
            return await get_popular_products(limit, category)
        
        # Get embeddings for interacted products
        interacted_embeddings = []
        for product in interacted_products:
            embedding_doc = await db.product_embeddings.find_one(
                {"product_id": product['id']},
                {"_id": 0}
            )
            
            if not embedding_doc:
                # Generate if doesn't exist
                embedding = await generate_product_embedding(product)
                if embedding:
                    interacted_embeddings.append(embedding)
            else:
                interacted_embeddings.append(embedding_doc['embedding'])
        
        if not interacted_embeddings:
            return await get_popular_products(limit, category)
        
        # Calculate average embedding of user's interests
        avg_embedding = np.mean(interacted_embeddings, axis=0)
        
        # Get all products (excluding already interacted)
        query = {"id": {"$nin": interacted_product_ids}}
        if category:
            query["category"] = category
        
        all_products = await db.products.find(query, {"_id": 0}).to_list(1000)
        
        # Get/generate embeddings for all products
        recommendations = []
        for product in all_products:
            embedding_doc = await db.product_embeddings.find_one(
                {"product_id": product['id']},
                {"_id": 0}
            )
            
            if not embedding_doc:
                embedding = await generate_product_embedding(product)
                if not embedding:
                    continue
            else:
                embedding = embedding_doc['embedding']
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                [avg_embedding],
                [embedding]
            )[0][0]
            
            recommendations.append({
                "product": product,
                "score": float(similarity),
                "reason": "Similar a tus productos vistos",
                "algorithm": "similarity"
            })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
        
    except Exception as e:
        logger.error(f"Error in similarity recommendations: {str(e)}")
        return []

async def get_collaborative_recommendations(
    user_email: str,
    limit: int = 10,
    category: Optional[str] = None
) -> List[dict]:
    """Get recommendations based on collaborative filtering"""
    try:
        # Get user's interactions
        user_interactions = await db.user_interactions.find(
            {"user_email": user_email},
            {"_id": 0}
        ).to_list(1000)
        
        if not user_interactions:
            return await get_popular_products(limit, category)
        
        # Get products user interacted with
        user_product_ids = set([i['product_id'] for i in user_interactions])
        
        # Find similar users (users who interacted with same products)
        similar_users_cursor = db.user_interactions.aggregate([
            {"$match": {"product_id": {"$in": list(user_product_ids)}, "user_email": {"$ne": user_email}}},
            {"$group": {"_id": "$user_email", "common_products": {"$addToSet": "$product_id"}}},
            {"$project": {"user_email": "$_id", "overlap": {"$size": "$common_products"}, "_id": 0}},
            {"$sort": {"overlap": -1}},
            {"$limit": 10}
        ])
        
        similar_users = await similar_users_cursor.to_list(10)
        
        if not similar_users:
            return await get_popular_products(limit, category)
        
        similar_user_emails = [u['user_email'] for u in similar_users]
        
        # Get products these similar users interacted with
        similar_user_interactions = await db.user_interactions.find(
            {
                "user_email": {"$in": similar_user_emails},
                "product_id": {"$nin": list(user_product_ids)}
            },
            {"_id": 0}
        ).to_list(1000)
        
        # Count product interactions and calculate scores
        product_scores = {}
        for interaction in similar_user_interactions:
            product_id = interaction['product_id']
            score = interaction.get('interaction_score', 1.0)
            
            if product_id not in product_scores:
                product_scores[product_id] = 0
            product_scores[product_id] += score
        
        # Get top products
        top_product_ids = sorted(product_scores.keys(), key=lambda x: product_scores[x], reverse=True)[:limit]
        
        # Fetch product details
        query = {"id": {"$in": top_product_ids}}
        if category:
            query["category"] = category
        
        products = await db.products.find(query, {"_id": 0}).to_list(limit)
        
        # Create recommendations
        recommendations = []
        for product in products:
            recommendations.append({
                "product": product,
                "score": product_scores[product['id']],
                "reason": "Usuarios similares también compraron esto",
                "algorithm": "collaborative"
            })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error in collaborative recommendations: {str(e)}")
        return []

async def get_popular_products(limit: int = 10, category: Optional[str] = None) -> List[dict]:
    """Get popular products as fallback"""
    try:
        # Count interactions per product
        pipeline = [
            {"$group": {"_id": "$product_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit * 2}  # Get more to filter by category
        ]
        
        popular_cursor = db.user_interactions.aggregate(pipeline)
        popular = await popular_cursor.to_list(limit * 2)
        
        if not popular:
            # No interactions, return featured products
            query = {"is_featured": True}
            if category:
                query["category"] = category
            products = await db.products.find(query, {"_id": 0}).limit(limit).to_list(limit)
        else:
            product_ids = [p['_id'] for p in popular]
            query = {"id": {"$in": product_ids}}
            if category:
                query["category"] = category
            products = await db.products.find(query, {"_id": 0}).to_list(limit)
        
        recommendations = []
        for product in products[:limit]:
            recommendations.append({
                "product": product,
                "score": 1.0,
                "reason": "Producto popular",
                "algorithm": "popular"
            })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting popular products: {str(e)}")
        return []

@api_router.post("/recommendations/track")
async def track_interaction(
    user_email: str,
    product_id: str,
    interaction_type: str,  # view, click, purchase, add_to_cart
    session_id: Optional[str] = None
):
    """Track user interaction for recommendations"""
    try:
        # Define interaction scores
        score_map = {
            "view": 0.5,
            "click": 1.0,
            "add_to_cart": 2.0,
            "purchase": 5.0,
            "wishlist": 1.5
        }
        
        interaction = {
            "id": str(uuid.uuid4()),
            "user_email": user_email,
            "product_id": product_id,
            "interaction_type": interaction_type,
            "interaction_score": score_map.get(interaction_type, 1.0),
            "session_id": session_id,
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.user_interactions.insert_one(interaction)
        
        return {
            "message": "Interaction tracked",
            "interaction_id": interaction['id']
        }
        
    except Exception as e:
        logger.error(f"Error tracking interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get personalized product recommendations"""
    try:
        if request.algorithm == "similarity":
            recommendations = await get_similarity_recommendations(
                request.user_email,
                request.limit,
                request.category
            )
        elif request.algorithm == "collaborative":
            recommendations = await get_collaborative_recommendations(
                request.user_email,
                request.limit,
                request.category
            )
        else:  # hybrid
            # Get both types and merge
            similarity_recs = await get_similarity_recommendations(
                request.user_email,
                request.limit // 2 + 1,
                request.category
            )
            collaborative_recs = await get_collaborative_recommendations(
                request.user_email,
                request.limit // 2 + 1,
                request.category
            )
            
            # Merge and deduplicate
            all_recs = similarity_recs + collaborative_recs
            seen_ids = set()
            recommendations = []
            for rec in all_recs:
                if rec['product']['id'] not in seen_ids:
                    seen_ids.add(rec['product']['id'])
                    recommendations.append(rec)
                    if len(recommendations) >= request.limit:
                        break
        
        # Format response
        response = []
        for rec in recommendations:
            product = rec['product']
            response.append(RecommendationResponse(
                product_id=product['id'],
                product_name=product['name'],
                product_description=product['description'],
                product_price=product['price'],
                product_image=product.get('image_url'),
                product_category=product['category'],
                score=rec['score'],
                reason=rec['reason'],
                algorithm_used=rec['algorithm']
            ))
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/recommendations/generate-embeddings")
async def generate_all_embeddings():
    """Generate embeddings for all products (admin endpoint)"""
    try:
        if not openai_client:
            raise HTTPException(status_code=503, detail="OpenAI not configured")
        
        products = await db.products.find({}, {"_id": 0}).to_list(1000)
        
        generated = 0
        skipped = 0
        
        for product in products:
            # Check if embedding already exists
            existing = await db.product_embeddings.find_one({"product_id": product['id']})
            if existing:
                skipped += 1
                continue
            
            embedding = await generate_product_embedding(product)
            if embedding:
                generated += 1
        
        return {
            "message": "Embeddings generation complete",
            "generated": generated,
            "skipped": skipped,
            "total": len(products)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
        content['content'] = " Contenido Premium - Actualiza tu membresía para acceder"
    
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
# DATABASE MANAGEMENT ENDPOINTS
# =========================

@api_router.get("/database/info")
async def get_database_info():
    """Get database statistics and collection info"""
    try:
        collections = await db.list_collection_names()
        
        # Get collection stats
        collection_stats = {}
        for col_name in collections:
            if col_name != "_migrations":  # Skip internal collection
                stats = await db.command("collStats", col_name)
                collection_stats[col_name] = {
                    "count": stats.get("count", 0),
                    "size_mb": round(stats.get("size", 0) / (1024 * 1024), 2),
                    "indexes": stats.get("nindexes", 0)
                }
        
        # Get migration info
        migrations_cursor = db["_migrations"].find({}, {'_id': 0})  # Exclude ObjectId
        migrations = await migrations_cursor.to_list(length=None)
        
        # Convert datetime to string for JSON serialization
        last_migration = None
        if migrations:
            last = migrations[-1]
            last_migration = {
                'migration_id': last.get('migration_id'),
                'description': last.get('description'),
                'applied_at': last.get('applied_at').isoformat() if last.get('applied_at') else None
            }
        
        return {
            "database_name": os.environ['DB_NAME'],
            "collections_count": len(collections),
            "collections": collection_stats,
            "migrations_applied": len(migrations),
            "last_migration": last_migration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database info error: {str(e)}")
        
async def get_external_saas(url, params=None):
    """Conexión ultra-flexible a cualquier API externa/interna/SaaS (GET)"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params or {}, timeout=20) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                error = await resp.text()
                return {"error": error}


@api_router.post("/database/backup")
async def create_database_backup(background_tasks: BackgroundTasks):
    """Create a database backup (runs in background)"""
    try:
        from database.backup import MongoBackupManager
        
        def run_backup():
            manager = MongoBackupManager(
                mongo_url=os.environ['MONGO_URL'],
                db_name=os.environ['DB_NAME']
            )
            manager.run_backup_job()
        
        background_tasks.add_task(run_backup)
        
        return {
            "message": "Backup job started in background",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")


@api_router.get("/database/backups")
async def list_database_backups():
    """List available database backups"""
    try:
        from database.backup import MongoBackupManager
        
        manager = MongoBackupManager(
            mongo_url=os.environ['MONGO_URL'],
            db_name=os.environ['DB_NAME']
        )
        
        backups = manager.list_backups()
        
        return {
            "count": len(backups),
            "backups": backups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"List backups failed: {str(e)}")


@api_router.get("/database/indexes/{collection_name}")
async def get_collection_indexes(collection_name: str):
    """Get indexes for a specific collection"""
    try:
        collection = db[collection_name]
        indexes = await collection.index_information()
        
        return {
            "collection": collection_name,
            "indexes": indexes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get indexes failed: {str(e)}")

# =========================
# SECURITY ENDPOINTS
# =========================

# API Keys Management
@api_router.post("/api-keys", status_code=201)
async def create_api_key(
    request: Request,
    name: str,
    scopes: List[str] = [],
    expires_in_days: Optional[int] = None
):
    """Create a new API key"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    try:
        api_key_obj, plain_key = await api_key_manager.create_api_key(
            user_email=user_email,
            name=name,
            scopes=scopes,
            expires_in_days=expires_in_days
        )
        
        # Log the action
        await audit_logger.log_from_request(
            request,
            action="apikey.create",
            resource_type="api_key",
            resource_id=api_key_obj.id,
            details={"name": name, "scopes": scopes}
        )
        
        return {
            "id": api_key_obj.id,
            "name": api_key_obj.name,
            "key": plain_key,  # Only shown once!
            "key_prefix": api_key_obj.key_prefix,
            "scopes": api_key_obj.scopes,
            "expires_at": api_key_obj.expires_at,
            "created_at": api_key_obj.created_at,
            "warning": "Save this key securely. It will not be shown again."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/api-keys")
async def list_api_keys():
    """List all API keys for current user"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    keys = await api_key_manager.list_api_keys(user_email)
    return {"keys": [k.model_dump() for k in keys]}


@api_router.delete("/api-keys/{key_id}")
async def revoke_api_key(key_id: str, request: Request):
    """Revoke an API key"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    success = await api_key_manager.revoke_api_key(key_id, user_email)
    
    if success:
        await audit_logger.log_from_request(
            request,
            action="apikey.revoke",
            resource_type="api_key",
            resource_id=key_id
        )
        return {"message": "API key revoked successfully"}
    
    raise HTTPException(status_code=404, detail="API key not found")


@api_router.post("/api-keys/{key_id}/rotate")
async def rotate_api_key(key_id: str, request: Request):
    """Rotate an API key (create new, revoke old)"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    try:
        new_key_obj, plain_key = await api_key_manager.rotate_api_key(key_id, user_email)
        
        await audit_logger.log_from_request(
            request,
            action="apikey.rotate",
            resource_type="api_key",
            resource_id=key_id,
            details={"new_key_id": new_key_obj.id}
        )
        
        return {
            "id": new_key_obj.id,
            "name": new_key_obj.name,
            "key": plain_key,
            "key_prefix": new_key_obj.key_prefix,
            "expires_at": new_key_obj.expires_at,
            "warning": "Save this key securely. It will not be shown again."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Two-Factor Authentication
@api_router.post("/auth/2fa/setup")
async def setup_2fa(request: Request):
    """Setup 2FA for current user"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    try:
        setup_info = await two_factor_manager.setup_2fa(user_email)
        
        await audit_logger.log_from_request(
            request,
            action="auth.2fa_setup",
            resource_type="user",
            resource_id=user_email
        )
        
        return {
            "qr_code": setup_info.qr_code,
            "manual_entry_key": setup_info.manual_entry_key,
            "backup_codes": setup_info.backup_codes,
            "message": "Scan QR code with authenticator app, then verify with a code to enable 2FA"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/auth/2fa/enable")
async def enable_2fa(verification_code: str, request: Request):
    """Enable 2FA after verifying first code"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    success = await two_factor_manager.enable_2fa(user_email, verification_code)
    
    if success:
        await audit_logger.log_from_request(
            request,
            action="auth.2fa_enable",
            resource_type="user",
            resource_id=user_email
        )
        return {"message": "2FA enabled successfully"}
    
    raise HTTPException(status_code=400, detail="Invalid verification code")


@api_router.post("/auth/2fa/disable")
async def disable_2fa(verification_code: str, request: Request):
    """Disable 2FA"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    success = await two_factor_manager.disable_2fa(user_email, verification_code)
    
    if success:
        await audit_logger.log_from_request(
            request,
            action="auth.2fa_disable",
            resource_type="user",
            resource_id=user_email
        )
        return {"message": "2FA disabled successfully"}
    
    raise HTTPException(status_code=400, detail="Invalid verification code or 2FA not enabled")


@api_router.get("/auth/2fa/status")
async def get_2fa_status():
    """Get 2FA status for current user"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    status_info = await two_factor_manager.get_2fa_status(user_email)
    return status_info


@api_router.post("/auth/2fa/backup-codes/regenerate")
async def regenerate_backup_codes(verification_code: str, request: Request):
    """Regenerate backup codes"""
    user_email = "admin@example.com"  # TODO: Get from authenticated user
    
    new_codes = await two_factor_manager.regenerate_backup_codes(user_email, verification_code)
    
    if new_codes:
        await audit_logger.log_from_request(
            request,
            action="auth.2fa_backup_regenerate",
            resource_type="user",
            resource_id=user_email
        )
        return {"backup_codes": new_codes}
    
    raise HTTPException(status_code=400, detail="Invalid verification code")


# Audit Logs
@api_router.get("/audit-logs")
async def search_audit_logs(
    user_email: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    status: Optional[str] = None,
    days: int = 7,
    limit: int = 100
):
    """Search audit logs"""
    from datetime import timedelta
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    logs = await audit_logger.search_logs(
        user_email=user_email,
        action=action,
        resource_type=resource_type,
        status=status,
        start_date=start_date,
        limit=limit
    )
    
    return {"logs": [log.model_dump() for log in logs]}


@api_router.get("/audit-logs/stats")
async def get_audit_stats(days: int = 30):
    """Get audit log statistics"""
    stats = await audit_logger.get_stats(days=days)
    return stats


@api_router.get("/audit-logs/security-events")
async def get_security_events(days: int = 7, limit: int = 100):
    """Get recent security events"""
    events = await audit_logger.get_security_events(days=days, limit=limit)
    return {"events": [event.model_dump() for event in events]}


@api_router.get("/audit-logs/user/{user_email}")
async def get_user_activity(user_email: str, days: int = 30, limit: int = 100):
    """Get activity history for a user"""
    logs = await audit_logger.get_user_activity(user_email, days=days, limit=limit)
    return {"logs": [log.model_dump() for log in logs]}


# Rate Limiter Info
@api_router.get("/security/rate-limiter/stats")
async def get_rate_limiter_stats():
    """Get rate limiter statistics"""
    return rate_limiter.get_stats()


@api_router.post("/security/rate-limiter/reset/{identifier}")
async def reset_rate_limit(identifier: str):
    """Reset rate limit for an identifier (admin only)"""
    await rate_limiter.reset_identifier(identifier)
    return {"message": f"Rate limit reset for {identifier}"}


# Security Dashboard
@api_router.get("/security/dashboard")
async def get_security_dashboard():
    """Get comprehensive security dashboard"""
    # Get recent audit stats
    audit_stats = await audit_logger.get_stats(days=7)
    
    # Get security events
    security_events = await audit_logger.get_security_events(days=7, limit=20)
    
    # Get rate limiter stats
    rate_limiter_stats = rate_limiter.get_stats()
    
    # Get failed operations
    failed_ops = await audit_logger.get_failed_operations(days=7, limit=20)
    
    return {
        "audit_stats": audit_stats,
        "recent_security_events": [e.model_dump() for e in security_events],
        "rate_limiter": rate_limiter_stats,
        "recent_failures": [f.model_dump() for f in failed_ops]
    }

# =========================
# MONITORING & HEALTH CHECK ENDPOINTS
# =========================

@api_router.get("/health")
async def health_check():
    """Comprehensive health check"""
    result = await health_checker.check_all()
    status_code = 200 if result['status'] == 'healthy' else 503
    return JSONResponse(content=result, status_code=status_code)


@api_router.get("/health/liveness")
async def liveness_check():
    """Kubernetes liveness probe"""
    is_alive = await health_checker.liveness_probe()
    if is_alive:
        return {"status": "alive"}
    return JSONResponse(content={"status": "dead"}, status_code=503)


@api_router.get("/health/readiness")
async def readiness_check():
    """Kubernetes readiness probe"""
    is_ready = await health_checker.readiness_probe()
    if is_ready:
        return {"status": "ready"}
    return JSONResponse(content={"status": "not_ready"}, status_code=503)


@api_router.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    from fastapi.responses import PlainTextResponse
    metrics_text = metrics_collector.export_prometheus_format()
    return PlainTextResponse(content=metrics_text, media_type="text/plain")


@api_router.get("/metrics/summary")
async def metrics_summary():
    """Human-readable metrics summary"""
    return {
        "requests": metrics_collector.get_request_metrics(),
        "system": metrics_collector.get_system_metrics(),
        "custom": metrics_collector.get_custom_metrics()
    }


@api_router.get("/monitoring/dashboard")
async def monitoring_dashboard():
    """Complete monitoring dashboard"""
    # Health status
    health = await health_checker.check_all()
    
    # Metrics
    metrics = {
        "requests": metrics_collector.get_request_metrics(),
        "system": metrics_collector.get_system_metrics()
    }
    
    # Security stats
    security_stats = rate_limiter.get_stats()
    
    # Audit logs stats
    audit_stats = await audit_logger.get_stats(days=7)
    
    return {
        "health": health,
        "metrics": metrics,
        "security": security_stats,
        "audit": audit_stats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# =========================
# DROPSHIPPING & AI CONTENT GENERATION ENDPOINTS
# =========================

from integrations import (
    get_fal_client,
    get_woo_client,
    DropshippingPriceCalculator,
    create_dropshipping_system
)

# Initialize dropshipping system
dropshipping_system = None

def get_dropshipping_system():
    """Get or create dropshipping system"""
    global dropshipping_system
    if dropshipping_system is None:
        dropshipping_system = create_dropshipping_system(
            woo_client=get_woo_client(),
            fal_client=get_fal_client(),
            price_calculator=DropshippingPriceCalculator()
        )
    return dropshipping_system


# FAL AI Endpoints
@api_router.post("/ai/generate-image")
async def generate_product_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024
):
    """Generate product image with FAL AI"""
    try:
        fal = get_fal_client()
        result = await fal.text_to_image(prompt, width, height)
        
        return {
            "success": True,
            "request_id": result.get('request_id'),
            "message": "Image generation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/generate-video")
async def generate_product_video(
    prompt: str,
    duration: int = 5,
    resolution: str = "720p"
):
    """Generate product video with FAL AI"""
    try:
        fal = get_fal_client()
        result = await fal.text_to_video(prompt, duration, resolution)
        
        return {
            "success": True,
            "request_id": result.get('request_id'),
            "message": "Video generation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/ai/status/{request_id}")
async def check_generation_status(request_id: str):
    """Check FAL AI generation status"""
    try:
        fal = get_fal_client()
        status = await fal.get_status(request_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Pricing Endpoints
@api_router.post("/dropshipping/calculate-price")
async def calculate_selling_price(
    data: Dict
):
    """Calculate selling price with profit margin"""
    try:
        supplier_price = data.get('supplier_price')
        currency = data.get('currency', 'EUR')
        
        if not supplier_price:
            raise HTTPException(status_code=400, detail="supplier_price is required")
        
        calculator = DropshippingPriceCalculator()
        pricing = calculator.calculate_selling_price(float(supplier_price), currency)
        return pricing
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/dropshipping/margin-rules")
async def get_margin_rules():
    """Get profit margin rules"""
    calculator = DropshippingPriceCalculator()
    return {
        "margin_rules": calculator.get_margin_info(),
        "description": "Profit margins by price range"
    }


# WooCommerce Product Management
@api_router.get("/woocommerce/products")
async def get_woo_products(
    per_page: int = 20,
    page: int = 1,
    search: str = None
):
    """Get products from WooCommerce store"""
    try:
        woo = get_woo_client()
        products = woo.get_products(per_page, page, search)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/woocommerce/products/{product_id}")
async def get_woo_product(product_id: int):
    """Get single product from WooCommerce"""
    try:
        woo = get_woo_client()
        product = woo.get_product(product_id)
        return product
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api_router.put("/woocommerce/products/{product_id}/price")
async def update_product_price(
    product_id: int,
    regular_price: float,
    sale_price: float = None
):
    """Update product price"""
    try:
        woo = get_woo_client()
        result = woo.update_product_price(product_id, regular_price, sale_price)
        return {"success": True, "product": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/woocommerce/stats")
async def get_store_stats():
    """Get store sales statistics"""
    try:
        woo = get_woo_client()
        stats = woo.get_sales_stats(days=30)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Automated Dropshipping System
@api_router.post("/dropshipping/process-product/{product_id}")
async def process_dropshipping_product(
    product_id: int,
    supplier_price: float,
    generate_content: bool = False
):
    """Process new dropshipping product"""
    try:
        system = get_dropshipping_system()
        result = await system.process_new_product(
            product_id,
            supplier_price,
            generate_content
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/dropshipping/process-all")
async def process_all_products(generate_content: bool = False):
    """Process all products in store"""
    try:
        system = get_dropshipping_system()
        result = await system.process_all_products(generate_content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/dropshipping/generate-content/{product_id}")
async def generate_product_content(product_id: int):
    """Generate AI images and videos for product"""
    try:
        woo = get_woo_client()
        product = woo.get_product(product_id)
        
        system = get_dropshipping_system()
        result = await system.generate_product_content(
            product_id,
            product.get('name', ''),
            product.get('description', '')
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/dropshipping/social-media/{product_id}")
async def generate_social_media_content(
    product_id: int,
    platforms: List[str] = None
):
    """Generate social media content for product"""
    try:
        system = get_dropshipping_system()
        result = await system.generate_social_media_content(product_id, platforms)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/dropshipping/stats")
async def get_dropshipping_stats():
    """Get dropshipping processing statistics"""
    try:
        system = get_dropshipping_system()
        stats = system.get_processing_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# DOWNLOAD ENDPOINT
# =========================

@api_router.get("/download/sistema-completo")
async def download_sistema_completo():
    """Download complete system package"""
    from fastapi.responses import FileResponse
    import os
    
    file_path = "/tmp/sistema-dropshipping-ia.tar.gz"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename="sistema-dropshipping-ia.tar.gz",
        media_type="application/gzip"
    )

@api_router.get("/download/parte/{parte_id}")
async def download_parte(parte_id: str):
    """Download system in parts (aa, ab, ac, ad, ae, af, ag)"""
    from fastapi.responses import FileResponse
    import os
    
    if parte_id not in ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag']:
        raise HTTPException(status_code=404, detail="Part not found")
    
    file_path = f"/tmp/sistema-parte-{parte_id}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=f"sistema-parte-{parte_id}",
        media_type="application/octet-stream"
    )

@api_router.get("/download/info")
async def download_info():
    """Get download information"""
    import os
    
    partes = []
    for parte in ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag']:
        path = f"/tmp/sistema-parte-{parte}"
        if os.path.exists(path):
            size = os.path.getsize(path)
            partes.append({
                'parte': parte,
                'url': f'/api/download/parte/{parte}',
                'size_mb': round(size / (1024 * 1024), 2)
            })
    
    return {
        'total_partes': len(partes),
        'size_total_mb': 69,
        'partes': partes,
        'instrucciones': {
            'descargar': 'Descarga todas las partes (aa, ab, ac, ad, ae, af, ag)',
            'juntar': 'cat sistema-parte-* > sistema-dropshipping-ia.tar.gz',
            'extraer': 'tar -xzf sistema-dropshipping-ia.tar.gz'
        }
    }


# =========================
# WORDPRESS MANAGEMENT ENDPOINTS
# =========================

from wordpress_integration import create_wordpress_client

@api_router.get("/wordpress/status")
async def wordpress_status():
    """Test WordPress connection and get status"""
    try:
        wp = create_wordpress_client()
        result = wp.test_connection()
        return result
    except Exception as e:
        logger.error(f"WordPress status error: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.get("/wordpress/pages")
async def get_wordpress_pages(per_page: int = 20, status: str = 'publish'):
    """Get all WordPress pages"""
    try:
        wp = create_wordpress_client()
        result = wp.get_pages(per_page, status)
        return result
    except Exception as e:
        logger.error(f"Error getting pages: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.get("/wordpress/posts")
async def get_wordpress_posts(per_page: int = 20, status: str = 'publish'):
    """Get all WordPress blog posts"""
    try:
        wp = create_wordpress_client()
        result = wp.get_posts(per_page, status)
        return result
    except Exception as e:
        logger.error(f"Error getting posts: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/pages/create")
async def create_wordpress_page(page_data: dict):
    """Create a new WordPress page"""
    try:
        wp = create_wordpress_client()
        result = wp.create_page(page_data)
        return result
    except Exception as e:
        logger.error(f"Error creating page: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/pages/create-bulk")
async def create_common_pages(request: dict = None):
    """
    Create common website pages in bulk
    request: {"page_types": ["about", "contact", ...]} or None for all
    Available types: about, contact, shipping, returns, terms, privacy, faq
    """
    try:
        wp = create_wordpress_client()
        all_pages = wp.get_common_pages_template()
        
        page_types = request.get('page_types') if request else None
        
        if page_types:
            # Filter pages based on requested types
            type_map = {
                'about': 'Sobre Nosotros',
                'contact': 'Contacto',
                'shipping': 'Política de Envíos',
                'returns': 'Política de Devoluciones',
                'terms': 'Términos y Condiciones',
                'privacy': 'Política de Privacidad',
                'faq': 'Preguntas Frecuentes'
            }
            titles_to_create = [type_map.get(pt) for pt in page_types if pt in type_map]
            pages_to_create = [p for p in all_pages if p['title'] in titles_to_create]
        else:
            pages_to_create = all_pages
        
        result = wp.create_page_bulk(pages_to_create)
        return result
    except Exception as e:
        logger.error(f"Error creating bulk pages: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.put("/wordpress/pages/{page_id}")
async def update_wordpress_page(page_id: int, page_data: dict):
    """Update an existing WordPress page"""
    try:
        wp = create_wordpress_client()
        result = wp.update_page(page_id, page_data)
        return result
    except Exception as e:
        logger.error(f"Error updating page: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/posts/create")
async def create_wordpress_post(post_data: dict):
    """Create a new WordPress blog post"""
    try:
        wp = create_wordpress_client()
        result = wp.create_blog_post(post_data)
        return result
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.put("/wordpress/posts/{post_id}")
async def update_wordpress_post(post_id: int, post_data: dict):
    """Update an existing WordPress post"""
    try:
        wp = create_wordpress_client()
        result = wp.update_post(post_id, post_data)
        return result
    except Exception as e:
        logger.error(f"Error updating post: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/posts/{post_id}/publish")
async def publish_wordpress_post(post_id: int):
    """Publish a draft post"""
    try:
        wp = create_wordpress_client()
        result = wp.publish_post(post_id)
        return result
    except Exception as e:
        logger.error(f"Error publishing post: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.get("/wordpress/plugins")
async def get_wordpress_plugins():
    """Get list of installed plugins"""
    try:
        wp = create_wordpress_client()
        result = wp.get_plugins()
        return result
    except Exception as e:
        logger.error(f"Error getting plugins: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/plugins/install")
async def install_wordpress_plugin(plugin_data: dict):
    """
    Install a plugin from WordPress.org
    plugin_data: {"slug": "plugin-slug"}
    """
    try:
        plugin_slug = plugin_data.get('slug')
        if not plugin_slug:
            return {"success": False, "error": "Plugin slug is required"}
        
        wp = create_wordpress_client()
        result = wp.install_plugin(plugin_slug)
        return result
    except Exception as e:
        logger.error(f"Error installing plugin: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/plugins/{plugin_path}/activate")
async def activate_wordpress_plugin(plugin_path: str):
    """Activate an installed plugin"""
    try:
        wp = create_wordpress_client()
        result = wp.activate_plugin(plugin_path)
        return result
    except Exception as e:
        logger.error(f"Error activating plugin: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/wordpress/analytics/setup")
async def setup_google_analytics(analytics_data: dict):
    """
    Setup Google Analytics
    analytics_data: {"tracking_id": "G-XXXXXXXXXX", "method": "header" or "plugin"}
    """
    try:
        tracking_id = analytics_data.get('tracking_id')
        method = analytics_data.get('method', 'header')
        
        if not tracking_id:
            return {"success": False, "error": "Google Analytics tracking ID is required"}
        
        wp = create_wordpress_client()
        result = wp.add_google_analytics(tracking_id, method)
        return result
    except Exception as e:
        logger.error(f"Error setting up Google Analytics: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.get("/wordpress/seo/recommendations")
async def get_seo_recommendations():
    """Get SEO plugin recommendations and setup instructions"""
    return {
        "success": True,
        "recommendations": [
            {
                "name": "Yoast SEO",
                "slug": "wordpress-seo",
                "description": "El plugin SEO más popular para WordPress",
                "features": [
                    "Análisis SEO en tiempo real",
                    "Vista previa de snippets de Google",
                    "Gestión de XML sitemaps",
                    "Análisis de legibilidad",
                    "Integración con redes sociales"
                ],
                "rating": 5,
                "downloads": "5M+",
                "recommended": True
            },
            {
                "name": "Rank Math SEO",
                "slug": "seo-by-rank-math",
                "description": "Plugin SEO moderno con IA integrada",
                "features": [
                    "Optimización con IA",
                    "Soporte para múltiples palabras clave",
                    "Análisis SEO avanzado",
                    "Rich Snippets integrados",
                    "Seguimiento de rankings"
                ],
                "rating": 5,
                "downloads": "1M+",
                "recommended": True
            },
            {
                "name": "All in One SEO",
                "slug": "all-in-one-seo-pack",
                "description": "Suite completa de herramientas SEO",
                "features": [
                    "Configuración sencilla",
                    "Optimización automática",
                    "Análisis de TruSEO",
                    "SEO local",
                    "Schema markup"
                ],
                "rating": 4.5,
                "downloads": "3M+",
                "recommended": False
            }
        ],
        "installation_guide": {
            "automatic": [
                "1. Usa el endpoint POST /api/wordpress/plugins/install con el slug del plugin",
                "2. Activa el plugin con POST /api/wordpress/plugins/{slug}/activate",
                "3. Configura las opciones básicas en WordPress admin"
            ],
            "manual": [
                "1. Ve a Plugins > Añadir nuevo en WordPress",
                "2. Busca 'Yoast SEO' o 'Rank Math'",
                "3. Click en 'Instalar ahora'",
                "4. Click en 'Activar'",
                "5. Sigue el asistente de configuración"
            ]
        },
        "setup_tips": [
            "Configura tu título y descripción por defecto",
            "Conecta Google Search Console",
            "Genera y envía tu XML sitemap",
            "Optimiza cada página con la palabra clave objetivo",
            "Verifica que no haya errores en el análisis SEO"
        ]
    }


@api_router.get("/wordpress/plugin/download")
async def download_wordpress_plugin():
    """Download the AI Dropshipping Manager plugin"""
    import os
    plugin_path = "/app/wordpress-plugin/ai-dropshipping-manager.zip"
    
    if not os.path.exists(plugin_path):
        return {"success": False, "error": "Plugin file not found"}
    
    from fastapi.responses import FileResponse
    return FileResponse(
        path=plugin_path,
        filename="ai-dropshipping-manager.zip",
        media_type="application/zip"
    )

@api_router.get("/wordpress/plugin/info")
async def get_plugin_info():
    """Get plugin information"""
    return {
        "success": True,
        "plugin": {
            "name": "AI Dropshipping Manager",
            "version": "1.1.0",
            "api_url": "https://wpmoneyhub.preview.emergentagent.com/api",
            "description": "Gestión automática de productos dropshipping con IA",
            "changelog": [
                "v1.1.0 - API URL actualizada a agente90.preview.emergentagent.com",
                "v1.0.0 - Versión inicial"
            ],
            "download_url": "https://wpmoneyhub.preview.emergentagent.com/api/wordpress/plugin/download",
            "installation": [
                "1. Descarga el plugin desde el enlace de arriba",
                "2. En WordPress, ve a Plugins > Añadir nuevo > Subir plugin",
                "3. Selecciona el archivo .zip descargado",
                "4. Click en 'Instalar ahora'",
                "5. Activa el plugin",
                "6. La API ya está configurada automáticamente"
            ]
        }
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
            " Payments & Checkout (Stripe)",
            " Revenue Analytics",
            " Subscription Management",
            " Campaign ROI Tracking",
            " Affiliate Program",
            " Amazon Associates Integration",
            " Dropshipping Automation",
            " Memberships & Premium Content",
            " Donations & Tips",
            " A/B Testing",
            " AI Product Recommendations",
            " Email Marketing Automation",
            " Cart Abandonment Recovery"
        ]
    }


# =====================================================
# SIMPLE STATUS ENDPOINT - DIAGNOSTICO
# =====================================================

@api_router.get("/status/simple")
async def simple_status():
    """
    Endpoint simple de status sin dependencias de DB
    Para verificar que el servidor está funcionando
    """
    return {
        "status": "live",
        "message": "Backend funcionando correctamente",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Super Cerebro AI Backend",
        "version": "1.0.0",
        "endpoints_available": True,
        "environment": {
            "mongo_configured": bool(os.environ.get('MONGO_URL')),
            "openrouter_configured": bool(os.environ.get('OPENROUTER_API_KEY')),
            "openai_configured": bool(os.environ.get('OPENAI_API_KEY')),
            "stripe_configured": bool(os.environ.get('STRIPE_API_KEY')),
            "wc_configured": bool(os.environ.get('WC_URL'))
        }
    }

@api_router.get("/status/detailed")
async def detailed_status():
    """
    Status detallado con información de todos los servicios
    """
    status = {
        "service": "Super Cerebro AI Backend",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": os.environ.get('ENVIRONMENT', 'development'),
        "services": {}
    }
    
    # Test MongoDB
    try:
        await db.command('ping')
        collections_count = len(await db.list_collection_names())
        status["services"]["mongodb"] = {
            "status": "connected",
            "database": os.environ.get('DB_NAME'),
            "collections": collections_count
        }
    except Exception as e:
        status["services"]["mongodb"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Check AI APIs
    status["services"]["ai_apis"] = {
        "openrouter": "configured" if os.environ.get('OPENROUTER_API_KEY') else "not_configured",
        "openai": "configured" if os.environ.get('OPENAI_API_KEY') else "not_configured",
        "perplexity": "configured" if os.environ.get('PERPLEXITY_API_KEY') else "not_configured",
        "fal_ai": "configured" if os.environ.get('FAL_API_KEY') else "not_configured"
    }
    
    # Check WooCommerce/WordPress
    status["services"]["integrations"] = {
        "woocommerce": "configured" if os.environ.get('WC_URL') else "not_configured",
        "wordpress": "configured" if os.environ.get('WP_URL') else "not_configured",
        "stripe": "configured" if os.environ.get('STRIPE_API_KEY') else "not_configured",
        "telegram": "configured" if os.environ.get('TELEGRAM_BOT_TOKEN') else "not_configured"
    }
    
    return status

# =====================================================
# AI SUPER POWERS - ENDPOINTS FOR WORDPRESS PLUGIN
# =====================================================

# TODO: Uncomment when ai_integrations functions are implemented
# from ai_integrations import (
#     generate_product_description,
#     generate_product_images,
#     analyze_market_competition,
#     get_optimal_pricing,
#     generate_social_media_content,
#     generate_email_campaign,
#     process_product_complete
# )

class AIProductRequest(BaseModel):
    """Request para procesar producto con AI"""
    product_name: str
    category: str
    features: Optional[List[str]] = None
    base_price: Optional[float] = None
    generate_images: bool = True

class AIDescriptionRequest(BaseModel):
    """Request para generar descripción"""
    product_name: str
    category: str
    features: Optional[List[str]] = None
    language: str = "es"
    custom_prompt: Optional[str] = None

class AIImageRequest(BaseModel):
    """Request para generar imágenes"""
    product_name: str
    category: str
    style: str = "professional product photo"
    num_images: int = 1
    custom_prompt: Optional[str] = None

class AIMarketRequest(BaseModel):
    """Request para análisis de mercado"""
    product_name: str
    category: str
    custom_prompt: Optional[str] = None

class AIPricingRequest(BaseModel):
    """Request para cálculo de precio óptimo"""
    product_name: str
    category: str
    base_price: float

class AISocialMediaRequest(BaseModel):
    """Request para contenido de redes sociales"""
    product_name: str
    description: str
    platforms: List[str] = ["instagram", "facebook", "twitter"]
    custom_prompt: Optional[str] = None

class AIEmailRequest(BaseModel):
    """Request para campaña de email"""
    product_name: str
    description: str
    target_audience: str = "general"
    custom_prompt: Optional[str] = None

# TODO: Uncomment these endpoints when ai_integrations functions are fully implemented
# 
# @api_router.post("/ai/product/complete")
# async def ai_process_product_complete(request: AIProductRequest):
#     """
#     Procesa producto completo con todas las integraciones AI
#     - Descripción SEO optimizada
#     - Análisis de mercado
#     - Precio óptimo
#     - Generación de imágenes
#     - Contenido de redes sociales
#     """
#     try:
#         result = await process_product_complete(
#             product_name=request.product_name,
#             category=request.category,
#             features=request.features,
#             base_price=request.base_price,
#             generate_images=request.generate_images
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error processing product: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# 
# @api_router.post("/ai/product/description")
# async def ai_generate_description(request: AIDescriptionRequest):
#     """
#     Genera descripción profesional con SEO
#     Usa OpenRouter (Claude 3.5 Sonnet)
#     """
#     try:
#         result = await generate_product_description(
#             product_name=request.product_name,
#             category=request.category,
#             features=request.features,
#             language=request.language,
#             custom_prompt=request.custom_prompt
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error generating description: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# 
# @api_router.post("/ai/product/images")
# async def ai_generate_images(request: AIImageRequest):
#     """
#     Genera imágenes profesionales del producto
#     Usa Fal AI (Flux) o DALL-E como respaldo
#     """
#     try:
#         result = await generate_product_images(
#             product_name=request.product_name,
#             category=request.category,
#             style=request.style,
#             num_images=request.num_images
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error generating images: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# 
# @api_router.post("/ai/product/market-analysis")
# async def ai_market_analysis(request: AIMarketRequest):
#     """
#     Analiza mercado y competencia en tiempo real
#     Usa Perplexity para búsqueda web actualizada
#     """
#     try:
#         result = await analyze_market_competition(
#             product_name=request.product_name,
#             category=request.category
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error analyzing market: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# # from ai_agent import agent
# @api_router.post("/ai/product/optimal-pricing")
# async def ai_optimal_pricing(request: AIPricingRequest):
#     """
#     Calcula precio óptimo basado en mercado
#     Usa Abacus AI para análisis predictivo
#     """
#     try:
#         result = await get_optimal_pricing(
#             product_name=request.product_name,
#             category=request.category,
#             base_price=request.base_price
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error calculating pricing: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# 
# @api_router.post("/ai/content/social-media")
# async def ai_social_media_content(request: AISocialMediaRequest):
#     """
#     Genera contenido optimizado para redes sociales
#     Posts, hashtags, mejores horarios
#     """
#     try:
#         result = await generate_social_media_content(
#             product_name=request.product_name,
#             description=request.description,
#             platforms=request.platforms
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error generating social media content: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
# 
# @api_router.post("/ai/content/email-campaign")
# async def ai_email_campaign(request: AIEmailRequest):
#     """
#     Genera campaña completa de email marketing
#     Asuntos, contenido HTML, segmentación
#     """
#     try:
#         result = await generate_email_campaign(
#             product_name=request.product_name,
#             description=request.description,
#             target_audience=request.target_audience
#         )
#         return result
#     except Exception as e:
#         logger.error(f"Error generating email campaign: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/ai/health")
async def ai_health_check():
    """Verifica que todas las APIs AI estén configuradas"""
    from ai_integrations import (
        OPENROUTER_KEY, PERPLEXITY_KEY, OPENAI_KEY, FAL_KEY, ABACUS_KEY
    )
    
    return {
        "success": True,
        "apis": {
            "openrouter": bool(OPENROUTER_KEY),
            "perplexity": bool(PERPLEXITY_KEY),
            "openai": bool(OPENAI_KEY),
            "fal_ai": bool(FAL_KEY),
            "abacus_ai": bool(ABACUS_KEY)
        }
    }


# =====================================================
# AI AGENT - CEREBRO CENTRAL DEL SISTEMA
# =====================================================
# TODO: Fix ai_agent.py to export 'agent' object before uncommenting
# from ai_agent import agent

# TODO: Uncomment these agent endpoints when ai_agent.py exports 'agent' properly
# 
# class AgentExecuteRequest(BaseModel):
#     """Request para ejecutar comando del agente"""
#     command: str
#     user_id: str = "default"
# 
# @api_router.post("/agent/upload")
# async def agent_upload_file(
#     file: UploadFile = File(...),
#     user_id: str = Form(...),
#     command: Optional[str] = Form(None)
# ):
#     """Upload y procesa archivos para el agente"""
#     # Implementation commented out - requires 'agent' object
#     pass
# 
# @api_router.post("/agent/execute")
# async def agent_execute_command(request: AgentExecuteRequest):
#     """Endpoint principal del agente inteligente"""
#     # Implementation commented out - requires 'agent' object
#     pass
# 
# @api_router.post("/agent/chat")
# async def agent_chat(request: AgentExecuteRequest):
#     """Chat conversacional con el agente"""
#     # Implementation commented out - requires 'agent' object
#     pass

# =====================================================
# TEMPORARY AGENT ENDPOINTS - WORDPRESS PLUGIN SUPPORT
# =====================================================

class AgentExecuteRequest(BaseModel):
    """Request para ejecutar comando del agente"""
    command: str
    user_id: str = "default"

@api_router.post("/agent/execute")
@api_router.post("/agent/execute")
@api_router.post("/agent/execute")
@api_router.post("/agent/chat")
async def agent_execute_command(request: AgentExecuteRequest):
    """
    Endpoint principal del agente con IA completa
    """
    try:
        logger.info(f"📨 Comando recibido de user {request.user_id}: {request.command[:50]}...")
        
        # Procesar comando con el agente
        resultado = await agente.procesar_comando(
            command=request.command,
            user_id=request.user_id
        )
        
        logger.info(f"📦 Resultado del agente: {resultado}")
        
        # Extraer respuesta con múltiples fallbacks
        ai_response = resultado.get('response', '')
        
        if not ai_response or len(ai_response.strip()) == 0:
            ai_response = resultado.get('mensaje', '')
        
        if not ai_response or len(ai_response.strip()) == 0:
            ai_response = "He procesado tu solicitud pero no generé una respuesta. Por favor, reformula tu pregunta."
        
        logger.info(f"✅ Respuesta extraída: {len(ai_response)} caracteres")
        
        # Extraer acciones
        acciones = resultado.get('acciones', [])
        
        # Si hubo acciones ejecutadas, agregarlas al mensaje
        if acciones and len(acciones) > 0:
            resumen_acciones = "\n\n🛠️ **Acciones ejecutadas:**\n"
            for accion in acciones:
                herramienta = accion.get('herramienta', 'desconocida')
                exito = accion.get('resultado', {}).get('success', False)
                estado = "✅" if exito else "❌"
                resumen_acciones += f"{estado} {herramienta}\n"
            
            ai_response += resumen_acciones
        
        # Construir respuesta final
        respuesta_final = {
            "success": resultado.get('success', True),
            "response": ai_response,
            "mensaje": ai_response,
            "acciones": acciones,
            "plan": {
                "respuesta_usuario": ai_response,
                "acciones_ejecutadas": len(acciones)
            },
            "timestamp": resultado.get('timestamp', datetime.now(timezone.utc).isoformat())
        }
        
        logger.info(f"📤 Enviando respuesta: success={respuesta_final['success']}, len={len(ai_response)}")
        
        return respuesta_final
        
    except Exception as e:
        logger.error(f"❌ Error en agent_execute_command: {str(e)}", exc_info=True)
        error_msg = f"Error inesperado: {str(e)}"
        return {
            "success": False,
            "response": error_msg,
            "mensaje": error_msg,
            "acciones": [],
            "plan": {
                "respuesta_usuario": error_msg,
                "acciones_ejecutadas": 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error en agent/execute: {str(e)}", exc_info=True)
        return {
            "success": False,
            "mensaje": f" Error al procesar tu solicitud:\n\n{str(e)}\n\nPor favor, intenta de nuevo o contacta con soporte.",
            "acciones": []
        }


@api_router.post("/agent/chat")
async def agent_chat(request: AgentExecuteRequest):
    """
    Alias para compatibilidad - usa el mismo endpoint
    """
    return await agent_execute_command(request)
@api_router.get("/agent/status")
async def agent_status():
    """Estado del agente y conversaciones activas - Con manejo robusto de errores"""
    try:
        # Intentar contar conversaciones en MongoDB
        total_conversations = 0
        total_memories = 0
        db_connected = False
        
        try:
            total_conversations = await db["conversations"].count_documents({})
            total_memories = await db["agent_memory"].count_documents({})
            db_connected = True
            logger.info(f"MongoDB connected: conversations={total_conversations}, memories={total_memories}")
        except Exception as db_error:
            logger.warning(f"MongoDB connection issue in /agent/status: {str(db_error)}")
            db_connected = False
        
        # Verificar si OpenAI key está disponible
        openai_key_available = bool(os.environ.get('OPENAI_API_KEY'))
        
        response = {
            "success": True,
            "agente_activo": True,
            "database_connected": db_connected,
            "conversaciones_totales": total_conversations,
            "memorias_guardadas": total_memories,
            "herramientas_disponibles": 22,
            "modelo": "Perplexity Pro (sonar-pro)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "caracteristicas": {
                "memoria_persistente": db_connected,
                "busqueda_semantica": openai_key_available,
                "rag_enabled": openai_key_available,
                "embeddings": openai_key_available,
                "serp_api": bool(os.environ.get('SERP_API_KEY')),
                "apify": bool(os.environ.get('APIFY_TOKEN')),
                "google_cloud": bool(os.environ.get('GOOGLE_CLIENT_ID')),
                "perplexity_pro": bool(os.environ.get('PERPLEXITY_API_KEY'))
            }
        }
        
        logger.info(f"Agent status check completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in /agent/status endpoint: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@api_router.get("/agent/memory/{user_id}")
async def get_agent_memory(user_id: str, limit: int = 20):
    """Obtiene el historial de memoria del agente para un usuario"""
    try:
        memories = await db["agent_memory"].find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        # Formatear memorias (sin embeddings para ahorrar bandwidth)
        formatted_memories = []
        for mem in memories:
            formatted_memories.append({
                "command": mem.get("command"),
                "response": mem.get("response"),
                "plan": mem.get("plan"),
                "timestamp": mem.get("timestamp")
            })
        
        return {
            "success": True,
            "user_id": user_id,
            "total": len(formatted_memories),
            "memories": formatted_memories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/agent/conversations/{user_id}")
async def get_agent_conversations(user_id: str, limit: int = 50):
    """Obtiene el historial completo de conversaciones de un usuario"""
    try:
        conversations = await db["conversations"].find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return {
            "success": True,
            "user_id": user_id,
            "total": len(conversations),
            "conversations": conversations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/agent/search-memory")
async def search_agent_memory(request: dict):
    """Busca en la memoria del agente usando similaridad semántica"""
    # TODO: Re-enable when agent is properly exported from ai_agent.py
    return {
        "success": False,
        "error": "Agent search functionality temporarily disabled",
        "message": "This endpoint requires the agent object which is currently unavailable"
    }
    # try:
    #     memories = await agent.search_relevant_memories(
    #         request.get("user_id"),
    #         request.get("command"),
    #         limit=10
    #     )
    #     
    #     return {
    #         "success": True,
    #         "query": request.get("command"),
    #         "resultados": len(memories),
    #         "memories": memories
    #     }
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/agent/memory/{user_id}")
async def delete_agent_memory(user_id: str):
    """Elimina toda la memoria de un usuario"""
    try:
        # Eliminar conversaciones
        result_conv = await db["conversations"].delete_many({"user_id": user_id})
        
        # Eliminar memorias
        result_mem = await db["agent_memory"].delete_many({"user_id": user_id})
        
        return {
            "success": True,
            "conversaciones_eliminadas": result_conv.deleted_count,
            "memorias_eliminadas": result_mem.deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@api_router.get("/download/wordpress-plugin")
async def download_wordpress_plugin():
    """Descarga el plugin de WordPress en formato ZIP"""
    from fastapi.responses import FileResponse
    import os
    
    file_path = "/app/ai-dropshipping-super-powered-v2.0.zip"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Plugin ZIP not found")
    
    return FileResponse(
        path=file_path,
        filename="ai-dropshipping-manager.zip",
        media_type="application/zip"
    )

@api_router.get("/download/wordpress-plugin-fixed")
async def download_wordpress_plugin_fixed():
    """Descarga el plugin de WordPress CORREGIDO (nombre de carpeta correcto)"""
    from fastapi.responses import FileResponse
    import os
    
    file_path = "/app/ai-dropshipping-manager-fixed.zip"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Plugin ZIP not found")
    
    return FileResponse(
        path=file_path,
        filename="ai-dropshipping-manager.zip",
        media_type="application/zip"
    )



# Include the router in the main app
app.include_router(api_router)

# Include webhook router
from webhooks import webhook_router
app.include_router(webhook_router)
@api_router.get("/debug/env")
async def debug_env():
    """Endpoint temporal para diagnóstico"""
    return {
        "perplexity_key_exists": bool(os.environ.get('PERPLEXITY_API_KEY')),
        "perplexity_key_length": len(os.environ.get('PERPLEXITY_API_KEY', '')) if os.environ.get('PERPLEXITY_API_KEY') else 0,
        "openai_key_exists": bool(os.environ.get('OPENAI_API_KEY')),
        "openrouter_key_exists": bool(os.environ.get('OPENROUTER_API_KEY')),
        "backend_url": os.environ.get('BACKEND_URL', 'Not set'),
        "environment": os.environ.get('ENVIRONMENT', 'Not set'),
        "agente_configured": bool(agente),
        "perplexity_test": "Checking..." if os.environ.get('PERPLEXITY_API_KEY') else "No API key"
    }

@api_router.post("/debug/test-ai")
async def test_ai_direct():
    """Test directo del agente AI"""
    try:
        result = await agente.procesar_comando(
            command="Hola, estas funcionando?",
            user_id="debug_test"
        )
        return {
            "status": "success",
            "result": result,
            "agente_available": True
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "agente_available": False
        }
from pydantic import BaseModel
from fastapi import HTTPException, Request
import aiohttp
import os

# Health check endpoint (for /api/statussimple)
@api_router.get("/statussimple")
async def simples_status():
    return {
        "status": "live",
        "message": "Backend is working correctly"
    }

# Conversational AI endpoint (for /api/ask)
class AskRequest(BaseModel):
    user_id: str
    question: str

class AskResponse(BaseModel):
    answer: str

PERPLEXITY_API_URL = os.environ.get("PERPLEXITY_API_URL", "").rstrip("/")
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")  # Optional

@api_router.post("/ask", response_model=AskResponse)
async def ask_endpoint(input: AskRequest, request: Request):
    url = f"{PERPLEXITY_API_URL}/api/answer"  # Correct endpoint for your Perplexity backend
    payload = {
        "user_id": input.user_id,
        "question": input.question
    }
    headers = {"Accept": "application/json"}
    if PERPLEXITY_API_KEY:
        headers["Authorization"] = f"Bearer {PERPLEXITY_API_KEY}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as resp:
                if resp.status != 200:
                    error_msg = await resp.text()
                    raise HTTPException(status_code=502, detail=f"AI service error: {error_msg}")
                response_data = await resp.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Could not reach the AI backend service. {str(e)}")

    answer = str(response_data.get("answer") or response_data)
    return AskResponse(answer=answer)


# =========================
# SECURITY MIDDLEWARES
# =========================

# 1. Security Headers Middleware (Helmet equivalent)
app.add_middleware(
    SecurityHeadersMiddleware,
    config={
        'development': os.environ.get('ENVIRONMENT') == 'development'
    }
)

# 2. IP Whitelist for Admin Endpoints
if admin_whitelist:
    app.add_middleware(
        IPWhitelistMiddleware,
        whitelist=admin_whitelist,
        admin_paths=[
            "/api/admin",
            "/api/database",
            "/api/audit-logs",
            "/api/api-keys"
        ]
    )
    logger.info(f" Admin IP whitelist enabled with {len(admin_whitelist)} IPs")

# 3. CSRF Protection
app.add_middleware(
    CSRFProtectionMiddleware,
    exempt_paths=[
        "/api/auth/login",
        "/api/auth/register",
        "/api/webhook"
    ]
)

# 4. CORS Middleware (more restrictive in production)
allowed_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
if '*' in allowed_origins and os.environ.get('ENVIRONMENT') == 'production':
    logger.warning("  CORS set to allow all origins in production - consider restricting")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-Token",
        "X-API-Key",
        "X-2FA-Code"
    ],
    expose_headers=[
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
        "Retry-After"
    ],
    max_age=3600
)



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db():
    """Initialize database with migrations on startup"""
    logger.info("="*60)
    logger.info(" SUPER CEREBRO AI - STARTING UP")
    logger.info("="*60)
    
    # Log environment configuration
    logger.info("📋 ENVIRONMENT CONFIGURATION:")
    logger.info(f"   - MongoDB: {' Configured' if os.environ.get('MONGO_URL') else ' Not configured'}")
    logger.info(f"   - Database Name: {os.environ.get('DB_NAME', 'Not set')}")
    logger.info(f"   - OpenRouter API: {' Configured' if os.environ.get('OPENROUTER_API_KEY') else ' Not configured'}")
    logger.info(f"   - OpenAI API: {' Configured' if os.environ.get('OPENAI_API_KEY') else ' Not configured'}")
    logger.info(f"   - Perplexity API: {' Configured' if os.environ.get('PERPLEXITY_API_KEY') else ' Not configured'}")
    logger.info(f"   - Stripe API: {' Configured' if os.environ.get('STRIPE_API_KEY') else ' Not configured'}")
    logger.info(f"   - WooCommerce: {' Configured' if os.environ.get('WC_URL') else ' Not configured'}")
    logger.info(f"   - WordPress: {' Configured' if os.environ.get('WP_URL') else ' Not configured'}")
    logger.info(f"   - Telegram Bot: {' Configured' if os.environ.get('TELEGRAM_BOT_TOKEN') else ' Not configured'}")
    logger.info(f"   - Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    # Test MongoDB connection
    try:
        logger.info(" Testing MongoDB connection...")
        await db.command('ping')
        logger.info(" MongoDB connection successful!")
    except Exception as e:
        logger.error(f" MongoDB connection failed: {str(e)}")
    
    # Run migrations
    try:
        from database.migrations import run_all_migrations
        logger.info(" Running database migrations...")
        await run_all_migrations(mongo_url, os.environ['DB_NAME'])
        logger.info(" Database migrations complete")
    except Exception as e:
        logger.error(f" Database migration error: {e}")
        # Don't fail startup, just log the error
    
    # Log available routes
    logger.info("  AVAILABLE API ROUTES:")
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append(f"   {list(route.methods)[0] if route.methods else 'GET'} {route.path}")
    for route in sorted(routes)[:20]:  # Show first 20 routes
        logger.info(route)
    
    logger.info("="*60)
    logger.info(" SUPER CEREBRO AI - READY TO SERVE")
    logger.info("="*60)
# ENDPOINTS DE DIAGNOSTICO - TEMPORAL
@api_router.get("/debug/env")
async def debug_env():
    """Endpoint temporal para diagnóstico de variables de entorno"""
    return {
        "perplexity_key_exists": bool(os.environ.get('PERPLEXITY_API_KEY')),
        "perplexity_key_length": len(os.environ.get('PERPLEXITY_API_KEY', '')),
        "perplexity_key_start": os.environ.get('PERPLEXITY_API_KEY', '')[:10] if os.environ.get('PERPLEXITY_API_KEY') else "None",
        "openai_key_exists": bool(os.environ.get('OPENAI_API_KEY')),
        "openrouter_key_exists": bool(os.environ.get('OPENROUTER_API_KEY')),
        "all_env_vars_with_api": [k for k in os.environ.keys() if 'API' in k.upper()]
    }

@api_router.post("/debug/test-perplexity")
async def test_perplexity_direct():
    """Test directo de Perplexity API"""
    import httpx
    
    perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
    
    if not perplexity_key:
        return {"error": "No PERPLEXITY_API_KEY found", "key_exists": False}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": "Hola, responde con 'SI FUNCIONO'"}],
                    "max_tokens": 50
                }
            )
            
            return {
                "status_code": response.status_code,
                "response_text": response.text[:500],  # Solo primeros 500 caracteres
                "success": response.status_code == 200,
                "key_length": len(perplexity_key)
            }
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "key_length": len(perplexity_key)
        }
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
@api_router.post("/debug/test-ai-detailed")
async def test_ai_detailed():
    """Test detallado de todas las APIs de IA"""
    results = {}
    
    # Test OpenRouter
    openrouter_key = os.environ.get('OPENROUTER_API_KEY')
    if openrouter_key:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openrouter_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://localhost",
                    },
                    json={
                        "model": "meta-llama/llama-3.1-70b-instruct",
                        "messages": [{"role": "user", "content": "Test"}],
                        "temperature": 0.8,
                        "max_tokens": 50,
                        "top_p": 0.95
                    }
                )
                results['openrouter'] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "error": response.text[:200] if response.status_code != 200 else None
                }
        except Exception as e:
            results['openrouter'] = {"success": False, "error": str(e)}
    else:
        results['openrouter'] = {"success": False, "error": "No API key"}

    # Test Perplexity
    perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
    if perplexity_key:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {perplexity_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-sonar-large-128k-online",
                        "messages": [{"role": "user", "content": "Test"}],
                        "temperature": 0.8,
                        "max_tokens": 50
                    }
                )
                results['perplexity'] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "error": response.text[:200] if response.status_code != 200 else None
                }
        except Exception as e:
            results['perplexity'] = {"success": False, "error": str(e)}
    else:
        results['perplexity'] = {"success": False, "error": "No API key"}

    # Test OpenAI
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4-turbo-preview",
                        "messages": [{"role": "user", "content": "Test"}],
                        "temperature": 0.8,
                        "max_tokens": 50
                    }
                )
                results['openai'] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "error": response.text[:200] if response.status_code != 200 else None
                }
        except Exception as e:
            results['openai'] = {"success": False, "error": str(e)}
    else:
        results['openai'] = {"success": False, "error": "No API key"}

    return results
