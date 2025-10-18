# 🔌 API Examples - Agente de Monetización

Ejemplos prácticos de cómo usar la API del Agente de Monetización.

## 🌐 Base URL
```
http://localhost:8001/api
```

---

## 1️⃣ Growth Hacker (Tendencias)

### Crear una tendencia
```bash
curl -X POST http://localhost:8001/api/trends \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "youtube",
    "topic": "Best Power Tools for Beginners 2025",
    "engagement_score": 88,
    "keywords": ["power tools", "beginner", "2025", "diy"]
  }'
```

### Obtener todas las tendencias
```bash
curl http://localhost:8001/api/trends
```

### Filtrar por plataforma
```bash
curl "http://localhost:8001/api/trends?platform=tiktok&limit=10"
```

### Analizar tendencia con IA
```bash
curl -X POST http://localhost:8001/api/trends/TREND_ID/analyze
```

---

## 2️⃣ Content Creator

### Generar contenido con IA
```bash
curl -X POST http://localhost:8001/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "youtube",
    "content_type": "tutorial",
    "keywords": ["cordless drill", "woodworking", "beginner"]
  }'
```

### Con prompt personalizado
```bash
curl -X POST http://localhost:8001/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "tiktok",
    "content_type": "tips",
    "keywords": ["tool organization", "garage"],
    "custom_prompt": "Create a 60-second TikTok script about organizing tools in a small garage. Include trending sounds suggestions."
  }'
```

### Obtener todas las ideas de contenido
```bash
curl http://localhost:8001/api/content
```

### Filtrar por estado
```bash
curl "http://localhost:8001/api/content?status=draft"
curl "http://localhost:8001/api/content?status=approved"
curl "http://localhost:8001/api/content?status=published"
```

### Actualizar estado de contenido
```bash
# Aprobar contenido
curl -X PATCH "http://localhost:8001/api/content/CONTENT_ID/status?status=approved"

# Publicar contenido
curl -X PATCH "http://localhost:8001/api/content/CONTENT_ID/status?status=published"
```

---

## 3️⃣ Monetization Manager

### Crear producto
```bash
curl -X POST http://localhost:8001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DeWalt Cordless Drill Kit",
    "description": "Professional 20V MAX cordless drill with 2 batteries",
    "price": 179.99,
    "category": "tools",
    "affiliate_link": "https://amazon.com/dp/B00EXAMPLE",
    "discount_code": "DEWALT25",
    "discount_percentage": 25,
    "image_url": "https://example.com/drill.jpg",
    "is_featured": true
  }'
```

### Crear producto con bundle
```bash
curl -X POST http://localhost:8001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Complete Workshop Bundle",
    "description": "All tools you need to start woodworking",
    "price": 499.99,
    "category": "equipment",
    "discount_code": "BUNDLE50",
    "discount_percentage": 50,
    "is_featured": true,
    "bundle_products": ["product_id_1", "product_id_2", "product_id_3"]
  }'
```

### Obtener todos los productos
```bash
curl http://localhost:8001/api/products
```

### Filtrar productos
```bash
# Por categoría
curl "http://localhost:8001/api/products?category=tools"

# Solo productos destacados
curl "http://localhost:8001/api/products?is_featured=true"
```

### Obtener producto específico
```bash
curl http://localhost:8001/api/products/PRODUCT_ID
```

### Actualizar producto
```bash
curl -X PATCH http://localhost:8001/api/products/PRODUCT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "price": 159.99,
    "discount_percentage": 30,
    "is_featured": true
  }'
```

### Eliminar producto
```bash
curl -X DELETE http://localhost:8001/api/products/PRODUCT_ID
```

---

## 4️⃣ Social Manager

### Crear publicación
```bash
curl -X POST http://localhost:8001/api/social/posts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "instagram",
    "content": "🔧 New tool alert! Check out this amazing drill kit\n\nSave 25% with code DEWALT25\n\nLink in bio 👆\n\n#tools #diy #woodworking",
    "media_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ]
  }'
```

### Programar publicación
```bash
curl -X POST http://localhost:8001/api/social/posts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "tiktok",
    "content": "Quick tool hack! 🛠️ #toolhacks #diy",
    "media_urls": ["https://example.com/video.mp4"],
    "scheduled_time": "2025-10-25T10:00:00Z"
  }'
```

### Vincular con contenido y productos
```bash
curl -X POST http://localhost:8001/api/social/posts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "youtube",
    "content": "New tutorial: How to use a cordless drill",
    "content_id": "CONTENT_ID",
    "product_ids": ["PRODUCT_ID_1", "PRODUCT_ID_2"]
  }'
```

### Obtener publicaciones
```bash
# Todas
curl http://localhost:8001/api/social/posts

# Por plataforma
curl "http://localhost:8001/api/social/posts?platform=instagram"

# Por estado
curl "http://localhost:8001/api/social/posts?status=published"
```

### Actualizar estado de publicación
```bash
# Programar
curl -X PATCH "http://localhost:8001/api/social/posts/POST_ID/status?status=scheduled"

# Publicar
curl -X PATCH "http://localhost:8001/api/social/posts/POST_ID/status?status=published"

# Con engagement
curl -X PATCH http://localhost:8001/api/social/posts/POST_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "published",
    "engagement": {
      "likes": 1250,
      "comments": 45,
      "shares": 89
    }
  }'
```

---

## 5️⃣ Ad Manager

### Crear campaña
```bash
curl -X POST http://localhost:8001/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Black Friday Tool Sale 2025",
    "description": "Promote top power tools with special discounts",
    "budget": 500.00,
    "platform": "facebook",
    "target_audience": {
      "age_range": "25-54",
      "interests": ["DIY", "woodworking", "home improvement"],
      "location": "United States"
    },
    "start_date": "2025-11-24T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z"
  }'
```

### Obtener campañas
```bash
# Todas
curl http://localhost:8001/api/campaigns

# Solo activas
curl "http://localhost:8001/api/campaigns?status=active"
```

### Actualizar estado de campaña
```bash
# Pausar
curl -X PATCH "http://localhost:8001/api/campaigns/CAMPAIGN_ID/status?status=paused"

# Reactivar
curl -X PATCH "http://localhost:8001/api/campaigns/CAMPAIGN_ID/status?status=active"

# Completar
curl -X PATCH "http://localhost:8001/api/campaigns/CAMPAIGN_ID/status?status=completed"
```

### Actualizar métricas de performance
```bash
curl -X PATCH http://localhost:8001/api/campaigns/CAMPAIGN_ID/performance \
  -H "Content-Type: application/json" \
  -d '{
    "impressions": 15000,
    "clicks": 850,
    "conversions": 42,
    "spend": 287.50,
    "ctr": 5.67,
    "cpc": 0.34,
    "roas": 3.2
  }'
```

---

## 6️⃣ Analytics & Dashboard

### Obtener dashboard completo
```bash
curl http://localhost:8001/api/analytics/dashboard
```

Respuesta:
```json
{
  "totals": {
    "trends": 5,
    "content": 12,
    "products": 8,
    "posts": 20,
    "campaigns": 3
  },
  "stats": {
    "published_posts": 15,
    "active_campaigns": 2,
    "featured_products": 3
  },
  "recent_trends": [...],
  "top_posts": [...]
}
```

---

## 7️⃣ AI Generation (Custom)

### Generar contenido personalizado
```bash
curl -X POST http://localhost:8001/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create 5 engaging Instagram captions for a cordless drill promotion. Include emojis and hashtags.",
    "provider": "openai",
    "model": "gpt-4o",
    "max_tokens": 500
  }'
```

### Usar provider alternativo
```bash
# Con Emergent LLM Key
curl -X POST http://localhost:8001/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a YouTube video description about tool safety",
    "provider": "emergent",
    "model": "gpt-4o-mini"
  }'

# Con OpenRouter
curl -X POST http://localhost:8001/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a product comparison between two drill brands",
    "provider": "openrouter"
  }'
```

---

## 🔄 Flujos Completos

### Flujo 1: De Tendencia a Post Publicado
```bash
# 1. Crear tendencia
TREND_ID=$(curl -s -X POST http://localhost:8001/api/trends \
  -H "Content-Type: application/json" \
  -d '{"platform":"tiktok","topic":"Tool Storage Hacks","engagement_score":95,"keywords":["storage","tools","organization"]}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Analizar con IA
curl -X POST "http://localhost:8001/api/trends/$TREND_ID/analyze"

# 3. Generar contenido basado en la tendencia
CONTENT_ID=$(curl -s -X POST http://localhost:8001/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{"platform":"tiktok","content_type":"tips","keywords":["storage","organization","garage"]}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 4. Aprobar contenido
curl -X PATCH "http://localhost:8001/api/content/$CONTENT_ID/status?status=approved"

# 5. Crear post
curl -X POST http://localhost:8001/api/social/posts \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"tiktok\",\"content\":\"Amazing tool storage hack!\",\"content_id\":\"$CONTENT_ID\"}"
```

### Flujo 2: Lanzar Producto con Campaña
```bash
# 1. Crear producto
PRODUCT_ID=$(curl -s -X POST http://localhost:8001/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Pro Drill Kit","description":"Complete drill set","price":199.99,"category":"tools","discount_code":"PRO30","discount_percentage":30,"is_featured":true}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Crear campaña publicitaria
curl -X POST http://localhost:8001/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{"name":"Pro Drill Launch","description":"Launch campaign","budget":300,"platform":"facebook","start_date":"2025-10-20T00:00:00Z","end_date":"2025-10-27T23:59:59Z"}'

# 3. Crear posts promocionales
curl -X POST http://localhost:8001/api/social/posts \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"instagram\",\"content\":\"New Pro Drill Kit! 30% OFF\",\"product_ids\":[\"$PRODUCT_ID\"]}"
```

---

## 📝 Notas

- Todos los IDs son UUIDs v4
- Las fechas deben estar en formato ISO 8601 con timezone
- Los arrays (keywords, media_urls, product_ids) se pasan como arrays JSON
- El sistema usa hot reload, los cambios se reflejan automáticamente
- Para debugging, revisa logs: `tail -f /var/log/supervisor/backend.err.log`

---

## 🔐 Autenticación

Actualmente la API no requiere autenticación (single user). En producción multi-usuario se añadirá JWT.

---

**¡Listo para empezar a monetizar! 💰**
