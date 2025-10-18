# 🔄 AUTOMATIZACIÓN WORDPRESS - Guía Completa

## ✅ YA IMPLEMENTADO

**Conexión Base:**
- ✓ WooCommerce API conectada
- ✓ Sincronización de productos funcionando
- ✓ Creación de blog posts
- ✓ 10 productos ya sincronizados

**Nuevos Endpoints Añadidos:**
- ✓ Sincronización automática de productos featured
- ✓ Actualización masiva de precios
- ✓ Creación de landing pages por categoría
- ✓ Widget de productos destacados

---

## 🎯 SEMANA 3: PLAN DE AUTOMATIZACIÓN

### DÍA 1-2: Sincronización Automática de Productos

#### Implementación Actual

**Endpoint 1: Sincronizar Solo Featured** ⭐
```bash
# Sincroniza automáticamente solo productos destacados
POST /api/wordpress/auto-sync-featured

# Respuesta:
{
  "total_featured": 6,
  "synced": 6,
  "results": [...]
}
```

**Endpoint 2: Sincronizar Todos**
```bash
POST /api/wordpress/sync-all-products
```

**Endpoint 3: Actualizar Precios**
```bash
# Actualiza precios de productos ya sincronizados
POST /api/wordpress/update-prices

# Útil cuando cambias descuentos o precios
```

#### Workflow Automático Sugerido

**Setup Diario (Cron Job):**
```bash
# Cada mañana a las 8 AM
# 1. Sincroniza productos nuevos featured
curl -X POST http://localhost:8001/api/wordpress/auto-sync-featured

# 2. Actualiza precios de todos
curl -X POST http://localhost:8001/api/wordpress/update-prices
```

**Cómo Programar (Linux/Mac):**
```bash
# Editar crontab
crontab -e

# Añadir línea:
0 8 * * * curl -X POST http://tu-dominio.com/api/wordpress/auto-sync-featured
0 8 * * * curl -X POST http://tu-dominio.com/api/wordpress/update-prices
```

---

### DÍA 3-4: Posts de Blog Automáticos

#### Sistema Implementado

**Endpoint: Crear Blog Post**
```bash
POST /api/wordpress/create-blog-post/{content_id}

# Ejemplo:
curl -X POST http://localhost:8001/api/wordpress/create-blog-post/CONTENT_ID

# Respuesta:
{
  "success": true,
  "post_id": 1234,
  "permalink": "https://herramientasyaccesorios.store/blog/...",
  "message": "Blog post created"
}
```

#### Workflow Automático

**Opción 1: Manual (Actual)**
1. Ve a Content Creator
2. Genera contenido con IA
3. Revisa y aprueba
4. Click en "Publish to WordPress"
5. ¡Post en tu blog!

**Opción 2: Automático (Implementar)**
```python
# Script que ejecutas semanalmente
import requests

API = "http://localhost:8001/api"

# 1. Obtener contenido aprobado
content_list = requests.get(f"{API}/content?status=approved").json()

# 2. Publicar cada uno en WordPress
for content in content_list:
    response = requests.post(
        f"{API}/wordpress/create-blog-post/{content['id']}"
    )
    print(f"Published: {content['title']}")
    
    # 3. Actualizar estado en el agente
    requests.patch(
        f"{API}/content/{content['id']}/status?status=published"
    )
```

**Guardar como:** `/app/scripts/auto_publish_blog.py`

**Ejecutar semanalmente:**
```bash
# Domingo a las 9 PM
0 21 * * 0 python3 /app/scripts/auto_publish_blog.py
```

---

### DÍA 5: Widget de Productos Destacados

#### Código del Widget Generado

El sistema ahora puede generar código HTML/CSS para un widget que muestra tus productos destacados.

**Usar en WordPress:**

1. **Ve a WordPress Admin** → Apariencia → Widgets

2. **Añade Widget HTML Personalizado**

3. **Pega este código:**

```html
<div id="featured-products-widget" class="featured-products">
    <h3>🔧 Productos Destacados</h3>
    <div class="products-slider">
        
        <!-- Producto 1: Taladro -->
        <div class="product-card">
            <h4>Taladro Inalámbrico 20V</h4>
            <p class="price">$89.99</p>
            <p class="discount">15% OFF - Código: TALADRO15</p>
            <a href="https://herramientasyaccesorios.store/producto/taladro" class="btn">Ver Producto</a>
        </div>
        
        <!-- Producto 2: Sierra -->
        <div class="product-card">
            <h4>Sierra Circular 7.25"</h4>
            <p class="price">$129.99</p>
            <p class="discount">20% OFF - Código: SIERRA20</p>
            <a href="https://herramientasyaccesorios.store/producto/sierra" class="btn">Ver Producto</a>
        </div>
        
        <!-- Producto 3: Organizador -->
        <div class="product-card">
            <h4>Organizador de Pared</h4>
            <p class="price">$69.99</p>
            <p class="discount">15% OFF - Código: ORGAN15</p>
            <a href="https://herramientasyaccesorios.store/producto/organizador" class="btn">Ver Producto</a>
        </div>
        
        <!-- Producto 4: Nivel Láser -->
        <div class="product-card">
            <h4>Nivel Láser 360°</h4>
            <p class="price">$79.99</p>
            <p class="discount">25% OFF - Código: NIVEL25</p>
            <a href="https://herramientasyaccesorios.store/producto/nivel" class="btn">Ver Producto</a>
        </div>
        
        <!-- Producto 5: Multiherramienta -->
        <div class="product-card">
            <h4>Multiherramienta 350W</h4>
            <p class="price">$84.99</p>
            <p class="discount">20% OFF - Código: MULTI20</p>
            <a href="https://herramientasyaccesorios.store/producto/multi" class="btn">Ver Producto</a>
        </div>
        
    </div>
</div>

<style>
.featured-products {
    padding: 30px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    margin: 30px 0;
    color: white;
}
.featured-products h3 {
    text-align: center;
    font-size: 28px;
    margin-bottom: 25px;
    color: white;
}
.products-slider {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}
.product-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.product-card h4 {
    margin: 0 0 15px 0;
    color: #333;
    font-size: 18px;
    min-height: 50px;
}
.product-card .price {
    font-size: 28px;
    font-weight: bold;
    color: #27ae60;
    margin: 10px 0;
}
.product-card .discount {
    background: #e74c3c;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    display: inline-block;
    margin: 10px 0;
    font-weight: 600;
}
.product-card .btn {
    display: block;
    background: #3498db;
    color: white;
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    text-decoration: none;
    margin-top: 15px;
    font-weight: 600;
    transition: background 0.3s ease;
}
.product-card .btn:hover {
    background: #2980b9;
    transform: scale(1.05);
}

@media (max-width: 768px) {
    .products-slider {
        grid-template-columns: 1fr;
    }
}
</style>
```

**Ubicaciones Recomendadas:**
- Sidebar derecho (todas las páginas)
- Después del contenido principal (posts)
- Homepage (arriba del fold)
- Páginas de categoría

---

### DÍA 6-7: Landing Pages por Categoría

#### Sistema de Landing Pages

El agente ahora puede crear automáticamente landing pages para cada categoría de productos.

**Endpoint:**
```bash
POST /api/wordpress/create-category-pages

# Crea páginas para:
# - /tools (Herramientas)
# - /accessories (Accesorios)
# - /equipment (Equipamiento)
# - /parts (Repuestos)
# - /safety (Seguridad)
```

**Cada landing page incluye:**
- Título SEO optimizado
- Descripción de la categoría
- Grid con todos los productos
- Códigos de descuento destacados
- CTAs para cada producto

#### Estructura de Landing Page

```html
<!-- Ejemplo: /herramientas -->
<div class="category-landing">
    <header class="category-hero">
        <h1>Las Mejores Herramientas Profesionales de 2025</h1>
        <p>Descubre nuestra selección de herramientas con descuentos exclusivos</p>
    </header>
    
    <section class="products-grid">
        <!-- Producto 1 -->
        <div class="product-item">
            <img src="..." alt="Taladro">
            <h3>Taladro Inalámbrico 20V</h3>
            <p>Taladro profesional con 2 baterías...</p>
            <div class="price-box">
                <span class="price">$89.99</span>
                <span class="discount">15% OFF</span>
            </div>
            <code class="discount-code">TALADRO15</code>
            <a href="..." class="cta-button">Ver Detalles →</a>
        </div>
        
        <!-- Más productos... -->
    </section>
    
    <section class="category-benefits">
        <h2>¿Por Qué Comprar Herramientas Aquí?</h2>
        <ul>
            <li>✓ Descuentos exclusivos hasta 25% OFF</li>
            <li>✓ Productos profesionales certificados</li>
            <li>✓ Envío rápido en 24-48h</li>
            <li>✓ Garantía extendida incluida</li>
        </ul>
    </section>
</div>
```

**SEO Optimizado:**
- Meta título: "Herramientas Profesionales | Descuentos hasta 25% OFF"
- Meta descripción: "Compra herramientas profesionales con descuentos exclusivos. Taladros, sierras, lijadoras y más. Envío gratis en pedidos +$50."
- URL amigable: `/herramientas/`

---

## 🔄 AUTOMATIZACIÓN COMPLETA

### Script Master de Sincronización

Crea este archivo: `/app/scripts/wordpress_sync_all.sh`

```bash
#!/bin/bash

API="http://localhost:8001/api"

echo "=========================================="
echo "  SINCRONIZACIÓN WORDPRESS AUTOMÁTICA"
echo "=========================================="
echo ""

# 1. Sincronizar productos featured
echo "1. Sincronizando productos destacados..."
curl -s -X POST "$API/wordpress/auto-sync-featured" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'✓ {d[\"synced\"]} productos sincronizados')"
echo ""

# 2. Actualizar precios
echo "2. Actualizando precios en WooCommerce..."
curl -s -X POST "$API/wordpress/update-prices" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'✓ {d[\"updated\"]} precios actualizados')"
echo ""

# 3. Publicar contenido aprobado
echo "3. Publicando contenido aprobado en blog..."
content_ids=$(curl -s "$API/content?status=approved" | python3 -c "import sys, json; print(' '.join([c['id'] for c in json.load(sys.stdin)]))")

for id in $content_ids; do
    curl -s -X POST "$API/wordpress/create-blog-post/$id" > /dev/null
    echo "✓ Post publicado: $id"
    curl -s -X PATCH "$API/content/$id/status?status=published" > /dev/null
done
echo ""

# 4. Verificar estado
echo "4. Estado final:"
curl -s "$API/wordpress/status" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'Conexión: {d[\"message\"]}')"
echo ""

echo "=========================================="
echo "  ✅ SINCRONIZACIÓN COMPLETADA"
echo "=========================================="
```

**Hacer ejecutable:**
```bash
chmod +x /app/scripts/wordpress_sync_all.sh
```

**Ejecutar manualmente:**
```bash
/app/scripts/wordpress_sync_all.sh
```

**Programar automáticamente:**
```bash
# Cada día a las 8 AM
0 8 * * * /app/scripts/wordpress_sync_all.sh >> /var/log/wp_sync.log 2>&1
```

---

## 📊 DASHBOARD DE MONITOREO

### Ver Estado de Sincronización

**Desde el Agente:**
```bash
# Ver dashboard
curl http://localhost:8001/api/analytics/dashboard

# Ver productos sincronizados
curl http://localhost:8001/api/products | python3 -c "
import sys, json
products = json.load(sys.stdin)
synced = [p for p in products if p.get('wc_product_id')]
print(f'Productos totales: {len(products)}')
print(f'Sincronizados: {len(synced)}')
print(f'Pendientes: {len(products) - len(synced)}')
"
```

**Desde WordPress:**
1. Ve a WooCommerce → Productos
2. Verifica que aparezcan los productos del agente
3. Chequea precios y descuentos

---

## 🎯 MEJORES PRÁCTICAS

### Sincronización de Productos

**DO ✓**
- Sincroniza solo productos featured primero
- Actualiza precios después de cambiar descuentos
- Usa imágenes de buena calidad
- Verifica que los links funcionen

**DON'T ✗**
- No sincronices productos sin describir bien
- No cambies precios en WooCommerce y el agente por separado
- No olvides actualizar el stock

### Posts de Blog

**DO ✓**
- Revisa contenido generado por IA antes de publicar
- Añade imágenes relevantes
- Incluye links a productos relacionados
- Usa keywords en el título

**DON'T ✗**
- No publiques contenido sin revisar
- No olvides añadir CTAs
- No ignores el SEO

### Landing Pages

**DO ✓**
- Una landing page por categoría principal
- Optimiza para SEO
- Incluye todos los productos de la categoría
- Añade testimonios si tienes

**DON'T ✗**
- No crees demasiadas páginas (confusión)
- No dupliques contenido
- No olvides los códigos de descuento

---

## 🚀 RESULTADOS ESPERADOS

### Semana 3 (Fin):

**Productos:**
- ✓ 12 productos en el agente
- ✓ 10-12 sincronizados en WooCommerce
- ✓ Precios actualizados diariamente
- ✓ Featured products destacados

**Contenido:**
- ✓ 5-10 posts de blog publicados
- ✓ SEO optimizado automáticamente
- ✓ Links a productos incluidos
- ✓ Tráfico orgánico comenzando

**Landing Pages:**
- ✓ 5 páginas de categoría creadas
- ✓ SEO para cada categoría
- ✓ Grid de productos funcional
- ✓ CTAs con códigos

**Widget:**
- ✓ Widget de productos featured en sidebar
- ✓ Visible en todas las páginas
- ✓ Responsive (móvil/desktop)
- ✓ Códigos de descuento visibles

---

## 📈 MÉTRICAS A TRACKEAR

### En WordPress Analytics:

- Visitas a landing pages
- CTR en widget de productos
- Conversiones desde blog posts
- Productos más visitados

### En WooCommerce:

- Ventas por producto
- Uso de códigos de descuento
- Tráfico desde cada fuente
- Carrito abandonado

### En el Agente:

- Productos sincronizados
- Posts publicados
- Contenido pendiente
- Featured products performance

---

## 🔧 TROUBLESHOOTING

**Productos no se sincronizan:**
```bash
# Verificar conexión
curl http://localhost:8001/api/wordpress/status

# Ver error específico
curl -X POST http://localhost:8001/api/wordpress/sync-product/PRODUCT_ID
```

**Precios incorrectos:**
```bash
# Forzar actualización
curl -X POST http://localhost:8001/api/wordpress/update-prices
```

**Posts no se crean:**
- Verifica credenciales de WordPress
- Chequea que el contenido esté "approved"
- Revisa permisos del usuario

---

## ✅ CHECKLIST SEMANA 3

**Día 1-2:**
- [ ] Ejecutar sincronización inicial de featured
- [ ] Verificar productos en WooCommerce
- [ ] Configurar actualización automática de precios

**Día 3-4:**
- [ ] Publicar 5 posts de blog desde contenido generado
- [ ] Verificar SEO de cada post
- [ ] Añadir imágenes a los posts

**Día 5:**
- [ ] Instalar widget de productos en sidebar
- [ ] Personalizar colores según tu marca
- [ ] Verificar responsive en móvil

**Día 6-7:**
- [ ] Crear landing pages de categorías
- [ ] Optimizar SEO de cada página
- [ ] Verificar todos los links funcionan
- [ ] Programar script de sincronización automática

---

**🎉 Al final de la semana 3 tendrás:**
- Sincronización automática diaria
- Blog activo con contenido IA
- Landing pages optimizadas
- Widget de productos funcionando
- Todo conectado y automatizado

**¿Listo para empezar? ¡Ejecuta el primer comando! 🚀**
