# 🔌 INSTALACIÓN AUTOMÁTICA DEL WIDGET - Plugin WordPress

## ✅ PLUGIN CREADO

**Archivo:** `/app/widget-productos-destacados.php`

Este plugin instala automáticamente el widget de productos destacados en tu WordPress.

---

## 🚀 INSTALACIÓN EN 4 PASOS

### PASO 1: Descargar el Plugin

El archivo ya está listo en: `/app/widget-productos-destacados.php`

**Necesitas transferirlo a tu servidor WordPress.**

---

### PASO 2: Subir a WordPress

**Opción A: FTP/SFTP** (Recomendado)

1. Conecta vía FTP a tu servidor
2. Ve a: `/wp-content/plugins/`
3. Crea carpeta: `widget-productos-destacados`
4. Sube el archivo: `widget-productos-destacados.php`

**Opción B: cPanel File Manager**

1. Accede a cPanel de tu hosting
2. File Manager → `public_html/wp-content/plugins/`
3. Crear carpeta `widget-productos-destacados`
4. Upload → `widget-productos-destacados.php`

**Opción C: Por WordPress Admin** (Más fácil)

1. Ve a: https://herramientasyaccesorios.store/wp-admin
2. Plugins → Añadir nuevo → Subir plugin
3. Pero necesitas comprimir el archivo como .zip primero

---

### PASO 3: Activar el Plugin

1. Ve a: `Plugins → Plugins instalados`
2. Busca: "Widget Productos Destacados"
3. Click en "Activar"

✅ **¡Listo! El plugin ya está activo**

---

### PASO 4: Añadir el Widget

**Opción A: Como Widget en Sidebar**

1. Ve a: `Apariencia → Widgets`
2. Busca: "🔧 Productos Destacados"
3. Arrástralo al Sidebar (o Footer, o donde quieras)
4. ¡Listo! No necesita configuración

**Opción B: Con Shortcode en Cualquier Lugar**

Puedes usar el shortcode en cualquier página, post o área de texto:

```
[productos_destacados]
```

**Ejemplos de uso:**

- En Homepage: Edita página → Añade shortcode
- En Posts: Dentro del contenido
- En Widget de Texto: Sidebar → Text Widget → Añade shortcode
- En Footer: Apariencia → Personalizar → Footer → Añade shortcode

---

## 🎨 LO QUE INCLUYE EL PLUGIN

**Funcionalidades:**
- ✅ Widget instalable desde Apariencia → Widgets
- ✅ Shortcode `[productos_destacados]` para usar anywhere
- ✅ CSS automático (no necesitas añadir estilos)
- ✅ 6 productos featured con descuentos
- ✅ Responsive (móvil + desktop)
- ✅ Animaciones y hover effects
- ✅ Links dinámicos (se adaptan a tu dominio)

**Productos Incluidos:**
1. Taladro Inalámbrico 20V - $89.99 (TALADRO15)
2. Sierra Circular 7.25" - $129.99 (SIERRA20)
3. Organizador de Pared - $69.99 (ORGAN15)
4. Nivel Láser 360° - $79.99 (NIVEL25)
5. Multiherramienta 350W - $84.99 (MULTI20)
6. Professional Drill Kit - $149.99 (DRILL20)

---

## 🔧 ALTERNATIVA: Instalación Manual (Sin Plugin)

Si no puedes instalar el plugin, usa el método original:

1. Copia el contenido de `/app/WIDGET_PRODUCTOS.html`
2. WordPress → Apariencia → Widgets
3. Añade "HTML Personalizado"
4. Pega el código
5. Guarda

---

## 📦 CREAR ZIP DEL PLUGIN (Para subir por WordPress Admin)

Si quieres subirlo desde WordPress Admin, necesitas crear un .zip:

```bash
# En tu terminal local o servidor
cd /app
zip widget-productos-destacados.zip widget-productos-destacados.php

# Ahora puedes subirlo desde:
# WordPress → Plugins → Añadir nuevo → Subir plugin
```

---

## ✅ VERIFICACIÓN

**Después de activar el plugin:**

1. **Ver Widgets Disponibles:**
   - Apariencia → Widgets
   - Debe aparecer "🔧 Productos Destacados"

2. **Probar Shortcode:**
   - Crea página de prueba
   - Añade: `[productos_destacados]`
   - Previsualiza

3. **Ver en Frontend:**
   - Visita tu sitio
   - El widget debe aparecer donde lo colocaste
   - Verifica que se vea bien en móvil

---

## 🎯 UBICACIONES RECOMENDADAS

### Como Widget:
- ✅ Sidebar derecho (visible en todas las páginas)
- ✅ Footer (disponible en todo el sitio)
- ✅ Homepage widget area

### Como Shortcode:
- ✅ Página de inicio (máxima visibilidad)
- ✅ Después de posts de blog
- ✅ Página "Productos"
- ✅ Checkout page (como upsell)

---

## 🔄 ACTUALIZAR PRODUCTOS

Para cambiar productos o precios:

1. **Editar el Plugin:**
   - FTP → `/wp-content/plugins/widget-productos-destacados/`
   - Edita `widget-productos-destacados.php`
   - Busca las secciones de productos
   - Cambia nombres, precios, códigos, URLs

2. **Después de Editar:**
   - Guarda archivo
   - Limpia caché de WordPress
   - Refresca página

---

## 💡 PERSONALIZACIÓN

### Cambiar Colores:

Busca en el archivo esta línea:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Cámbiala por:
```css
/* Verde-Azul */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* Naranja-Rojo */
background: linear-gradient(135deg, #f12711 0%, #f5af19 100%);

/* Azul-Oscuro */
background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
```

### Cambiar Texto del Título:

Busca:
```html
<h3>🔧 Productos Destacados - Descuentos Hasta 25%</h3>
```

Cámbialo por lo que quieras:
```html
<h3>🔥 Ofertas Especiales - Solo Hoy</h3>
```

---

## 🆘 TROUBLESHOOTING

**Plugin no aparece en lista:**
```
Solución:
1. Verifica que el archivo esté en:
   /wp-content/plugins/widget-productos-destacados/widget-productos-destacados.php
2. El nombre de carpeta y archivo deben coincidir
```

**Widget no se ve:**
```
Solución:
1. Verifica que el plugin esté activado
2. Limpia caché: Plugins → WP Super Cache → Delete Cache
3. Verifica que el área de widgets esté activa en tu tema
```

**Shortcode muestra texto plano:**
```
Solución:
1. Verifica que el plugin esté activado
2. El shortcode es: [productos_destacados] (sin espacios)
3. Asegúrate de estar en modo HTML, no Visual
```

**CSS no se aplica:**
```
Solución:
1. Limpia caché del navegador (Ctrl+Shift+R)
2. Limpia caché de WordPress
3. Verifica que el plugin esté activado
```

---

## 📊 VENTAJAS DEL PLUGIN vs HTML Manual

| Característica | Plugin | HTML Manual |
|---|---|---|
| Instalación | Una vez | Cada vez que cambias |
| Actualizaciones | Fácil (edita 1 archivo) | Tedioso (edita cada widget) |
| Shortcode | ✅ Sí | ❌ No |
| Portable | ✅ Sí (export/import) | ❌ No |
| Mantenimiento | Fácil | Difícil |
| CSS | Automático | Manual |

---

## 🎉 ¡LISTO!

Una vez instalado el plugin:

✅ Widget disponible en Widgets
✅ Shortcode [productos_destacados] funcionando  
✅ CSS aplicado automáticamente
✅ 6 productos con descuentos visibles
✅ Responsive y con animaciones
✅ Listo para generar conversiones

---

## 📝 RESUMEN DE ARCHIVOS

1. **/app/widget-productos-destacados.php** - Plugin completo
2. **/app/WIDGET_PRODUCTOS.html** - Versión HTML standalone
3. **/app/INSTALAR_PLUGIN_WIDGET.md** - Esta guía

---

**¿Necesitas ayuda con la instalación? ¡Dime en qué paso estás y te guío! 🚀**
