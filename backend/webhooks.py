"""
Webhook Handler for WooCommerce
Receives notifications when products are created/updated
"""
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging
import hashlib
import hmac
import os

logger = logging.getLogger(__name__)

webhook_router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


def verify_woocommerce_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify WooCommerce webhook signature"""
    try:
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Signature verification error: {str(e)}")
        return False


async def process_product_webhook(product_data: Dict[str, Any]):
    """Process product in background"""
    try:
        from integrations.automated_dropshipping import AutomatedDropshipping
        
        automation = AutomatedDropshipping()
        product_id = product_data.get('id')
        
        logger.info(f"Processing product webhook for ID: {product_id}")
        
        # Check if product needs processing
        price = product_data.get('price', '0')
        regular_price = product_data.get('regular_price', '0')
        
        needs_processing = (
            not price or price == '0' or price == '' or
            not regular_price or regular_price == '0' or regular_price == ''
        )
        
        if needs_processing:
            logger.info(f"Product {product_id} needs processing - no price set")
            
            # Process product automatically
            result = automation.process_single_product(
                product_id=product_id,
                generate_content=False  # Optional: set to True for AI content
            )
            
            logger.info(f"Product {product_id} processed: {result}")
        else:
            logger.info(f"Product {product_id} already has price: €{price}")
            
    except Exception as e:
        logger.error(f"Error processing product webhook: {str(e)}")


@webhook_router.post("/woocommerce/product-created")
async def woocommerce_product_created(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for WooCommerce product.created event
    
    Configure in WooCommerce:
    - Topic: product.created
    - Delivery URL: https://your-domain.com/api/webhooks/woocommerce/product-created
    - Secret: (copy from .env WC_WEBHOOK_SECRET)
    """
    try:
        # Get payload
        payload = await request.body()
        payload_str = payload.decode('utf-8')
        
        # Get signature header
        signature = request.headers.get('X-WC-Webhook-Signature', '')
        
        # Verify signature (optional but recommended)
        webhook_secret = os.getenv('WC_WEBHOOK_SECRET', '')
        if webhook_secret and signature:
            if not verify_woocommerce_signature(payload, signature, webhook_secret):
                logger.warning("Invalid webhook signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse JSON
        import json
        product_data = json.loads(payload_str)
        
        logger.info(f"Received product.created webhook for product ID: {product_data.get('id')}")
        
        # Process in background
        background_tasks.add_task(process_product_webhook, product_data)
        
        return {
            "status": "success",
            "message": "Webhook received and queued for processing",
            "product_id": product_data.get('id')
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@webhook_router.post("/woocommerce/product-updated")
async def woocommerce_product_updated(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for WooCommerce product.updated event
    
    Configure in WooCommerce:
    - Topic: product.updated
    - Delivery URL: https://your-domain.com/api/webhooks/woocommerce/product-updated
    """
    try:
        payload = await request.body()
        payload_str = payload.decode('utf-8')
        
        import json
        product_data = json.loads(payload_str)
        
        logger.info(f"Received product.updated webhook for product ID: {product_data.get('id')}")
        
        # Process in background (only if needs processing)
        background_tasks.add_task(process_product_webhook, product_data)
        
        return {
            "status": "success",
            "message": "Webhook received",
            "product_id": product_data.get('id')
        }
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@webhook_router.get("/test")
async def test_webhook():
    """Test endpoint to verify webhook is accessible"""
    return {
        "status": "ok",
        "message": "Webhook endpoint is accessible",
        "endpoints": {
            "product_created": "/api/webhooks/woocommerce/product-created",
            "product_updated": "/api/webhooks/woocommerce/product-updated"
        }
    }
