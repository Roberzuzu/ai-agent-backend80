"""
Setup script to get Instagram Business Account ID and Facebook Page ID
"""

import os
import requests
from dotenv import load_dotenv, set_key
from pathlib import Path

ROOT_DIR = Path(__file__).parent
env_file = ROOT_DIR / '.env'
load_dotenv(env_file)

def get_facebook_page_info():
    """Get Facebook Page ID and info"""
    access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    
    url = "https://graph.facebook.com/v18.0/me/accounts"
    params = {'access_token': access_token}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data and len(data['data']) > 0:
        page = data['data'][0]
        print(f"\n✅ Facebook Page encontrada:")
        print(f"   Name: {page.get('name')}")
        print(f"   ID: {page.get('id')}")
        print(f"   Category: {page.get('category')}")
        return page.get('id')
    else:
        print("\n❌ No se encontró página de Facebook")
        return None

def get_instagram_business_account(page_id):
    """Get Instagram Business Account ID linked to Facebook Page"""
    access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    params = {
        'fields': 'instagram_business_account',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'instagram_business_account' in data:
        ig_id = data['instagram_business_account']['id']
        print(f"\n✅ Instagram Business Account encontrada:")
        print(f"   ID: {ig_id}")
        
        # Get Instagram username
        url = f"https://graph.facebook.com/v18.0/{ig_id}"
        params = {
            'fields': 'username,name,profile_picture_url',
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        ig_data = response.json()
        
        print(f"   Username: @{ig_data.get('username')}")
        print(f"   Name: {ig_data.get('name')}")
        
        return ig_id
    else:
        print("\n❌ No se encontró cuenta de Instagram Business vinculada")
        print("   Asegúrate de tener una cuenta Instagram Business vinculada a tu Facebook Page")
        return None

def update_env_file(fb_page_id, ig_account_id):
    """Update .env file with IDs"""
    if fb_page_id:
        set_key(env_file, 'FACEBOOK_PAGE_ID', fb_page_id)
        print(f"\n✅ FACEBOOK_PAGE_ID actualizado en .env")
    
    if ig_account_id:
        set_key(env_file, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', ig_account_id)
        print(f"✅ INSTAGRAM_BUSINESS_ACCOUNT_ID actualizado en .env")

if __name__ == "__main__":
    print("="*60)
    print("  CONFIGURACIÓN DE CUENTAS DE REDES SOCIALES")
    print("="*60)
    
    # Get Facebook Page
    fb_page_id = get_facebook_page_info()
    
    # Get Instagram Account
    ig_account_id = None
    if fb_page_id:
        ig_account_id = get_instagram_business_account(fb_page_id)
    
    # Update .env file
    if fb_page_id or ig_account_id:
        update_env_file(fb_page_id, ig_account_id)
        print("\n" + "="*60)
        print("  ✅ CONFIGURACIÓN COMPLETADA")
        print("="*60)
        print("\n  Reinicia el backend para aplicar cambios:")
        print("  sudo supervisorctl restart backend")
    else:
        print("\n" + "="*60)
        print("  ❌ NO SE PUDO COMPLETAR LA CONFIGURACIÓN")
        print("="*60)
        print("\n  Verifica:")
        print("  1. Los tokens son correctos")
        print("  2. Tienes una Facebook Page creada")
        print("  3. Tienes Instagram Business vinculado a la Page")
