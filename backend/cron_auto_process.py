#!/usr/bin/env python3
"""
Cron Job: Auto-process WooCommerce products without price
Runs every hour/day to catch any products that weren't processed via webhook
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/woocommerce_cron.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from integrations.woocommerce import WooCommerceClient
from integrations.dropshipping_pricing import calculate_price


def extract_name_from_slug(slug: str) -> str:
    """Extract readable name from slug"""
    if not slug:
        return "Producto sin nombre"
    return slug.replace('-', ' ').title()[:100]


def estimate_supplier_price(slug: str, description: str) -> float:
    """Estimate supplier price from product info"""
    text = f"{slug} {description}".lower()
    
    price_keywords = {
        'profesional': 80.0,
        'combo': 90.0,
        'kit': 60.0,
        'set': 50.0,
        'sierra': 75.0,
        'taladro': 65.0,
        'bateria': 55.0,
        'amoladora': 50.0,
        'multiherramienta': 45.0,
        'electrica': 45.0,
        'atornillador': 40.0,
        'herramienta': 35.0,
        'mini': 30.0,
    }
    
    for keyword, price in price_keywords.items():
        if keyword in text:
            return price
    
    return 40.0  # Default price


def run_cron_job():
    """Main cron job function"""
    logger.info("="*60)
    logger.info("Starting WooCommerce Auto-Processing Cron Job")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("="*60)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Initialize WooCommerce client
        wc = WooCommerceClient()
        
        # Get all products
        logger.info("Fetching products from WooCommerce...")
        products = wc.get_products()
        
        # Filter products without price
        no_price_products = [
            p for p in products 
            if not p.get('price') or p.get('price') == '0' or p.get('price') == ''
        ]
        
        logger.info(f"Total products: {len(products)}")
        logger.info(f"Products without price: {len(no_price_products)}")
        
        if not no_price_products:
            logger.info("✅ All products have prices - nothing to process")
            return
        
        # Process each product
        processed = 0
        errors = []
        
        for product in no_price_products:
            product_id = product['id']
            slug = product.get('slug', '')
            name = product.get('name', '')
            
            try:
                logger.info(f"Processing product ID {product_id}: {slug}")
                
                # Generate name if missing
                if not name or name.strip() == '':
                    name = extract_name_from_slug(slug)
                    logger.info(f"  Generated name: {name}")
                
                # Estimate supplier price
                short_desc = product.get('short_description', '')
                supplier_price = estimate_supplier_price(slug, short_desc)
                
                # Calculate selling price
                pricing = calculate_price(supplier_price, 'EUR')
                selling_price = pricing['selling_price_rounded']
                profit = pricing['profit']
                margin = pricing['margin_percentage'] * 100
                
                logger.info(f"  Supplier: €{supplier_price:.2f} → Selling: €{selling_price:.2f} ({margin:.0f}% margin, €{profit:.2f} profit)")
                
                # Update product
                update_data = {
                    'regular_price': str(selling_price),
                    'price': str(selling_price)
                }
                
                if not product.get('name') or product.get('name').strip() == '':
                    update_data['name'] = name
                
                result = wc.update_product(product_id, update_data)
                
                if result:
                    logger.info(f"  ✅ Product {product_id} updated successfully")
                    processed += 1
                else:
                    logger.error(f"  ❌ Failed to update product {product_id}")
                    errors.append(product_id)
                    
            except Exception as e:
                logger.error(f"  ❌ Error processing product {product_id}: {str(e)}")
                errors.append(product_id)
        
        # Summary
        logger.info("="*60)
        logger.info("Cron Job Summary")
        logger.info("="*60)
        logger.info(f"Products processed: {processed}/{len(no_price_products)}")
        logger.info(f"Errors: {len(errors)}")
        
        if errors:
            logger.warning(f"Failed product IDs: {errors}")
        
        logger.info("✅ Cron job completed successfully")
        
        return {
            'success': True,
            'processed': processed,
            'total': len(no_price_products),
            'errors': len(errors)
        }
        
    except Exception as e:
        logger.error(f"❌ Cron job failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    run_cron_job()
