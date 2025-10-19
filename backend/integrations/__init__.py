"""
Integrations package
FAL AI, WooCommerce, Dropshipping automation
"""
from .fal_ai import FALAIClient, get_fal_client
from .woocommerce import WooCommerceClient, get_woo_client, ProductContentGenerator
from .dropshipping_pricing import DropshippingPriceCalculator, calculate_price, calculate_bulk
from .automated_dropshipping import AutomatedDropshippingSystem, create_dropshipping_system

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
