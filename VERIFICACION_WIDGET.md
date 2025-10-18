# ✅ Checklist de Verificación del Widget

## Desktop (Escritorio)

- [ ] Widget visible en sidebar/homepage
- [ ] 6 productos mostrados correctamente
- [ ] Precios visibles ($89.99, $129.99, etc.)
- [ ] Badges de descuento funcionando (15% OFF, 20% OFF, etc.)
- [ ] Códigos de descuento legibles (TALADRO15, SIERRA20, etc.)
- [ ] Botones "Ver Producto →" funcionando
- [ ] Links apuntan a productos correctos
- [ ] Hover effects funcionando (cards se elevan al pasar mouse)
- [ ] Animación de entrada funcionando (cards aparecen con fade-in)
- [ ] Colores y diseño coherentes con tu marca

## Mobile (Móvil)

- [ ] Widget responsive (se adapta a pantalla pequeña)
- [ ] Cards en 1 columna (no lado a lado)
- [ ] Texto legible sin hacer zoom
- [ ] Botones fáciles de presionar
- [ ] Scrolling vertical funciona bien
- [ ] No hay elementos cortados

## Funcionalidad

- [ ] Click en botón lleva a página de producto
- [ ] Código de descuento se puede copiar
- [ ] Precios actualizados correctamente
- [ ] Descuentos calculados correctamente:
  - Taladro: $89.99 (15% OFF de $105.88) ✓
  - Sierra: $129.99 (20% OFF de $162.49) ✓
  - Organizador: $69.99 (15% OFF de $82.34) ✓
  - Nivel: $79.99 (25% OFF de $106.65) ✓
  - Multi: $84.99 (20% OFF de $106.24) ✓
  - Drill: $149.99 (15% OFF de $174.99) ✓

## Rendimiento

- [ ] Widget carga rápido (<2 segundos)
- [ ] No afecta velocidad del resto de la página
- [ ] Imágenes optimizadas (si añadiste)
- [ ] CSS se aplica correctamente

## SEO y Accesibilidad

- [ ] Links tienen texto descriptivo
- [ ] Colores tienen buen contraste
- [ ] Texto legible
- [ ] Códigos de descuento copiables

---

## 🐛 Problemas Comunes

### Widget No Aparece

**Solución 1:** Verifica que el área de widgets esté activa
```
Apariencia → Widgets → Verifica que "Sidebar" esté disponible
```

**Solución 2:** Limpia caché
```
Plugins → WP Super Cache → Delete Cache
O tu plugin de caché
```

**Solución 3:** Cambia de ubicación
- Intenta en "Footer" en vez de "Sidebar"
- O directamente en una página

### Diseño Roto

**Solución:** Verifica que el CSS se copió completo
- El código debe tener las etiquetas `<style>` y `</style>`
- No debe haber código cortado

### Links No Funcionan

**Solución:** Actualiza las URLs
```html
<!-- Cambia esto: -->
href="https://herramientasyaccesorios.store/producto/taladro-inalambrico"

<!-- Por la URL real de WooCommerce -->
href="https://herramientasyaccesorios.store/?product=taladro"
```

### Colores No Match con Tu Marca

**Solución:** Personaliza el gradiente
```css
/* Busca esta línea: */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Cámbiala por tus colores */
```

---

## 🎯 Próximos Pasos

Una vez verificado:

1. **Toma screenshot** del widget funcionando
2. **Comparte en redes** para promocionar
3. **Monitorea clicks** en los próximos días
4. **Ajusta productos** según performance

---

## 📊 Métricas a Trackear

### En Google Analytics:
- Clicks en botones del widget
- Conversiones desde widget
- Productos más clickeados

### En WooCommerce:
- Ventas por producto featured
- Uso de códigos del widget
- Tráfico desde homepage vs otras páginas

### En el Agente:
- Featured products performance
- Actualizar precios semanalmente
- Rotar productos según ventas

---

## 🔄 Mantenimiento

### Semanal:
- Actualizar precios si cambian
- Verificar que códigos siguen activos
- Cambiar productos featured si es necesario

### Mensual:
- Analizar qué productos generan más clicks
- Ajustar orden de productos
- Probar diferentes calls-to-action

---

**¡Widget listo para monetizar! 💰**
