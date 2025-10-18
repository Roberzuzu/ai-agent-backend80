# 🎨 Dashboard Mejorado - Guía de Usuario

## ✨ Nuevas Funcionalidades Implementadas

### 1. **Dashboard Analytics Avanzado** 📊

Accede al nuevo dashboard en la ruta `/dashboard-enhanced` o haciendo click en "Analytics" en la navegación.

#### Características Principales:

**📈 Gráficos Interactivos**
- **Revenue Timeline**: Visualiza ingresos día a día
- **Conversion Sources**: Distribución de conversiones por canal (Pie Chart)
- **Campaign Performance**: Rendimiento de las top 5 campañas (Bar Chart)

**🎯 Filtros de Fecha**
Analiza tus métricas en diferentes períodos:
- 7 días
- 30 días (por defecto)
- 90 días
- 1 año

**📊 Widgets de Métricas**

1. **Afiliados**
   - Total de afiliados
   - Afiliados activos
   - Clicks totales
   - Comisiones generadas

2. **Carritos Abandonados**
   - Total de carritos
   - Carritos abandonados
   - Carritos recuperados
   - Tasa de abandono

3. **Tests A/B**
   - Tests activos
   - Tests completados
   - Mejora promedio

4. **Email Marketing**
   - Campañas activas
   - Emails enviados
   - Tasa de apertura
   - Tasa de clicks

**📈 Comparación de Períodos**
Cada métrica principal muestra:
- Valor actual
- % de cambio vs período anterior
- Indicador visual (↑ positivo, ↓ negativo)

### 2. **Error Boundaries** 🛡️

El sistema ahora captura errores automáticamente y muestra:
- Mensaje amigable al usuario
- Opciones de recuperación (recargar o ir al inicio)
- Detalles técnicos en modo desarrollo
- Contacto a soporte

### 3. **Retry Logic en APIs** 🔄

Todas las llamadas al backend incluyen:
- **3 intentos automáticos** en caso de error
- **Exponential backoff**: 1s, 2s, 4s entre intentos
- **Notificaciones automáticas** con toast messages
- **Auto-redirect** si la sesión expira

### 4. **Toast Notifications** 🔔

Sistema de notificaciones integrado que muestra:
- ✅ Éxito en operaciones
- ❌ Errores con mensajes claros
- ℹ️ Información relevante
- ⚠️ Advertencias

Los mensajes aparecen automáticamente en la esquina superior derecha.

## 🚀 Cómo Usar

### Acceder al Dashboard Mejorado

1. Inicia sesión en la aplicación
2. Haz click en **"Analytics"** en la barra de navegación
3. Selecciona el rango de fechas que deseas analizar
4. Explora los diferentes widgets y gráficos

### Actualizar Datos

- Click en el botón de **refresh** (↻) para actualizar las métricas
- Los datos se actualizan automáticamente al cambiar el filtro de fecha

### Exportar Datos

- Click en el botón de **download** (↓) para exportar los datos
- Se generará un reporte con todas las métricas actuales

## 🎨 Componentes Reutilizables

### StatCard
Tarjeta de estadística con comparación de períodos:

```jsx
<StatCard
  title="Total Ingresos"
  value={1500}
  icon={DollarSign}
  color="green"
  prefix="$"
  comparison={{
    value: 12.5,
    isPositive: true,
    period: 'vs mes anterior'
  }}
/>
```

### ChartCard
Container para gráficos con loading states:

```jsx
<ChartCard
  title="Revenue Timeline"
  description="Últimos 30 días"
  loading={false}
  height="300px"
>
  <Line data={chartData} options={chartOptions} />
</ChartCard>
```

### DateRangeFilter
Filtro de rangos de fecha:

```jsx
<DateRangeFilter 
  selectedRange={30} 
  onRangeChange={(days) => setSelectedRange(days)}
/>
```

## 🛠️ Para Desarrolladores

### Backend Endpoint

```
GET /api/analytics/dashboard-enhanced?days=30
```

**Parámetros:**
- `days` (opcional): Número de días a consultar (default: 30)

**Respuesta:**
```json
{
  "period": {
    "days": 30,
    "start_date": "2025-09-18T...",
    "end_date": "2025-10-18T..."
  },
  "metrics": {
    "revenue": { "current": 0, "previous": 0, "change_percent": 0 },
    "transactions": { "current": 0, "previous": 0 },
    "affiliates": { "total": 0, "active": 0, "total_clicks": 0 },
    "cart_abandonment": { ... },
    "ab_tests": { ... },
    "email_campaigns": { ... }
  },
  "charts": {
    "revenue_timeline": [...],
    "conversion_sources": {...},
    "campaign_performance": [...]
  }
}
```

### Axios con Retry

```javascript
import axiosInstance from '@/lib/axiosConfig';

// Uso normal - retry automático
const response = await axiosInstance.get('/api/some-endpoint');

// Con opciones adicionales
import { apiRequest } from '@/lib/axiosConfig';

const { data, error } = await apiRequest(
  () => axiosInstance.post('/api/create', payload),
  {
    showSuccessToast: true,
    successMessage: 'Creado exitosamente'
  }
);
```

## 📋 Checklist de Testing

- [ ] Dashboard carga correctamente
- [ ] Gráficos se renderizan
- [ ] Filtros de fecha funcionan
- [ ] Botón refresh actualiza datos
- [ ] Toast notifications aparecen en errores
- [ ] Error boundary captura errores
- [ ] Retry logic funciona en errores de red
- [ ] Widgets muestran datos correctos
- [ ] Comparaciones de períodos son precisas
- [ ] Responsive en mobile

## 🎯 Próximos Pasos

1. Testear todas las funcionalidades
2. Validar datos con usuarios reales
3. Agregar más tipos de gráficos según necesidad
4. Implementar exportación real (CSV/Excel)
5. Agregar filtros adicionales (por producto, campaña, etc.)

## 💡 Tips

- Usa el filtro de 7 días para análisis diarios
- Usa 30 días para análisis mensuales
- El refresh automático no está habilitado para optimizar performance
- Los datos simulados (carritos, A/B tests, email) serán reemplazados con datos reales

---

**¿Preguntas o sugerencias?**  
Contacta al equipo de desarrollo o abre un issue en el repositorio.
