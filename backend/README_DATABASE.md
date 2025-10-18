# Database Optimization System

Sistema completo de optimización de base de datos MongoDB con índices, validaciones, migraciones y backups automáticos.

## 📚 Características

### ✅ 1. Sistema de Índices
- **Índices simples**: Email, status, created_at, etc.
- **Índices compuestos**: (user_email, status), (user_email, created_at)
- **Índices únicos**: Email, unique_code, session_id
- **Índices de texto**: Búsqueda full-text en productos
- **Índices sparse**: Para campos opcionales como stripe_subscription_id

### ✅ 2. Schema Validation
- Validación de tipos de datos
- Required fields
- Pattern matching (email format)
- Enum constraints (status values)
- Range validations (commission_rate: 0-100)

### ✅ 3. Sistema de Migraciones
- Migraciones versionadas con tracking
- Ejecución idempotente (no duplica migraciones)
- Rollback support
- Logging detallado de cada migración

### ✅ 4. Backups Automáticos
- Compresión gzip de backups
- Políticas de retención (default: 7 días)
- Límite de backups (default: 10)
- CLI para backup/restore manual
- Cron job para automatización

## 🚀 Uso

### Ejecutar Migraciones

**Al inicio de la aplicación:**
```bash
cd /app/backend
python3 init_db.py
```

**Manualmente:**
```bash
cd /app/backend
python3 -m database.migrations
```

### Backups

**Crear backup manual:**
```bash
cd /app/backend
python3 -m database.backup backup
```

**Listar backups disponibles:**
```bash
python3 -m database.backup list
```

**Restaurar desde backup:**
```bash
python3 -m database.backup restore --backup-file /app/backups/backup_20250118_120000.tar.gz
```

**Limpiar backups antiguos:**
```bash
python3 -m database.backup cleanup --retention-days 7 --max-backups 10
```

**Configurar cron job (ejecutar a las 2 AM diariamente):**
```bash
crontab -e
# Agregar:
0 2 * * * /app/backend/scripts/backup_cron.sh
```

## 📊 Colecciones Optimizadas

### 1. **users**
- Índices: email (unique), username (unique), role+is_active
- Validación: Email format, role enum, required fields

### 2. **products**
- Índices: category, is_featured, price, text search (name+description)
- Validación: Price > 0, required fields

### 3. **payment_transactions**
- Índices: user_email, payment_status, session_id (unique), user+status
- Validación: Amount > 0, payment_type/status enums

### 4. **subscriptions**
- Índices: user_email, status, user+status, stripe_subscription_id (unique)
- Validación: Status enum, required fields

### 5. **affiliates**
- Índices: email (unique), unique_code (unique), status
- Validación: Email format, commission_rate 0-100, status enum

### 6. **affiliate_links**
- Índices: affiliate_id, unique_code (unique), product_id
- Validación: Required fields

### 7. **affiliate_commissions**
- Índices: affiliate_id, status, affiliate+status, transaction_id
- Validación: Status enum, amounts > 0

### 8. **affiliate_payouts**
- Índices: affiliate_id, status, requested_at
- Validación: Status enum, amount > 0

### 9. **notifications**
- Índices: user_email, is_read, user+is_read, user+created_at, type
- Validación: Type enum, required fields, title/message min length

### 10. **campaigns**
- Índices: status, platform, date_range, created_at
- Validación: Status enum, required fields

### 11. **content_ideas**
- Índices: status, platform, content_type, created_at
- Validación: Status enum

### 12. **trends**
- Índices: platform, engagement_score, created_at
- Validación: Required fields

### 13. **social_posts**
- Índices: status, platform, scheduled_time, created_at
- Validación: Status enum

## 🔧 Migraciones Disponibles

| ID | Descripción | Estado |
|----|------------|--------|
| 001 | User indexes | ✅ |
| 002 | Product indexes | ✅ |
| 003 | Payment transaction indexes | ✅ |
| 004 | Subscription indexes | ✅ |
| 005 | Affiliate program indexes | ✅ |
| 006 | Notification indexes | ✅ |
| 007 | Campaign indexes | ✅ |
| 008 | Content and trend indexes | ✅ |
| 100 | User schema validation | ✅ |
| 101 | Payment schema validation | ✅ |
| 102 | Affiliate schema validation | ✅ |
| 103 | Notification schema validation | ✅ |

## 📈 Impacto en Performance

### Antes (sin índices):
- Query por email: **O(n)** - Scan completo
- Filtros por status: **O(n)** - Scan completo
- Ordenamiento: **O(n log n)** - Sort en memoria

### Después (con índices):
- Query por email: **O(log n)** - B-tree lookup
- Filtros por status: **O(log n)** - Index scan
- Ordenamiento: **O(1)** - Index order

### Mejoras esperadas:
- **Queries simples**: 10-100x más rápidas
- **Queries compuestas**: 50-500x más rápidas
- **Full-text search**: 100-1000x más rápido
- **Uso de memoria**: Reducción del 80-90%

## 🛡️ Schema Validation Benefits

1. **Integridad de datos**: Previene datos inválidos
2. **Debugging**: Errores claros cuando fallan validaciones
3. **Documentación**: Schema sirve como documentación
4. **Performance**: MongoDB puede optimizar mejor con schemas conocidos

## 📦 Estructura de Archivos

```
backend/
├── database/
│   ├── __init__.py         # Package initialization
│   ├── migrations.py       # Migration system
│   └── backup.py          # Backup system
├── scripts/
│   └── backup_cron.sh     # Cron job for automated backups
├── init_db.py             # Database initialization script
└── README_DATABASE.md     # This file
```

## ⚠️ Consideraciones

### Desarrollo vs Producción

**Desarrollo:**
- Validaciones en modo "warn" para debugging
- Backups menos frecuentes
- Retención más corta

**Producción:**
- Validaciones en modo "error" (strict)
- Backups diarios automáticos
- Retención 7-30 días
- Monitoreo de tamaño de índices

### Mantenimiento

**Verificar índices:**
```javascript
db.getCollectionNames().forEach(function(col) {
    print("\n=== " + col + " ===");
    printjson(db[col].getIndexes());
});
```

**Estadísticas de índices:**
```javascript
db.payment_transactions.stats().indexSizes
```

**Rebuild índices (si es necesario):**
```javascript
db.payment_transactions.reIndex()
```

## 🔄 Próximas Mejoras

- [ ] Compound indexes avanzados basados en query patterns
- [ ] Partial indexes para casos específicos
- [ ] TTL indexes para datos temporales
- [ ] Backup incremental
- [ ] Replica sets para HA (requiere infraestructura)
- [ ] Sharding para escalabilidad horizontal

## 📞 Soporte

Para más información sobre optimización de MongoDB:
- [MongoDB Indexing Best Practices](https://www.mongodb.com/docs/manual/indexes/)
- [Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [Backup Strategies](https://www.mongodb.com/docs/manual/core/backups/)
