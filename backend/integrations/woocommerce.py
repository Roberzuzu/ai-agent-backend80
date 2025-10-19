"""
WooCommerce Integration
Manage products, orders, and inventory
"""
import os
import requests
from requests.auth import HTTPBasicAuth
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class WooCommerceClient:
    """WooCommerce REST API Client"""
    
    def __init__(
        self,
        store_url: str = None,
        consumer_key: str = None,
        consumer_secret: str = None
    ):
        self.store_url = (store_url or os.environ.get('WORDPRESS_URL', '')).rstrip('/')
        self.consumer_key = consumer_key or os.environ.get('WC_CONSUMER_KEY')
        self.consumer_secret = consumer_secret or os.environ.get('WC_CONSUMER_SECRET')
        
        if not all([self.store_url, self.consumer_key, self.consumer_secret]):
            logger.warning("WooCommerce credentials not fully configured")
        
        self.api_url = f"{self.store_url}/wp-json/wc/v3"
        self.auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        params: Dict = None
    ) -> Dict:
        """Make API request"""
        url = f"{self.api_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"WooCommerce API error: {e}")
            raise
    
    # PRODUCTS
    
    def get_products(
        self,
        per_page: int = 100,
        page: int = 1,
        search: str = None,
        status: str = None
    ) -> List[Dict]:
        """Get products from store"""
        params = {
            'per_page': per_page,
            'page': page
        }
        
        if search:
            params['search'] = search
        
        if status:
            params['status'] = status
        
        return self._request('GET', 'products', params=params)
    
    def get_product(self, product_id: int) -> Dict:
        """Get single product"""
        return self._request('GET', f'products/{product_id}')
    
    def create_product(self, product_data: Dict) -> Dict:
        """Create new product"""
        return self._request('POST', 'products', data=product_data)
    
    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update product"""
        return self._request('PUT', f'products/{product_id}', data=product_data)
    
    def delete_product(self, product_id: int, force: bool = False) -> Dict:
        """Delete product"""
        params = {'force': 'true' if force else 'false'}
        return self._request('DELETE', f'products/{product_id}', params=params)
    
    def update_product_price(
        self,
        product_id: int,
        regular_price: float,
        sale_price: float = None
    ) -> Dict:
        """Update product price"""
        data = {'regular_price': str(regular_price)}
        
        if sale_price:
            data['sale_price'] = str(sale_price)
        
        return self.update_product(product_id, data)
    
    def update_product_images(
        self,
        product_id: int,
        image_urls: List[str]
    ) -> Dict:
        """Update product images"""
        images = [{'src': url} for url in image_urls]
        return self.update_product(product_id, {'images': images})
    
    def set_product_stock(
        self,
        product_id: int,
        stock_status: str = "instock",
        manage_stock: bool = False,
        stock_quantity: int = None
    ) -> Dict:
        """Update product stock"""
        data = {
            'stock_status': stock_status,
            'manage_stock': manage_stock
        }
        
        if stock_quantity is not None:
            data['stock_quantity'] = stock_quantity
        
        return self.update_product(product_id, data)
    
    # ORDERS
    
    def get_orders(
        self,
        per_page: int = 100,
        page: int = 1,
        status: str = None
    ) -> List[Dict]:
        """Get orders"""
        params = {
            'per_page': per_page,
            'page': page
        }
        
        if status:
            params['status'] = status
        
        return self._request('GET', 'orders', params=params)
    
    def get_order(self, order_id: int) -> Dict:
        """Get single order"""
        return self._request('GET', f'orders/{order_id}')
    
    def update_order_status(
        self,
        order_id: int,
        status: str
    ) -> Dict:
        """Update order status"""
        return self._request('PUT', f'orders/{order_id}', data={'status': status})
    
    # CATEGORIES
    
    def get_categories(self) -> List[Dict]:
        """Get product categories"""
        return self._request('GET', 'products/categories', params={'per_page': 100})
    
    def create_category(self, name: str, parent_id: int = 0) -> Dict:
        """Create category"""
        data = {'name': name}
        if parent_id:
            data['parent'] = parent_id
        return self._request('POST', 'products/categories', data=data)
    
    # ANALYTICS
    
    def get_sales_stats(self, days: int = 30) -> Dict:
        """Get sales statistics"""
        from datetime import timedelta
        
        orders = self.get_orders(per_page=100, status='completed')
        
        # Simple stats
        total_sales = sum(float(order.get('total', 0)) for order in orders)
        num_orders = len(orders)
        avg_order = total_sales / num_orders if num_orders > 0 else 0
        
        return {
            'period_days': days,
            'total_sales': round(total_sales, 2),
            'num_orders': num_orders,
            'avg_order_value': round(avg_order, 2),
            'currency': orders[0].get('currency', 'EUR') if orders else 'EUR'
        }


# Helper class for product content generation
class ProductContentGenerator:
    """Generate product descriptions and metadata"""
    
    @staticmethod
    def generate_seo_title(product_name: str, category: str = None) -> str:
        """Generate SEO-friendly title"""
        if category:
            return f"{product_name} - {category} | Herramientas y Accesorios"
        return f"{product_name} | Herramientas y Accesorios"
    
    @staticmethod
    def generate_meta_description(product_name: str, key_features: List[str]) -> str:
        """Generate meta description"""
        features_text = ", ".join(key_features[:3])
        return f"Compra {product_name} con {features_text}. Envío rápido y garantía. ✓ Mejor precio ✓ Alta calidad"
    
    @staticmethod
    def enhance_description(basic_description: str, features: List[str]) -> str:
        """Enhance product description"""
        enhanced = f"{basic_description}\n\n"
        enhanced += "<h3>Características principales:</h3>\n<ul>\n"
        
        for feature in features:
            enhanced += f"<li>{feature}</li>\n"
        
        enhanced += "</ul>\n\n"
        enhanced += "<p><strong>✓ Envío rápido</strong><br>"
        enhanced += "✓ Garantía de satisfacción<br>"
        enhanced += "✓ Atención al cliente 24/7</p>"
        
        return enhanced


# Global instance
woo_client = None


def get_woo_client() -> WooCommerceClient:
    """Get global WooCommerce client"""
    global woo_client
    if woo_client is None:
        woo_client = WooCommerceClient()
    return woo_client
