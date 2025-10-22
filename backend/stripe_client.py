"""
Standalone Stripe Client - Replace emergentintegrations.payments.stripe
Uses native Stripe SDK
"""

import os
import stripe
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")


class CheckoutSessionRequest(BaseModel):
    """Request model for checkout session"""
    price_amount: float
    currency: str = "usd"
    product_name: str
    product_description: Optional[str] = None
    success_url: str
    cancel_url: str
    metadata: Optional[Dict[str, Any]] = None
    mode: str = "payment"  # payment or subscription
    recurring_interval: Optional[str] = None  # month, year


class CheckoutSessionResponse(BaseModel):
    """Response model for checkout session"""
    session_id: str
    url: str
    success: bool = True


class CheckoutStatusResponse(BaseModel):
    """Response model for checkout status"""
    session_id: str
    payment_status: str
    customer_email: Optional[str] = None
    amount_total: Optional[float] = None
    success: bool = True


class StripeCheckout:
    """Standalone Stripe checkout client"""
    
    def __init__(self, api_key: str):
        stripe.api_key = api_key
    
    async def create_checkout_session(self, request: CheckoutSessionRequest) -> CheckoutSessionResponse:
        """Create Stripe checkout session"""
        try:
            # Prepare line items
            line_items = [{
                'price_data': {
                    'currency': request.currency,
                    'product_data': {
                        'name': request.product_name,
                        'description': request.product_description or request.product_name,
                    },
                    'unit_amount': int(request.price_amount * 100),  # Convert to cents
                },
                'quantity': 1,
            }]
            
            # Add recurring data if subscription
            if request.mode == "subscription" and request.recurring_interval:
                line_items[0]['price_data']['recurring'] = {
                    'interval': request.recurring_interval
                }
            
            # Create session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode=request.mode,
                success_url=request.success_url,
                cancel_url=request.cancel_url,
                metadata=request.metadata or {}
            )
            
            return CheckoutSessionResponse(
                session_id=session.id,
                url=session.url
            )
        
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    async def get_checkout_session_status(self, session_id: str) -> CheckoutStatusResponse:
        """Get checkout session status"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            return CheckoutStatusResponse(
                session_id=session.id,
                payment_status=session.payment_status,
                customer_email=session.customer_details.email if session.customer_details else None,
                amount_total=session.amount_total / 100 if session.amount_total else None
            )
        
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
