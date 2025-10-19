# 🤖 Personalización de Prompts AI - Guía Completa

## ✨ ¡SÍ! Puedes personalizar completamente los prompts

El plugin ahora incluye una página de **Configuración de Prompts** donde puedes personalizar exactamente cómo la IA genera el contenido.

## 📍 Cómo Acceder

1. Ir a WordPress Admin
2. **AI Dropshipping** → **🤖 Prompts AI**
3. Verás 5 secciones de prompts editables

## 🎯 Prompts Personalizables

### 1. 📝 Prompt: Descripción de Producto
Controla cómo se generan las descripciones SEO.

**Variables disponibles:**
- `{product_name}` - Nombre del producto
- `{category}` - Categoría del producto
- `{features}` - Lista de características

**Ejemplo de personalización:**
```
Crea una descripción EMOCIONANTE para vender:

Producto: {product_name}
Categoría: {category}

Quiero:
1. Un título que suene premium
2. 3 párrafos cortos y directos
3. 5 beneficios con íconos ✅
4. Precio psicológico (mencionar ahorro)
5. Urgencia (stock limitado)

Tono: Entusiasta y persuasivo
Longitud: Máximo 300 palabras
```

### 2. 🖼️ Prompt: Generación de Imágenes
Controla el estilo de las imágenes generadas.

**Variables disponibles:**
- `{product_name}` - Nombre del producto
- `{category}` - Categoría
- `{style}` - Estilo solicitado

**Ejemplo de personalización:**
```
Create a stunning lifestyle photo of {product_name}.

Style: Magazine cover quality
Setting: Modern minimalist home
Lighting: Natural window light, golden hour
Composition: Product in use by happy customer
Colors: Warm tones, Instagram aesthetic
Mood: Aspirational, premium, desirable

8K resolution, professional photography
```

### 3. 📊 Prompt: Análisis de Mercado
Controla qué información de mercado investigar.

**Variables disponibles:**
- `{product_name}` - Nombre del producto
- `{category}` - Categoría

**Ejemplo de personalización:**
```
Investiga el mercado ESPAÑOL de {product_name} ({category}).

PRIORIDAD ALTA:
1. Precio promedio en Amazon.es
2. Precio en ManoMano.es
3. Precio en Leroy Merlin
4. Reviews más comunes (positivos y negativos)

PRIORIDAD MEDIA:
5. Tendencia de búsquedas en Google (España)
6. Estacionalidad (¿cuándo se busca más?)
7. Palabras clave long-tail

FORMATO: JSON con precios_competencia, precio_recomendado, keywords
```

### 4. 📱 Prompt: Contenido de Redes Sociales
Controla los posts generados.

**Variables disponibles:**
- `{product_name}` - Nombre del producto
- `{description}` - Descripción
- `{platforms}` - Plataformas (instagram, facebook, twitter)

**Ejemplo de personalización:**
```
Crea posts VIRALES para {product_name}.

INSTAGRAM:
- Hook en primera línea (pregunta o estadística)
- 3 beneficios con emojis
- CTA: "Link en bio 👆"
- 10 hashtags mixtos (populares + nichos)
- Mejor hora: 19:00-21:00

FACEBOOK:
- Historia corta de uso del producto
- Pregunta al final para engagement
- Tono: Conversacional, amigable
- 5 hashtags máximo

TWITTER:
- Thread de 3 tweets
- Primera línea enganchadora
- Datos o beneficios concretos
- Incluir pregunta para replies
```

### 5. 📧 Prompt: Campaña de Email
Controla los emails generados.

**Variables disponibles:**
- `{product_name}` - Nombre del producto
- `{description}` - Descripción
- `{target_audience}` - Audiencia objetivo

**Ejemplo de personalización:**
```
Crea un email de LANZAMIENTO para {product_name}.

ASUNTO (3 variaciones):
1. Con urgencia (stock limitado)
2. Con curiosidad (pregunta)
3. Con beneficio directo (ahorra X%)

ESTRUCTURA:
- Preheader: 1 frase que complemente el asunto
- Héroe: Imagen del producto + título impactante
- Problema: 2 párrafos sobre el dolor que resuelve
- Solución: 3 beneficios del producto
- Social proof: "Únete a X clientes satisfechos"
- CTA principal: Botón grande "Comprar ahora"
- CTA secundario: "Ver más detalles"
- Urgencia: "Oferta válida 48 horas"
- PS: Recordatorio de beneficio principal

Tono: {target_audience} (ajustar según audiencia)
```

## 💡 Consejos para Prompts Efectivos

### ✅ Buenas Prácticas

1. **Sé Específico**
   ```
   ❌ Crea una buena descripción
   ✅ Crea una descripción de 200 palabras con tono profesional y 5 beneficios con emojis
   ```

2. **Usa Estructura Clara**
   ```
   ✅ Usa números y viñetas
   ✅ Separa secciones con saltos de línea
   ✅ Usa MAYÚSCULAS para énfasis
   ```

3. **Especifica el Formato de Salida**
   ```
   ✅ Formato: JSON con claves {title, description, keywords}
   ✅ Formato: HTML con tags <h2>, <ul>, <li>
   ✅ Formato: Texto plano, máximo 500 caracteres
   ```

4. **Define el Tono**
   ```
   ✅ Tono: Profesional y técnico
   ✅ Tono: Casual y amigable
   ✅ Tono: Urgente y persuasivo
   ```

5. **Incluye Ejemplos si es Necesario**
   ```
   ✅ Ejemplo de título: "🔥 La Mejor Sierra Circular - ¡50% de Descuento!"
   ```

### ⚠️ Evitar

1. **Prompts Demasiado Largos**
   - Máximo 500 palabras por prompt
   - La IA puede "olvidar" instrucciones al final

2. **Prompts Vagos**
   ```
   ❌ Haz algo bueno
   ❌ Hazlo interesante
   ```

3. **Contradicciones**
   ```
   ❌ Sé breve... proporciona todos los detalles posibles
   ```

4. **Variables Incorrectas**
   ```
   ❌ {nombre_producto} ← No existe
   ✅ {product_name} ← Correcto
   ```

## 🔄 Restaurar Valores por Defecto

Si tus prompts personalizados no funcionan bien:

1. Ir a **AI Dropshipping** → **🤖 Prompts AI**
2. Click en **🔄 Restaurar Valores por Defecto**
3. Confirmar
4. Los prompts volverán a la configuración original

## 🧪 Probar tus Prompts

1. Guarda tus prompts personalizados
2. Ve a **Productos** → Editar cualquier producto
3. Usa los botones AI del meta box
4. Los nuevos prompts se aplicarán inmediatamente

## 📊 Ejemplos de Uso por Industria

### Herramientas (actual)
```
Lenguaje técnico, especificaciones detalladas, seguridad
```

### Moda
```
Lenguaje aspiracional, tendencias, looks sugeridos
```

### Alimentación
```
Lenguaje sensorial, recetas, valores nutricionales
```

### Electrónica
```
Especificaciones técnicas, comparativas, compatibilidad
```

### Juguetes
```
Lenguaje educativo, desarrollo infantil, seguridad
```

## 💾 Respaldo de Prompts

Los prompts se guardan en la base de datos de WordPress en:
- `wp_options` tabla
- Keys: `ai_dropship_prompt_*`

Para hacer backup manual:
```sql
SELECT * FROM wp_options WHERE option_name LIKE 'ai_dropship_prompt_%';
```

## 🎨 Variables Dinámicas Disponibles

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{product_name}` | Nombre del producto | "Sierra Circular Makita" |
| `{category}` | Categoría principal | "Herramientas Eléctricas" |
| `{features}` | Lista de características | "1200W, Disco 7 pulgadas" |
| `{description}` | Descripción corta | "Sierra profesional..." |
| `{base_price}` | Precio base | "199.99" |
| `{style}` | Estilo de imagen | "professional product photo" |
| `{platforms}` | Plataformas sociales | "instagram, facebook" |
| `{target_audience}` | Audiencia objetivo | "profesionales" |

## 🚀 Casos de Uso Avanzados

### 1. Multilenguaje
```
Genera en ESPAÑOL para España (con "tú"):
Producto: {product_name}

O genera en ESPAÑOL LATAM (con "vos"):
Producto: {product_name}
```

### 2. Segmentación por Precio
```
Si precio > €100: Tono premium, mencionar calidad
Si precio < €100: Tono accesible, mencionar valor
```

### 3. SEO Local
```
Incluye keywords locales:
- España: "comprar en España", "envío península"
- México: "envío CDMX", "pago en pesos"
```

## 📞 Soporte

¿Necesitas ayuda personalizando prompts?
- Revisa ejemplos en esta guía
- Prueba con productos de prueba primero
- Itera y mejora basado en resultados

---

**Recuerda**: Los prompts son poderosos. Experimenta y encuentra tu estilo perfecto para cada tipo de producto.
