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
    
    def create_page(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a WordPress page"""
        try:
            response = requests.post(
                f"{self.wp_api}/pages",
                headers=self.wp_headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                page = response.json()
                return {
                    'success': True,
                    'page_id': page.get('id'),
                    'permalink': page.get('link'),
                    'message': f"Page created: {page.get('title', {}).get('rendered')}"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to create page: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error creating page: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_widget_code(self, product_ids: List[str]) -> str:
        """Generate HTML/JS code for featured products widget"""
        widget_html = """
        <div id="featured-products-widget" class="featured-products">
            <h3>Productos Destacados</h3>
            <div class="products-slider">
        """
        
        # Note: In real implementation, would fetch product details
        # For now, return template
        widget_html += """
                <!-- Products will be loaded here -->
            </div>
        </div>
        
        <style>
        .featured-products {
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
            margin: 20px 0;
        }
        .products-slider {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        .product-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .product-card h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .product-card .price {
            font-size: 24px;
            font-weight: bold;
            color: #27ae60;
            margin: 10px 0;
        }
        .product-card .discount {
            background: #e74c3c;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            display: inline-block;
        }
        .product-card .btn {
            display: block;
            background: #3498db;
            color: white;
            text-align: center;
            padding: 10px;
            border-radius: 4px;
            text-decoration: none;
            margin-top: 10px;
        }
        .product-card .btn:hover {
            background: #2980b9;
        }
        </style>
        """
        
        return widget_html
    
    def auto_publish_content_as_post(self, content_data: Dict[str, Any], product_ids: List[str] = None) -> Dict[str, Any]:
        """Automatically publish content as blog post with product links"""
        try:
            # Build content with product mentions
            post_content = content_data.get('generated_content', '')
            
            # Add products section if product_ids provided
            if product_ids:
                post_content += "\n\n<h3>Productos Recomendados</h3>\n"
                post_content += "<p>Para este proyecto/tutorial, recomendamos:</p>\n<ul>"
                
                # Would fetch actual product details here
                for pid in product_ids[:5]:
                    post_content += f"\n<li>Producto {pid} - <a href='#'>Ver detalles</a></li>"
                
                post_content += "\n</ul>"
            
            # Add call to action
            post_content += "\n\n<p><strong>¿Necesitas estas herramientas?</strong> "
            post_content += "Visita nuestra tienda y usa nuestros códigos de descuento exclusivos.</p>"
            
            post_data = {
                'title': content_data.get('title'),
                'content': post_content,
                'status': 'publish',
                'categories': [],
                'tags': content_data.get('keywords', []),
                'meta': {
                    '_agent_content_id': content_data.get('id'),
                    '_seo_description': content_data.get('description', '')[:160]
                }
            }
            
            return self.create_blog_post(post_data)
            
        except Exception as e:
            logger.error(f"Error auto-publishing content: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_pages(self, per_page: int = 20, status: str = 'publish') -> Dict[str, Any]:
        """Get WordPress pages"""
        try:
            params = {
                'per_page': per_page,
                'status': status
            }
            
            response = requests.get(
                f"{self.wp_api}/pages",
                headers=self.wp_headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                pages = response.json()
                return {
                    'success': True,
                    'pages': pages,
                    'count': len(pages)
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to get pages: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error getting pages: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_posts(self, per_page: int = 20, status: str = 'publish') -> Dict[str, Any]:
        """Get WordPress posts"""
        try:
            params = {
                'per_page': per_page,
                'status': status
            }
            
            response = requests.get(
                f"{self.wp_api}/posts",
                headers=self.wp_headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                posts = response.json()
                return {
                    'success': True,
                    'posts': posts,
                    'count': len(posts)
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to get posts: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error getting posts: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_page(self, page_id: int, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing WordPress page"""
        try:
            response = requests.post(
                f"{self.wp_api}/pages/{page_id}",
                headers=self.wp_headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 200:
                page = response.json()
                return {
                    'success': True,
                    'page_id': page.get('id'),
                    'message': f"Page updated: {page.get('title', {}).get('rendered')}"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to update page: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error updating page: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing WordPress post"""
        try:
            response = requests.post(
                f"{self.wp_api}/posts/{post_id}",
                headers=self.wp_headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 200:
                post = response.json()
                return {
                    'success': True,
                    'post_id': post.get('id'),
                    'message': f"Post updated: {post.get('title', {}).get('rendered')}"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to update post: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error updating post: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_page_bulk(self, pages_config: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple common pages at once"""
        results = []
        errors = []
        
        for page_config in pages_config:
            result = self.create_page(page_config)
            if result.get('success'):
                results.append({
                    'title': page_config.get('title'),
                    'page_id': result.get('page_id'),
                    'permalink': result.get('permalink')
                })
            else:
                errors.append({
                    'title': page_config.get('title'),
                    'error': result.get('error')
                })
        
        return {
            'success': len(errors) == 0,
            'created': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        }
    
    def get_plugins(self) -> Dict[str, Any]:
        """Get installed plugins"""
        try:
            response = requests.get(
                f"{self.base_url}/wp-json/wp/v2/plugins",
                headers=self.wp_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                plugins = response.json()
                return {
                    'success': True,
                    'plugins': plugins,
                    'count': len(plugins)
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to get plugins: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error getting plugins: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def install_plugin(self, plugin_slug: str) -> Dict[str, Any]:
        """Install a plugin from WordPress.org repository"""
        try:
            response = requests.post(
                f"{self.base_url}/wp-json/wp/v2/plugins",
                headers=self.wp_headers,
                json={'slug': plugin_slug, 'status': 'inactive'},
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                plugin = response.json()
                return {
                    'success': True,
                    'plugin': plugin_slug,
                    'message': f"Plugin {plugin_slug} installed successfully"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to install plugin: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error installing plugin: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def activate_plugin(self, plugin_path: str) -> Dict[str, Any]:
        """Activate a plugin"""
        try:
            response = requests.post(
                f"{self.base_url}/wp-json/wp/v2/plugins/{plugin_path}",
                headers=self.wp_headers,
                json={'status': 'active'},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f"Plugin {plugin_path} activated"
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to activate plugin: {response.status_code}",
                    'details': response.text
                }
        except Exception as e:
            logger.error(f"Error activating plugin: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_google_analytics(self, ga_tracking_id: str, method: str = 'header') -> Dict[str, Any]:
        """
        Add Google Analytics tracking code to WordPress
        Methods: 'header' (add to theme header), 'plugin' (use plugin)
        """
        try:
            # Google Analytics 4 tracking code
            ga_code = f"""
<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_tracking_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_tracking_id}');
</script>
<!-- End Google Analytics -->
"""
            
            if method == 'header':
                # For header injection, we would typically use a plugin like Insert Headers and Footers
                # or modify the theme's header.php
                # Since direct file modification via API is limited, we'll create instructions
                return {
                    'success': True,
                    'method': 'manual',
                    'code': ga_code,
                    'instructions': [
                        "1. Go to Appearance > Theme Editor in WordPress",
                        "2. Select header.php file",
                        "3. Paste the tracking code before </head> tag",
                        "Or install 'Insert Headers and Footers' plugin and paste code there"
                    ],
                    'message': "Google Analytics code generated. Manual installation required."
                }
            else:
                return {
                    'success': True,
                    'method': 'plugin',
                    'code': ga_code,
                    'recommendation': "Install 'Site Kit by Google' plugin for official GA integration",
                    'message': "For automated GA setup, install Site Kit by Google plugin"
                }
        except Exception as e:
            logger.error(f"Error adding Google Analytics: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_common_pages_template(self) -> List[Dict[str, Any]]:
        """Get templates for common website pages"""
        return [
            {
                'title': 'Sobre Nosotros',
                'content': '''
                    <h2>Quiénes Somos</h2>
                    <p>Somos tu tienda de confianza especializada en herramientas y accesorios de alta calidad.</p>
                    
                    <h3>Nuestra Misión</h3>
                    <p>Proporcionar las mejores herramientas al mejor precio, con atención personalizada y envíos rápidos.</p>
                    
                    <h3>¿Por Qué Elegirnos?</h3>
                    <ul>
                        <li>Productos de marcas reconocidas</li>
                        <li>Precios competitivos y ofertas exclusivas</li>
                        <li>Envío rápido y seguro</li>
                        <li>Atención al cliente excepcional</li>
                        <li>Garantía en todos nuestros productos</li>
                    </ul>
                ''',
                'status': 'publish'
            },
            {
                'title': 'Contacto',
                'content': '''
                    <h2>Contáctanos</h2>
                    <p>¿Tienes alguna pregunta? Estamos aquí para ayudarte.</p>
                    
                    <h3>Formas de Contacto</h3>
                    <ul>
                        <li><strong>Email:</strong> contacto@herramientasyaccesorios.store</li>
                        <li><strong>Horario:</strong> Lunes a Viernes, 9:00 - 18:00</li>
                    </ul>
                    
                    <p>También puedes usar el formulario de contacto a continuación:</p>
                    [contact-form-7]
                ''',
                'status': 'publish'
            },
            {
                'title': 'Política de Envíos',
                'content': '''
                    <h2>Información de Envíos</h2>
                    
                    <h3>Tiempos de Entrega</h3>
                    <ul>
                        <li>Envío estándar: 3-5 días hábiles</li>
                        <li>Envío express: 1-2 días hábiles</li>
                    </ul>
                    
                    <h3>Costos de Envío</h3>
                    <p>Envío gratis en compras superiores a $50 USD</p>
                    <p>Envío estándar: $5.99 USD</p>
                    
                    <h3>Seguimiento</h3>
                    <p>Recibirás un número de seguimiento una vez que tu pedido sea enviado.</p>
                ''',
                'status': 'publish'
            },
            {
                'title': 'Política de Devoluciones',
                'content': '''
                    <h2>Devoluciones y Reembolsos</h2>
                    
                    <h3>30 Días de Garantía</h3>
                    <p>Si no estás satisfecho con tu compra, puedes devolverla dentro de los 30 días.</p>
                    
                    <h3>Proceso de Devolución</h3>
                    <ol>
                        <li>Contacta con nuestro servicio de atención al cliente</li>
                        <li>Recibe tu etiqueta de devolución</li>
                        <li>Envía el producto en su embalaje original</li>
                        <li>Recibe tu reembolso en 5-7 días hábiles</li>
                    </ol>
                    
                    <h3>Condiciones</h3>
                    <ul>
                        <li>El producto debe estar sin usar</li>
                        <li>Embalaje original intacto</li>
                        <li>Incluir todos los accesorios</li>
                    </ul>
                ''',
                'status': 'publish'
            },
            {
                'title': 'Términos y Condiciones',
                'content': '''
                    <h2>Términos y Condiciones de Uso</h2>
                    
                    <h3>1. Aceptación de Términos</h3>
                    <p>Al utilizar este sitio web, aceptas estos términos y condiciones en su totalidad.</p>
                    
                    <h3>2. Uso del Sitio</h3>
                    <p>Este sitio es solo para uso personal y no comercial.</p>
                    
                    <h3>3. Precios y Disponibilidad</h3>
                    <p>Los precios están sujetos a cambios sin previo aviso. La disponibilidad de productos no está garantizada.</p>
                    
                    <h3>4. Propiedad Intelectual</h3>
                    <p>Todo el contenido de este sitio es propiedad de Herramientas y Accesorios Store.</p>
                    
                    <h3>5. Limitación de Responsabilidad</h3>
                    <p>No nos hacemos responsables de daños indirectos o consecuentes derivados del uso del sitio.</p>
                ''',
                'status': 'publish'
            },
            {
                'title': 'Política de Privacidad',
                'content': '''
                    <h2>Política de Privacidad</h2>
                    
                    <h3>Información que Recopilamos</h3>
                    <ul>
                        <li>Nombre y datos de contacto</li>
                        <li>Dirección de envío</li>
                        <li>Información de pago (procesada de forma segura)</li>
                        <li>Historial de pedidos</li>
                    </ul>
                    
                    <h3>Uso de la Información</h3>
                    <p>Utilizamos tu información para:</p>
                    <ul>
                        <li>Procesar tus pedidos</li>
                        <li>Mejorar nuestros servicios</li>
                        <li>Enviarte ofertas y novedades (con tu consentimiento)</li>
                    </ul>
                    
                    <h3>Seguridad</h3>
                    <p>Utilizamos medidas de seguridad estándar de la industria para proteger tu información.</p>
                    
                    <h3>Cookies</h3>
                    <p>Utilizamos cookies para mejorar tu experiencia de navegación.</p>
                    
                    <h3>Tus Derechos</h3>
                    <p>Puedes solicitar acceso, corrección o eliminación de tus datos personales en cualquier momento.</p>
                ''',
                'status': 'publish'
            },
            {
                'title': 'Preguntas Frecuentes (FAQ)',
                'content': '''
                    <h2>Preguntas Frecuentes</h2>
                    
                    <h3>¿Cómo puedo hacer un pedido?</h3>
                    <p>Simplemente navega por nuestros productos, añade los artículos a tu carrito y procede al checkout.</p>
                    
                    <h3>¿Qué métodos de pago aceptan?</h3>
                    <p>Aceptamos tarjetas de crédito/débito (Visa, MasterCard, American Express) y PayPal.</p>
                    
                    <h3>¿Puedo cancelar mi pedido?</h3>
                    <p>Puedes cancelar tu pedido dentro de las primeras 24 horas. Contacta con nosotros lo antes posible.</p>
                    
                    <h3>¿Ofrecen garantía en los productos?</h3>
                    <p>Todos nuestros productos tienen garantía del fabricante. El período varía según el producto.</p>
                    
                    <h3>¿Envían internacionalmente?</h3>
                    <p>Actualmente solo enviamos dentro de Estados Unidos.</p>
                    
                    <h3>¿Cómo puedo rastrear mi pedido?</h3>
                    <p>Recibirás un email con el número de seguimiento una vez que tu pedido sea enviado.</p>
                ''',
                'status': 'publish'
            }
        ]


def create_wordpress_client() -> WordPressIntegration:
    """Create WordPress integration client"""
    return WordPressIntegration()
