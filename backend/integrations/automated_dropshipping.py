"""
Automated Dropshipping System
Connects WooCommerce, FAL AI, and Pricing
"""
import logging
from typing import Dict, List, Optional
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class AutomatedDropshippingSystem:
    """
    Automated system for dropshipping store
    - Fetches products from WooCommerce
    - Calculates optimal prices
    - Generates AI content (images/videos)
    - Updates products automatically
    """
    
    def __init__(self, woo_client, fal_client, price_calculator):
        self.woo = woo_client
        self.fal = fal_client
        self.pricer = price_calculator
    
    async def process_new_product(
        self,
        product_id: int,
        supplier_price: float,
        generate_content: bool = True
    ) -> Dict:
        """
        Process a new product from SharkDropship
        
        Steps:
        1. Get product from WooCommerce
        2. Calculate selling price
        3. Generate AI images (if needed)
        4. Generate AI video demo
        5. Update product with new price and media
        
        Args:
            product_id: WooCommerce product ID
            supplier_price: Price from AliExpress/Temu
            generate_content: Whether to generate AI content
        
        Returns:
            Dict with processing results
        """
        logger.info(f"Processing product {product_id}")
        
        try:
            # 1. Get product details
            product = self.woo.get_product(product_id)
            product_name = product.get('name', '')
            product_desc = product.get('description', '')
            
            # 2. Calculate pricing
            pricing = self.pricer.calculate_selling_price(supplier_price)
            
            logger.info(
                f"Calculated price for '{product_name}': "
                f"€{pricing['supplier_price']} → €{pricing['selling_price_rounded']}"
            )
            
            # 3. Update price in WooCommerce
            self.woo.update_product_price(
                product_id,
                regular_price=pricing['selling_price_rounded']
            )
            
            result = {
                'product_id': product_id,
                'product_name': product_name,
                'pricing': pricing,
                'price_updated': True,
                'content_generated': False
            }
            
            # 4. Generate AI content if requested
            if generate_content:
                content_result = await self.generate_product_content(
                    product_id,
                    product_name,
                    product_desc
                )
                result['content_generated'] = content_result['success']
                result['content_details'] = content_result
            
            logger.info(f"Product {product_id} processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing product {product_id}: {e}")
            return {
                'product_id': product_id,
                'error': str(e),
                'success': False
            }
    
    async def generate_product_content(
        self,
        product_id: int,
        product_name: str,
        product_description: str
    ) -> Dict:
        """
        Generate AI images and videos for product
        
        Args:
            product_id: Product ID
            product_name: Product name
            product_description: Product description
        
        Returns:
            Dict with generated content URLs
        """
        logger.info(f"Generating AI content for: {product_name}")
        
        try:
            # Generate product image
            image_prompt = f"""
            Professional product photography of {product_name}.
            {product_description[:200]}
            White background, studio lighting, high resolution, commercial quality.
            Product centered, sharp focus, elegant presentation.
            """
            
            image_result = await self.fal.text_to_image(
                prompt=image_prompt,
                width=1024,
                height=1024
            )
            
            # Generate product demo video
            video_prompt = f"""
            Professional product demonstration video for {product_name}.
            {product_description[:200]}
            Show the product from multiple angles with smooth camera movements.
            Cinematic lighting, commercial quality, engaging visuals.
            """
            
            video_result = await self.fal.text_to_video(
                prompt=video_prompt,
                duration=5,
                resolution="720p"
            )
            
            return {
                'success': True,
                'image_request_id': image_result.get('request_id'),
                'video_request_id': video_result.get('request_id'),
                'message': 'Content generation started'
            }
            
        except Exception as e:
            logger.error(f"Content generation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def process_all_products(
        self,
        generate_content: bool = False
    ) -> Dict:
        """
        Process all products in store
        
        Args:
            generate_content: Generate AI content for all
        
        Returns:
            Dict with processing summary
        """
        logger.info("Processing all products in store")
        
        try:
            # Get all products
            products = self.woo.get_products(per_page=100)
            
            processed = []
            errors = []
            
            for product in products:
                product_id = product.get('id')
                
                # Check if product has price set
                current_price = float(product.get('regular_price', 0))
                
                if current_price == 0:
                    logger.info(f"Product {product_id} has no price, skipping auto-pricing")
                    continue
                
                try:
                    # Assume current price is supplier price if very low
                    # This is a heuristic - adjust as needed
                    if current_price < 100:
                        result = await self.process_new_product(
                            product_id,
                            supplier_price=current_price,
                            generate_content=generate_content
                        )
                        processed.append(result)
                    
                except Exception as e:
                    errors.append({
                        'product_id': product_id,
                        'error': str(e)
                    })
                
                # Rate limiting
                await asyncio.sleep(2)
            
            return {
                'total_products': len(products),
                'processed': len(processed),
                'errors': len(errors),
                'processed_details': processed,
                'error_details': errors
            }
            
        except Exception as e:
            logger.error(f"Bulk processing error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_social_media_content(
        self,
        product_id: int,
        platforms: List[str] = None
    ) -> Dict:
        """
        Generate social media content for product
        
        Args:
            product_id: Product ID
            platforms: List of platforms (instagram, tiktok, facebook)
        
        Returns:
            Dict with generated content for each platform
        """
        if platforms is None:
            platforms = ['instagram', 'tiktok', 'facebook']
        
        try:
            product = self.woo.get_product(product_id)
            product_name = product.get('name', '')
            
            results = {}
            
            for platform in platforms:
                prompt = f"""
                Eye-catching {platform} promotional video for {product_name}.
                Dynamic, trendy style perfect for {platform}.
                Hook viewers in first 3 seconds.
                Show product benefits quickly.
                """
                
                video_result = await self.fal.text_to_video(
                    prompt=prompt,
                    duration=15 if platform == 'tiktok' else 10,
                    resolution="720p"
                )
                
                results[platform] = video_result
            
            return {
                'success': True,
                'product_id': product_id,
                'platforms': results
            }
            
        except Exception as e:
            logger.error(f"Social media content generation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_processing_stats(self) -> Dict:
        """Get statistics about processed products"""
        try:
            products = self.woo.get_products(per_page=100)
            
            total = len(products)
            with_price = sum(1 for p in products if float(p.get('regular_price', 0)) > 0)
            with_images = sum(1 for p in products if p.get('images'))
            published = sum(1 for p in products if p.get('status') == 'publish')
            
            return {
                'total_products': total,
                'with_price': with_price,
                'with_images': with_images,
                'published': published,
                'needs_processing': total - with_price
            }
            
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {'error': str(e)}


# Initialize system
def create_dropshipping_system(woo_client, fal_client, price_calculator):
    """Create automated dropshipping system instance"""
    return AutomatedDropshippingSystem(woo_client, fal_client, price_calculator)
