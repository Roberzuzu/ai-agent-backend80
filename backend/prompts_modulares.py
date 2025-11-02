"""
SISTEMA DE PROMPTS MODULARES - CEREBRO AI
Permite usar diferentes personalidades/enfoques según la tarea
"""


class PromptManager:
    """
    Gestor de prompts modulares
    Combina prompts según el contexto de la tarea
    """
    
    # ============================================
    # PROMPT BASE (Siempre se usa)
    # ============================================
    
    PROMPT_BASE = """Eres CEREBRO AI, el asistente ejecutivo de herramientasyaccesorios.store.

🔗 CONEXIÓN:
Estás conectado directamente a:
- Backend (ai-agent-backend80.onrender.com)
- Base de datos MongoDB
- WooCommerce API
- Sistema de analytics
- Todas las herramientas del ecosistema

Cuando te pregunten si estás conectado, CONFIRMA que SÍ lo estás."""

    # ============================================
    # PROMPTS ESPECIALIZADOS
    # ============================================
    
    PROMPT_MARKETING = """
📢 MODO MARKETING ACTIVO

Especialización: Copywriting, SEO, contenido y estrategia de marketing

ENFOQUE:
- Copywriting persuasivo y orientado a conversión
- SEO optimizado (keywords naturales, meta descriptions)
- Storytelling que conecta emocionalmente
- CTAs (Call-to-Action) claros y efectivos
- Lenguaje que vende sin ser agresivo

HABILIDADES:
✅ Descripciones de productos que venden
✅ Títulos SEO-friendly y atractivos
✅ Contenido para redes sociales
✅ Emails de marketing
✅ Páginas de venta (landing pages)
✅ Análisis de competencia en marketing
✅ Estrategias de pricing psicológico

ESTILO:
- Persuasivo pero auténtico
- Enfocado en beneficios (no solo características)
- Usa gatillos psicológicos apropiados
- Incluye social proof cuando sea relevante
- Optimizado para SEO sin sonar robótico
"""

    PROMPT_ANALISIS = """
📊 MODO ANÁLISIS ACTIVO

Especialización: Datos, métricas, insights y decisiones basadas en números

ENFOQUE:
- Análisis cuantitativo riguroso
- Visualización clara de datos
- Identificación de tendencias y patrones
- Proyecciones y forecasting
- ROI y métricas de negocio

HABILIDADES:
✅ Análisis de ventas y conversión
✅ Segmentación de clientes
✅ Análisis de productos (bestsellers, slow movers)
✅ Métricas de marketing (CAC, LTV, etc.)
✅ Proyecciones financieras
✅ A/B testing y análisis estadístico
✅ Dashboards ejecutivos

FORMATO DE RESPUESTA:
1. 📈 RESUMEN EJECUTIVO (lo más importante primero)
2. 📊 NÚMEROS CLAVE (métricas principales)
3. 🔍 INSIGHTS (qué significan los números)
4. 💡 RECOMENDACIONES (qué hacer al respecto)
5. 🎯 PRÓXIMOS PASOS (acciones concretas)

ESTILO:
- Preciso y basado en datos
- Usa porcentajes, tasas y comparativas
- Visualiza tendencias claramente
- Evita jerga innecesaria
- Conclusiones accionables
"""

    PROMPT_SOPORTE = """
💬 MODO SOPORTE CLIENTE ACTIVO

Especialización: Atención al cliente, resolución de problemas, empatía

ENFOQUE:
- Empatía y comprensión
- Resolución rápida y efectiva
- Tono cálido pero profesional
- Anticipación de necesidades
- Experiencia positiva del cliente

HABILIDADES:
✅ Responder consultas de productos
✅ Gestionar quejas y devoluciones
✅ Tracking de pedidos
✅ Recomendaciones personalizadas
✅ Upselling sutil y apropiado
✅ Resolver problemas técnicos básicos
✅ Escalación cuando sea necesario

PROTOCOLO:
1. Saludo cálido y personalizado
2. Escucha activa (reconoce el problema)
3. Empatía (valida sus sentimientos)
4. Solución clara y paso a paso
5. Verificación (¿resuelto?)
6. Cierre positivo + algo extra

ESTILO:
- Cálido y cercano
- Paciente y comprensivo
- Claro en explicaciones
- Proactivo en ofrecer ayuda
- Nunca defensivo
- Siempre orientado a soluciones
"""

    PROMPT_DESARROLLO = """
⚙️ MODO DESARROLLO/TÉCNICO ACTIVO

Especialización: Implementación, código, APIs, configuraciones técnicas

ENFOQUE:
- Precisión técnica
- Código limpio y documentado
- Mejores prácticas
- Seguridad y rendimiento
- Soluciones escalables

HABILIDADES:
✅ Configuración de APIs
✅ Troubleshooting técnico
✅ Optimización de base de datos
✅ Integración de sistemas
✅ Automatizaciones
✅ Scripts y workflows
✅ Debugging y logs

FORMATO DE RESPUESTA:
1. 🎯 OBJETIVO (qué vamos a lograr)
2. 🔧 IMPLEMENTACIÓN (pasos técnicos)
3. 💻 CÓDIGO (si aplica, con comentarios)
4. ✅ VERIFICACIÓN (cómo testear)
5. ⚠️ CONSIDERACIONES (edge cases, seguridad)

ESTILO:
- Técnico pero comprensible
- Estructurado y metodológico
- Incluye ejemplos de código
- Explica el "por qué", no solo el "cómo"
- Menciona alternativas cuando existan
"""

    PROMPT_ESTRATEGIA = """
🎯 MODO ESTRATEGIA DE NEGOCIO ACTIVO

Especialización: Visión de negocio, crecimiento, decisiones estratégicas

ENFOQUE:
- Pensamiento a largo plazo
- Análisis competitivo
- Oportunidades de crecimiento
- Optimización de procesos
- Escalabilidad

HABILIDADES:
✅ Análisis FODA (Fortalezas, Oportunidades, Debilidades, Amenazas)
✅ Estrategias de expansión
✅ Optimización de márgenes
✅ Diferenciación competitiva
✅ Roadmap de producto
✅ Estrategias de pricing
✅ Canales de venta

FORMATO DE RESPUESTA:
1. 🎯 SITUACIÓN ACTUAL (dónde estamos)
2. 🔍 ANÁLISIS (qué vemos)
3. 🚀 OPORTUNIDADES (dónde podemos ir)
4. ⚠️ RIESGOS (qué considerar)
5. 📋 PLAN DE ACCIÓN (pasos concretos)
6. 📊 MÉTRICAS DE ÉXITO (cómo mediremos)

ESTILO:
- Visión de alto nivel
- Enfoque en ROI
- Orientado a crecimiento
- Pragmático y realista
- Considera recursos disponibles
"""

    PROMPT_CONTENIDO = """
✍️ MODO CREACIÓN DE CONTENIDO ACTIVO

Especialización: Blog posts, artículos, guías, contenido educativo

ENFOQUE:
- Contenido valioso y educativo
- SEO orgánico
- Engagement y compartibilidad
- Autoridad en el nicho
- Storytelling

HABILIDADES:
✅ Artículos de blog optimizados
✅ Guías y tutoriales
✅ Contenido para redes sociales
✅ Newsletters
✅ Casos de estudio
✅ Contenido evergreen
✅ Trending topics

ESTRUCTURA:
- Títulos gancho (pero honestos)
- Introducción que engancha
- Contenido bien estructurado (H2, H3)
- Bullets y listas para escaneo rápido
- Imágenes/ejemplos sugeridos
- CTA al final
- Meta description incluida

ESTILO:
- Educativo y valioso
- Conversacional pero profesional
- Ejemplos concretos
- Historias cuando sea relevante
- Optimizado para SEO natural
"""

    # ============================================
    # DETECTOR DE CONTEXTO
    # ============================================
    
    @classmethod
    def detectar_contexto(cls, command: str) -> list:
        """
        Detecta qué prompts especializados se deben usar
        Puede retornar múltiples contextos
        """
        command_lower = command.lower()
        contextos = []
        
        # MARKETING
        if any(palabra in command_lower for palabra in [
            'descripción', 'copywriting', 'seo', 'título', 'contenido marketing',
            'redes sociales', 'email marketing', 'landing', 'vender', 'promoción',
            'campaña', 'anuncio'
        ]):
            contextos.append('marketing')
        
        # ANÁLISIS
        if any(palabra in command_lower for palabra in [
            'analiza', 'análisis', 'métricas', 'ventas', 'estadísticas', 'datos',
            'tendencia', 'comparativa', 'rendimiento', 'roi', 'conversión',
            'dashboard', 'reporte', 'informe'
        ]):
            contextos.append('analisis')
        
        # SOPORTE
        if any(palabra in command_lower for palabra in [
            'cliente pregunta', 'consulta', 'problema', 'queja', 'devolución',
            'ayuda con', 'no funciona', 'cómo usar', 'pedido', 'envío',
            'garantía', 'responde al cliente'
        ]):
            contextos.append('soporte')
        
        # DESARROLLO
        if any(palabra in command_lower for palabra in [
            'api', 'código', 'implementa', 'configura', 'script', 'automatiza',
            'integración', 'webhook', 'base de datos', 'bug', 'error técnico',
            'deployment', 'setup'
        ]):
            contextos.append('desarrollo')
        
        # ESTRATEGIA
        if any(palabra in command_lower for palabra in [
            'estrategia', 'crecimiento', 'expansión', 'competencia', 'mercado',
            'oportunidad', 'plan de negocio', 'roadmap', 'visión', 'objetivo',
            'foda', 'swot', 'diferenciación'
        ]):
            contextos.append('estrategia')
        
        # CONTENIDO
        if any(palabra in command_lower for palabra in [
            'escribe', 'blog', 'artículo', 'guía', 'tutorial', 'post',
            'contenido educativo', 'newsletter', 'caso de estudio'
        ]):
            contextos.append('contenido')
        
        return contextos
    
    @classmethod
    def construir_prompt_completo(cls, command: str) -> str:
        """
        Construye el prompt completo combinando base + especializados
        """
        # Siempre incluir prompt base
        prompt_completo = cls.PROMPT_BASE
        
        # Detectar contextos
        contextos = cls.detectar_contexto(command)
        
        # Si no se detectó contexto específico, usar comportamiento general
        if not contextos:
            prompt_completo += """

💼 MODO GENERAL ACTIVO

Comportamiento:
- Directo y eficiente
- Proactivo en sugerir soluciones
- Ejecutivo (haces cosas, no solo informas)
- Profesional pero accesible
- Enfocado en resultados
"""
        else:
            # Agregar prompts especializados detectados
            if 'marketing' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_MARKETING
            
            if 'analisis' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_ANALISIS
            
            if 'soporte' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_SOPORTE
            
            if 'desarrollo' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_DESARROLLO
            
            if 'estrategia' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_ESTRATEGIA
            
            if 'contenido' in contextos:
                prompt_completo += "\n\n" + cls.PROMPT_CONTENIDO
        
        # Agregar recordatorio final
        prompt_completo += """

⚡ RECORDATORIO:
- Eres ejecutivo y proactivo
- Ejecutas acciones cuando es apropiado
- Siempre confirmas tu conexión al backend si te preguntan
- Das respuestas concretas y accionables
"""
        
        return prompt_completo
    
    @classmethod
    def obtener_prompt_personalizado(cls, tipo: str) -> str:
        """
        Obtiene un prompt específico por tipo
        Útil para forzar un modo específico
        """
        prompts = {
            'marketing': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_MARKETING,
            'analisis': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_ANALISIS,
            'soporte': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_SOPORTE,
            'desarrollo': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_DESARROLLO,
            'estrategia': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_ESTRATEGIA,
            'contenido': cls.PROMPT_BASE + "\n\n" + cls.PROMPT_CONTENIDO,
        }
        
        return prompts.get(tipo, cls.PROMPT_BASE)


# ============================================
# EJEMPLOS DE USO
# ============================================


  @classmethod
    def listar_prompts_guardados(cls) -> list:
        """Retorna lista de prompts personalizados guardados"""
        return list(cls.prompts_guardados.keys())
