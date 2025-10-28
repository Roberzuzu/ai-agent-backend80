"""
Integrations package for Cerebro AI
FAL AI, WooCommerce, Dropshipping automation
"""

try:
    from .fal_ai import FALAIClient, get_fal_client
except ImportError:
    FALAIClient = None
    get_fal_client = None

try:
    from .woocommerce import WooCommerceClient, get_woo_client, ProductContentGenerator
except ImportError:
    WooCommerceClient = None
    get_woo_client = None
    ProductContentGenerator = None

try:
    from .dropshipping_pricing import DropshippingPriceCalculator, calculate_price, calculate_bulk
except ImportError:
    DropshippingPriceCalculator = None
    calculate_price = None
    calculate_bulk = None

try:
    from .automated_dropshipping import AutomatedDropshippingSystem, create_dropshipping_system
except ImportError:
    AutomatedDropshippingSystem = None
    create_dropshipping_system = None

__all__ = [
    'FALAIClient',
    'get_fal_client',
    'WooCommerceClient',
    'get_woo_client',
    'ProductContentGenerator',
    'DropshippingPriceCalculator',
    'calculate_price',
    'calculate_bulk',
    'AutomatedDropshippingSystem',
    'create_dropshipping_system',
]
