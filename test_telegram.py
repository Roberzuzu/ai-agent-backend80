#!/usr/bin/env python3
"""
Script to test Telegram notifications
"""
import requests
import os

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '7202793910')

def test_telegram_direct():
    """Test sending message directly to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    text = """<b>🎉 Test de Notificación Directa</b>

Este es un mensaje de prueba enviado directamente desde el script de testing.

✅ Sistema de notificaciones funcionando correctamente
📱 Telegram Bot integrado
🔔 Notificaciones automáticas activas

🔗 <a href='http://localhost:3000/notifications'>Ver en el sistema</a>"""
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Mensaje enviado exitosamente a Telegram!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing Telegram notifications...")
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")
    print()
    test_telegram_direct()
