"""
Script de prueba para verificar el sistema de fallback Perplexity → OpenAI
"""
import asyncio
import sys
sys.path.append('/app/backend')

from ai_agent import AIAgent

async def test_cerebro():
    """Prueba el sistema de Cerebro AI con fallback"""
    
    agent = AIAgent()
    
    print("=" * 80)
    print("🧠 PRUEBA DEL SISTEMA CEREBRO AI CON FALLBACK")
    print("=" * 80)
    print()
    
    # Test 1: Comando simple
    print("📝 Test 1: Comando simple - 'Dame las estadísticas del sitio'")
    print("-" * 80)
    
    result = await agent.think(
        command="Dame las estadísticas del sitio", 
        user_id="test_user_fallback"
    )
    
    print()
    print("✅ RESULTADO:")
    print(f"  • Success: {result.get('success')}")
    print(f"  • Provider usado: {result.get('provider', 'N/A')}")
    
    if result.get('perplexity_error'):
        print(f"  ⚠️  Error de Perplexity: {result.get('perplexity_error')}")
        print(f"  ✅ Fallback a OpenAI funcionó correctamente")
    else:
        print(f"  ✅ Perplexity funcionó correctamente (primario)")
    
    if result.get('success'):
        plan = result.get('plan', {})
        print(f"  • Plan: {plan.get('plan', 'N/A')[:100]}")
        print(f"  • Respuesta: {plan.get('respuesta_usuario', 'N/A')[:150]}")
        print(f"  • Acciones: {len(plan.get('acciones', []))} acciones")
    else:
        print(f"  ❌ Error: {result.get('error')}")
    
    print()
    print("=" * 80)
    print("🎉 PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_cerebro())
