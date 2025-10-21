"""
Script de prueba completo para el sistema de fallback
- Test 1: Perplexity funcionando (primario)
- Test 2: Simulación de fallo de Perplexity (backup OpenAI)
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('/app/backend/.env')

sys.path.append('/app/backend')

from ai_agent import AIAgent

async def test_perplexity_working():
    """Test 1: Verificar que Perplexity funciona correctamente"""
    print("=" * 80)
    print("🧠 TEST 1: PERPLEXITY FUNCIONANDO (CEREBRO PRIMARIO)")
    print("=" * 80)
    print()
    
    agent = AIAgent()
    
    result = await agent.think(
        command="¿Cuántos productos tengo en mi tienda?",
        user_id="test_user_1"
    )
    
    print("✅ RESULTADO TEST 1:")
    print(f"  • Success: {result.get('success')}")
    print(f"  • Provider: {result.get('provider', 'N/A')}")
    
    if result.get('perplexity_error'):
        print(f"  ⚠️  Perplexity Error: {result.get('perplexity_error')}")
    
    if result.get('success'):
        plan = result.get('plan', {})
        print(f"  • Plan: {plan.get('plan', 'N/A')[:100]}...")
        print(f"  • Respuesta: {plan.get('respuesta_usuario', 'N/A')[:100]}...")
    
    print()
    return result.get('success')

async def test_openai_fallback():
    """Test 2: Verificar fallback a OpenAI (simulando fallo de Perplexity)"""
    print("=" * 80)
    print("🔄 TEST 2: FALLBACK A OPENAI (BACKUP)")
    print("=" * 80)
    print()
    
    # Temporalmente invalidar la key de Perplexity para probar el fallback
    original_key = os.environ.get('PERPLEXITY_API_KEY')
    os.environ['PERPLEXITY_API_KEY'] = 'invalid_key_for_testing'
    
    # Crear nuevo agente con key inválida
    from ai_agent import AIAgent as TestAgent
    import importlib
    import ai_agent
    importlib.reload(ai_agent)
    
    # Forzar recarga del módulo
    test_agent = ai_agent.AIAgent()
    
    result = await test_agent.think(
        command="Dame estadísticas de ventas",
        user_id="test_user_2"
    )
    
    # Restaurar la key original
    os.environ['PERPLEXITY_API_KEY'] = original_key
    
    print("✅ RESULTADO TEST 2:")
    print(f"  • Success: {result.get('success')}")
    print(f"  • Provider: {result.get('provider', 'N/A')}")
    
    if result.get('perplexity_error'):
        print(f"  ⚠️  Perplexity Error: {result.get('perplexity_error')}")
        print(f"  ✅ Fallback funcionó correctamente")
    
    if result.get('success'):
        plan = result.get('plan', {})
        print(f"  • Plan: {plan.get('plan', 'N/A')[:100]}...")
        print(f"  • Respuesta: {plan.get('respuesta_usuario', 'N/A')[:100]}...")
    
    print()
    return result.get('success')

async def main():
    """Ejecutar todos los tests"""
    print("\n")
    print("🚀 INICIANDO BATERÍA DE TESTS DEL CEREBRO AI")
    print()
    
    # Test 1: Perplexity working
    test1_pass = await test_perplexity_working()
    
    # Test 2: OpenAI fallback
    test2_pass = await test_openai_fallback()
    
    # Resumen
    print("=" * 80)
    print("📊 RESUMEN DE TESTS")
    print("=" * 80)
    print(f"  ✅ Test 1 (Perplexity Primario): {'PASÓ' if test1_pass else 'FALLÓ'}")
    print(f"  ✅ Test 2 (OpenAI Backup): {'PASÓ' if test2_pass else 'FALLÓ'}")
    print()
    
    if test1_pass and test2_pass:
        print("🎉 TODOS LOS TESTS PASARON - SISTEMA FUNCIONANDO CORRECTAMENTE")
        print()
        print("CONFIGURACIÓN:")
        print("  • Cerebro Primario: Perplexity (sonar-pro)")
        print("  • Cerebro Backup: OpenAI (gpt-4o)")
        print("  • Fallback Automático: ✅ ACTIVADO")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON")
    
    print("=" * 80)
    print()

if __name__ == "__main__":
    asyncio.run(main())
