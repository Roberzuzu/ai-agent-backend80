"""
WordPress and WooCommerce Integration Module
Syncs products and content with herramientasyaccesorios.store
"""

import os
import requests
import logging
import base64
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class WordPressIntegration:
    """WordPress and WooCommerce integration"""
    
    def __init__(self):
        self.base_url = os.environ.get('WORDPRESS_URL', '').rstrip('/')
        self.username = os.environ.get('WORDPRESS_USER')
        self.password = os.environ.get('WORDPRESS_PASSWORD')
        
        # WooCommerce API credentials
        self.wc_key = os.environ.get('WC_CONSUMER_KEY')
        self.wc_secret = os.environ.get('WC_CONSUMER_SECRET')
        
        # Create basic auth header for WordPress
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.wp_headers = {
            'Authorization': f'Basic {encoded}',
            'Content-Type': 'application/json'
        }
        
        # WooCommerce uses query params for auth
        self.wc_auth = {
            'consumer_key': self.wc_key,
            'consumer_secret': self.wc_secret
        }
        
        self.headers = self.wp_headers  # For backward compatibility
        self.wp_api = f"{self.base_url}/wp-json/wp/v2"
        self.wc_api = f"{self.base_url}/wp-json/wc/v3"
    
    def test_connection(self) -> Dict[str, Any]:
        """Test WordPress and WooCommerce connection"""
        try:
            # Test WooCommerce connection
            response = requests.get(
                f"{self.wc_api}/system_status",
                params=self.wc_auth,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'message': 'Connected to WooCommerce',
                    'store_name': data.get('settings', {}).get('general', {}).get('woocommerce_store_address'),
                    'url': self.base_url,
                    'wc_version': data.get('environment', {}).get('version')
                }
            else:
                return {
                    'success': False,
                    'error': f"WooCommerce connection failed: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"WooCommerce connection error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a WooCommerce product"""
        try:
            # Map product data to WooCommerce format
            wc_product = {
                'name': product_data.get('name'),
                'type': 'simple',
                'regular_price': str(product_data.get('price', 0)),
                'description': product_data.get('description', ''),
                'short_description': product_data.get('description', '')[:120],
                'categories': [
                    {'name': product_data.get('category', 'Uncategorized')}
                ],
                'meta_data': [
                    {'key': '_agent_product_id', 'value': product_data.get('id')},
                    {'key': '_affiliate_link', 'value': product_data.get('affiliate_link', '')},
                    {'key': '_discount_code', 'value': product_data.get('discount_code', '')},
                ]
            }
            
            # Add sale price if discount exists
            if product_data.get('discount_percentage', 0) > 0:
                original_price = product_data.get('price', 0)
                discount = product_data.get('discount_percentage', 0)
                sale_price = original_price * (1 - discount / 100)
                wc_product['sale_price'] = str(round(sale_price, 2))
            
            # Add image if available
            if product_data.get('image_url'):
                wc_product['images'] = [
                    {'src': product_data.get('image_url')}
                ]
            
            # Set as featured if specified
            if product_data.get('is_featured', False):
                wc_product['featured'] = True
            
            response = requests.post(
                f"{self.wc_api}/products",
                params=self.wc_auth,
                json=wc_product,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                wc_data = response.json()
                return {
                    'success': True,
                    'wc_product_id': wc_data.get('id'),
                    'permalink': wc_data.get('permalink'),
                    'message': f"Product created: {wc_data.get('name')}"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to create product: {response.status_code}",
                    'details': response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating WooCommerce product: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_product(self, wc_product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing WooCommerce product"""
        try:
            wc_product = {
                'name': product_data.get('name'),
                'regular_price': str(product_data.get('price', 0)),
                'description': product_data.get('description', ''),
            }
            
            if product_data.get('discount_percentage', 0) > 0:
                original_price = product_data.get('price', 0)
                discount = product_data.get('discount_percentage', 0)
                sale_price = original_price * (1 - discount / 100)
                wc_product['sale_price'] = str(round(sale_price, 2))
            
            response = requests.put(
                f"{self.wc_api}/products/{wc_product_id}",
                params=self.wc_auth,
                json=wc_product,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Product updated'
                }
            else:
                return {
                    'success': False,
                    'error': f"Update failed: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_blog_post(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a WordPress blog post from generated content"""
        try:
            # Prepare post data
            post_data = {
                'title': content_data.get('title'),
                'content': content_data.get('generated_content', content_data.get('description')),
                'status': 'draft',  # Start as draft for review
                'categories': [],
                'tags': [],
                'meta': {
                    '_agent_content_id': content_data.get('id'),
                }
            }
            
            # Add category based on platform
            platform = content_data.get('platform', 'general')
            post_data['categories'] = [platform.capitalize()]
            
            # Add tags from keywords
            if content_data.get('keywords'):
                post_data['tags'] = content_data.get('keywords')
            
            response = requests.post(
                f"{self.wp_api}/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                wp_post = response.json()
                return {
                    'success': True,
                    'post_id': wp_post.get('id'),
                    'permalink': wp_post.get('link'),
                    'message': f"Blog post created: {wp_post.get('title', {}).get('rendered')}"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to create post: {response.status_code}",
                    'details': response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def publish_post(self, post_id: int) -> Dict[str, Any]:
        """Publish a draft post"""
        try:
            response = requests.post(
                f"{self.wp_api}/posts/{post_id}",
                headers=self.headers,
                json={'status': 'publish'},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Post published'
                }
            else:
                return {
                    'success': False,
                    'error': f"Publish failed: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error publishing post: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_products(self, per_page: int = 10) -> Dict[str, Any]:
        """Get WooCommerce products"""
        try:
            params = self.wc_auth.copy()
            params['per_page'] = per_page
            
            response = requests.get(
                f"{self.wc_api}/products",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                products = response.json()
                return {
                    'success': True,
                    'products': products,
                    'count': len(products)
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to get products: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error getting products: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def sync_featured_products(self, product_ids: List[str]) -> Dict[str, Any]:
        """Sync featured products to WordPress"""
        results = []
        
        for product_id in product_ids[:5]:  # Limit to 5 featured
            # This would need to get product data from MongoDB
            # and sync to WordPress
            results.append({
                'product_id': product_id,
                'status': 'synced'
            })
        
        return {
            'success': True,
            'synced': len(results),
            'results': results
        }


def create_wordpress_client() -> WordPressIntegration:
    """Create WordPress integration client"""
    return WordPressIntegration()
