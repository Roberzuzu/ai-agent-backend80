#!/usr/bin/env python3
"""
Script para arreglar productos sin precio en WooCommerce
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from integrations.woocommerce import WooCommerceClient
from integrations.dropshipping_pricing import calculate_price

# Precios base estimados según categoría (precio de proveedor estimado)
CATEGORY_BASE_PRICES = {
    'herramienta': 35.0,
    'electrica': 45.0,
    'bateria': 55.0,
    'taladro': 65.0,
    'sierra': 75.0,
    'amoladora': 50.0,
    'atornillador': 40.0,
    'multiherramienta': 45.0,
    'kit': 60.0,
    'set': 50.0,
    'mini': 30.0,
    'profesional': 80.0,
    'inalambrica': 70.0,
    'combo': 90.0,
    'default': 40.0
}

def estimate_supplier_price(slug: str, description: str) -> float:
    """Estima el precio de proveedor basado en el slug y descripción"""
    text = f"{slug} {description}".lower()
    
    # Buscar palabras clave en el texto
    for keyword, price in CATEGORY_BASE_PRICES.items():
        if keyword in text:
            return price
    
    return CATEGORY_BASE_PRICES['default']

def extract_name_from_slug(slug: str) -> str:
    """Extrae un nombre legible del slug"""
    if not slug:
        return "Producto sin nombre"
    
    # Reemplazar guiones por espacios y capitalizar
    name = slug.replace('-', ' ').title()
    
    # Limitar longitud
    if len(name) > 100:
        name = name[:100]
    
    return name

def fix_products_without_price():
    """Arregla todos los productos sin precio"""
    print("🔧 Iniciando reparación de productos sin precio...\n")
    
    # Inicializar cliente WooCommerce
    wc = WooCommerceClient(
        store_url=os.getenv('WORDPRESS_URL'),
        consumer_key=os.getenv('WC_CONSUMER_KEY'),
        consumer_secret=os.getenv('WC_CONSUMER_SECRET')
    )
    
    # Obtener todos los productos
    print("📦 Obteniendo productos de WooCommerce...")
    products = wc.get_products()
    
    # Filtrar productos sin precio
    no_price_products = [
        p for p in products 
        if not p.get('price') or p.get('price') == '0' or p.get('price') == ''
    ]
    
    print(f"✅ Encontrados {len(no_price_products)} productos sin precio\n")
    
    if not no_price_products:
        print("✨ ¡Todos los productos ya tienen precio!")
        return
    
    fixed_count = 0
    errors = []
    
    for i, product in enumerate(no_price_products, 1):
        product_id = product['id']
        slug = product.get('slug', '')
        name = product.get('name', '')
        short_desc = product.get('short_description', '')
        
        print(f"\n[{i}/{len(no_price_products)}] Procesando producto ID: {product_id}")
        print(f"   Slug: {slug}")
        
        try:
            # Generar nombre si no existe
            if not name or name.strip() == '':
                name = extract_name_from_slug(slug)
                print(f"   ✏️  Nombre generado: {name}")
            
            # Estimar precio de proveedor
            supplier_price = estimate_supplier_price(slug, short_desc)
            print(f"   💰 Precio proveedor estimado: €{supplier_price:.2f}")
            
            # Calcular precio de venta con margen
            pricing = calculate_price(supplier_price, 'EUR')
            selling_price = pricing['selling_price_rounded']
            profit = pricing['profit']
            margin = pricing['margin_percentage'] * 100
            
            print(f"   💵 Precio de venta: €{selling_price:.2f}")
            print(f"   📊 Margen: {margin:.0f}% (€{profit:.2f} ganancia)")
            
            # Actualizar producto en WooCommerce
            update_data = {
                'regular_price': str(selling_price),
                'price': str(selling_price)
            }
            
            # Solo actualizar nombre si estaba vacío
            if not product.get('name') or product.get('name').strip() == '':
                update_data['name'] = name
            
            result = wc.update_product(product_id, update_data)
            
            if result:
                print(f"   ✅ Producto actualizado exitosamente")
                fixed_count += 1
            else:
                print(f"   ❌ Error al actualizar producto")
                errors.append(f"ID {product_id}: Error en actualización")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            errors.append(f"ID {product_id}: {str(e)}")
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE REPARACIÓN")
    print("="*60)
    print(f"✅ Productos reparados: {fixed_count}/{len(no_price_products)}")
    print(f"❌ Errores: {len(errors)}")
    
    if errors:
        print("\n⚠️  Errores encontrados:")
        for error in errors:
            print(f"   - {error}")
    
    print("\n✨ Proceso completado!")
    
    return {
        'total': len(no_price_products),
        'fixed': fixed_count,
        'errors': len(errors)
    }

if __name__ == "__main__":
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Ejecutar reparación
    fix_products_without_price()
