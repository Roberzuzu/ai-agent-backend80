#!/usr/bin/env python3
"""
Create test data for payment system testing
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://backend-verify-6.preview.emergentagent.com/api"

def create_test_products():
    """Create test products for checkout testing"""
    products = [
        {
            "name": "Taladro Profesional DeWalt 20V",
            "description": "Taladro inalámbrico profesional con batería de litio 20V, ideal para trabajos pesados de construcción y carpintería.",
            "price": 149.99,
            "affiliate_link": "https://amzn.to/3example1",
            "discount_code": "DRILL20",
            "discount_percentage": 15.0,
            "category": "Herramientas Eléctricas",
            "image_url": "https://example.com/drill.jpg",
            "is_featured": True
        },
        {
            "name": "Kit de Destornilladores Precision Pro",
            "description": "Set completo de 32 destornilladores de precisión para electrónicos, relojes y dispositivos pequeños.",
            "price": 29.99,
            "affiliate_link": "https://amzn.to/3example2",
            "discount_code": "PRECISION10",
            "discount_percentage": 10.0,
            "category": "Herramientas Manuales",
            "image_url": "https://example.com/screwdrivers.jpg",
            "is_featured": False
        },
        {
            "name": "Sierra Circular Makita 7-1/4",
            "description": "Sierra circular profesional con motor de 15 amperios, perfecta para cortes precisos en madera y materiales de construcción.",
            "price": 199.99,
            "affiliate_link": "https://amzn.to/3example3",
            "discount_code": "SAW25",
            "discount_percentage": 25.0,
            "category": "Herramientas Eléctricas",
            "image_url": "https://example.com/saw.jpg",
            "is_featured": True
        }
    ]
    
    created_products = []
    for product in products:
        try:
            response = requests.post(
                f"{BASE_URL}/products",
                json=product,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                created_product = response.json()
                created_products.append(created_product)
                print(f"✅ Created product: {product['name']} (${product['price']})")
            else:
                print(f"❌ Failed to create product {product['name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating product {product['name']}: {str(e)}")
    
    return created_products

def create_test_campaigns():
    """Create test campaigns for ROI testing"""
    campaigns = [
        {
            "name": "Campaña Black Friday Herramientas",
            "description": "Promoción especial de Black Friday para herramientas eléctricas con descuentos hasta 30%",
            "budget": 500.0,
            "platform": "facebook",
            "target_audience": {
                "age_range": "25-55",
                "interests": ["herramientas", "bricolaje", "construcción"],
                "location": "España"
            },
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "end_date": (datetime.now() - timedelta(days=15)).isoformat()
        },
        {
            "name": "Campaña Google Ads Precisión",
            "description": "Campaña dirigida para herramientas de precisión y electrónicos",
            "budget": 300.0,
            "platform": "google",
            "target_audience": {
                "keywords": ["destornilladores precisión", "herramientas electrónicos"],
                "location": "España, México, Argentina"
            },
            "start_date": (datetime.now() - timedelta(days=20)).isoformat(),
            "end_date": (datetime.now() - timedelta(days=5)).isoformat()
        }
    ]
    
    created_campaigns = []
    for campaign in campaigns:
        try:
            response = requests.post(
                f"{BASE_URL}/campaigns",
                json=campaign,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                created_campaign = response.json()
                created_campaigns.append(created_campaign)
                print(f"✅ Created campaign: {campaign['name']} (${campaign['budget']} budget)")
            else:
                print(f"❌ Failed to create campaign {campaign['name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating campaign {campaign['name']}: {str(e)}")
    
    return created_campaigns

def main():
    """Create all test data"""
    print("🚀 Creating Test Data for Payment System")
    print("=" * 50)
    
    print("\n📦 Creating Test Products...")
    products = create_test_products()
    
    print(f"\n📈 Creating Test Campaigns...")
    campaigns = create_test_campaigns()
    
    print("\n" + "=" * 50)
    print(f"✅ Test data creation complete!")
    print(f"   Products created: {len(products)}")
    print(f"   Campaigns created: {len(campaigns)}")
    print("\n🔄 Ready to run payment system tests!")

if __name__ == "__main__":
    main()