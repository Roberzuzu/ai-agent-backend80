# CONTENIDO OPTIMIZADO PARA HERRAMIENTASYACCESORIOS.STORE

## 📄 PÁGINAS ESENCIALES PARA WORDPRESS

---

## 1. PÁGINA DE INICIO (Homepage)

**Título SEO:** Herramientas y Accesorios Profesionales - Envío Gratis en Península | HerramientasyAccesorios.store

**Meta Description:** Compra herramientas eléctricas profesionales con envío gratis. Taladros, sierras, amoladoras y más. Garantía de 2 años. ¡Ofertas hasta 50% de descuento!

**Contenido:**

```html
<!-- HERO SECTION -->
<section class="hero-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 80px 20px; color: white; text-align: center;">
    <h1 style="font-size: 48px; font-weight: bold; margin-bottom: 20px;">
        🔧 Herramientas Profesionales para Profesionales
    </h1>
    <p style="font-size: 24px; margin-bottom: 30px;">
        Calidad superior al mejor precio. Envío gratis en pedidos superiores a €50
    </p>
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
        <a href="/tienda" class="btn-primary" style="background: white; color: #667eea; padding: 15px 40px; border-radius: 8px; font-weight: bold; text-decoration: none;">
            Ver Catálogo Completo →
        </a>
        <a href="#ofertas" class="btn-secondary" style="background: rgba(255,255,255,0.2); color: white; padding: 15px 40px; border-radius: 8px; font-weight: bold; text-decoration: none;">
            Ver Ofertas del Día 🔥
        </a>
    </div>
</section>

<!-- BENEFICIOS -->
<section style="padding: 60px 20px; max-width: 1200px; margin: 0 auto;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; text-align: center;">
        <div>
            <div style="font-size: 48px; margin-bottom: 15px;">🚚</div>
            <h3>Envío Gratis</h3>
            <p>En pedidos superiores a €50 en Península</p>
        </div>
        <div>
            <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
            <h3>Garantía 2 Años</h3>
            <p>Todas nuestras herramientas están garantizadas</p>
        </div>
        <div>
            <div style="font-size: 48px; margin-bottom: 15px;">💳</div>
            <h3>Pago Seguro</h3>
            <p>Paga con tarjeta, PayPal o transferencia</p>
        </div>
        <div>
            <div style="font-size: 48px; margin-bottom: 15px;">🎯</div>
            <h3>Mejor Precio</h3>
            <p>Garantía de devolución si encuentras más barato</p>
        </div>
    </div>
</section>

<!-- CATEGORÍAS DESTACADAS -->
<section id="categorias" style="padding: 60px 20px; background: #f8f9fa;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 40px;">
            🛠️ Explora por Categoría
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px;">
            <div class="category-card" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 64px; margin-bottom: 20px;">⚡</div>
                <h3>Herramientas Eléctricas</h3>
                <p>Taladros, amoladoras, sierras y más</p>
                <a href="/categoria/herramientas-electricas" style="color: #667eea; font-weight: bold;">Ver productos →</a>
            </div>
            <div class="category-card" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 64px; margin-bottom: 20px;">🔋</div>
                <h3>Herramientas a Batería</h3>
                <p>Libertad de movimiento, máxima potencia</p>
                <a href="/categoria/baterias" style="color: #667eea; font-weight: bold;">Ver productos →</a>
            </div>
            <div class="category-card" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 64px; margin-bottom: 20px;">🎁</div>
                <h3>Kits Profesionales</h3>
                <p>Sets completos al mejor precio</p>
                <a href="/categoria/kits" style="color: #667eea; font-weight: bold;">Ver productos →</a>
            </div>
            <div class="category-card" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 64px; margin-bottom: 20px;">🛡️</div>
                <h3>Seguridad y Protección</h3>
                <p>Guantes, gafas, cascos y más</p>
                <a href="/categoria/seguridad" style="color: #667eea; font-weight: bold;">Ver productos →</a>
            </div>
        </div>
    </div>
</section>

<!-- OFERTAS DEL DÍA -->
<section id="ofertas" style="padding: 60px 20px; max-width: 1200px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 36px; margin-bottom: 10px;">
            🔥 Ofertas del Día
        </h2>
        <p style="font-size: 18px; color: #666;">
            Ahorra hasta 50% en productos seleccionados. ¡Stock limitado!
        </p>
    </div>
    
    <!-- Aquí irán los productos destacados mediante shortcode de WooCommerce -->
    [products limit="8" columns="4" orderby="popularity" on_sale="true"]
</section>

<!-- TESTIMONIOS -->
<section style="padding: 60px 20px; background: #f8f9fa;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 40px;">
            ⭐ Lo que dicen nuestros clientes
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="color: #ffc107; font-size: 24px; margin-bottom: 15px;">★★★★★</div>
                <p style="font-style: italic; margin-bottom: 20px;">
                    "Excelente calidad y precio. El taladro llegó en 2 días y funciona perfectamente. 100% recomendado."
                </p>
                <p style="font-weight: bold;">- Carlos M., Madrid</p>
            </div>
            <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="color: #ffc107; font-size: 24px; margin-bottom: 15px;">★★★★★</div>
                <p style="font-style: italic; margin-bottom: 20px;">
                    "Compré un kit completo para mi taller. La relación calidad-precio es imbatible. Muy satisfecho."
                </p>
                <p style="font-weight: bold;">- Ana R., Barcelona</p>
            </div>
            <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="color: #ffc107; font-size: 24px; margin-bottom: 15px;">★★★★★</div>
                <p style="font-style: italic; margin-bottom: 20px;">
                    "Atención al cliente excelente. Tuve una duda y me respondieron en minutos. Volveré a comprar."
                </p>
                <p style="font-weight: bold;">- José L., Valencia</p>
            </div>
        </div>
    </div>
</section>

<!-- NEWSLETTER -->
<section style="padding: 80px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;">
    <div style="max-width: 600px; margin: 0 auto;">
        <h2 style="font-size: 36px; margin-bottom: 20px;">
            📧 Ofertas Exclusivas en tu Email
        </h2>
        <p style="font-size: 18px; margin-bottom: 30px;">
            Suscríbete y recibe un 10% de descuento en tu primera compra
        </p>
        <!-- Formulario de suscripción -->
        <form style="display: flex; gap: 10px; max-width: 500px; margin: 0 auto;">
            <input type="email" placeholder="tu@email.com" style="flex: 1; padding: 15px; border-radius: 8px; border: none; font-size: 16px;" required>
            <button type="submit" style="padding: 15px 30px; background: white; color: #667eea; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">
                Suscribir
            </button>
        </form>
        <p style="font-size: 12px; margin-top: 15px; opacity: 0.8;">
            No spam. Cancela cuando quieras.
        </p>
    </div>
</section>

<!-- TRUST BADGES -->
<section style="padding: 40px 20px; text-align: center; background: white;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 40px; flex-wrap: wrap; opacity: 0.6;">
        <div>🔒 Pago 100% Seguro</div>
        <div>✅ Envío 24-48h</div>
        <div>↩️ Devolución 30 días</div>
        <div>🏆 +5000 clientes satisfechos</div>
    </div>
</section>
```

**Shortcodes a usar en WordPress:**
- Productos en oferta: `[products limit="8" columns="4" orderby="popularity" on_sale="true"]`
- Productos destacados: `[featured_products per_page="8" columns="4"]`
- Últimos productos: `[recent_products per_page="8" columns="4"]`

---

## 2. PÁGINA "SOBRE NOSOTROS"

**Slug:** /sobre-nosotros

**Título SEO:** Sobre Nosotros - Herramientas Profesionales desde 2020 | HerramientasyAccesorios.store

**Meta Description:** Somos especialistas en herramientas profesionales. Más de 5 años ofreciendo calidad, precio y servicio. Conoce nuestra historia y compromiso.

**Contenido:**

```markdown
# Sobre HerramientasyAccesorios.store

## 🏭 Nuestra Historia

Desde 2020, **HerramientasyAccesorios.store** se ha consolidado como una de las tiendas online de referencia en España para herramientas profesionales y accesorios de calidad.

Nuestro compromiso es simple: **ofrecer las mejores herramientas al mejor precio**, con un servicio al cliente excepcional y garantía de satisfacción.

## 🎯 Nuestra Misión

Proporcionar a profesionales y aficionados al bricolaje herramientas de alta calidad que les permitan realizar sus proyectos con **seguridad, eficiencia y precisión**.

## ✨ Por Qué Elegirnos

### 1. **Calidad Garantizada**
Todos nuestros productos pasan controles de calidad rigurosos. Solo trabajamos con marcas reconocidas y proveedores certificados.

### 2. **Mejores Precios**
Gracias a nuestras alianzas directas con fabricantes, podemos ofrecer precios competitivos sin comprometer la calidad.

### 3. **Envío Rápido y Seguro**
- Envío gratis en pedidos +€50
- Entrega en 24-48h en Península
- Embalaje profesional para proteger tus herramientas

### 4. **Atención al Cliente Excepcional**
Nuestro equipo de expertos está disponible para ayudarte:
- 📧 Email: info@herramientasyaccesorios.store
- 📞 Teléfono: [Tu teléfono]
- 💬 Chat en línea: Lun-Vie 9:00-18:00

### 5. **Garantía de Satisfacción**
- ✅ 30 días de devolución sin preguntas
- ✅ 2 años de garantía en todos los productos
- ✅ Soporte técnico post-venta

## 📊 Nuestros Números

- 🎯 **+5,000 clientes satisfechos**
- ⭐ **4.8/5 valoración media**
- 📦 **+10,000 productos enviados**
- 🏆 **98% tasa de satisfacción**

## 🌱 Compromiso con el Medio Ambiente

Estamos comprometidos con la sostenibilidad:
- Embalajes reciclables
- Colaboración con proveedores responsables
- Compensación de huella de carbono en envíos

## 🤝 Únete a Nuestra Comunidad

Miles de profesionales y aficionados confían en nosotros. Síguenos en redes sociales para:
- Ver tutoriales y consejos
- Conocer nuevos productos
- Participar en sorteos exclusivos

[Botón: Conoce Nuestros Productos]
```

---

## 3. POLÍTICA DE ENVÍOS

**Slug:** /envios

**Título SEO:** Política de Envíos - Envío Gratis en Península | HerramientasyAccesorios.store

**Contenido:**

```markdown
# 🚚 Política de Envíos

## Envío Gratis en Península

**¡Envío gratuito en todos los pedidos superiores a €50!**

Para pedidos inferiores a €50, el coste de envío es de solo **€4.99**.

## ⏰ Plazos de Entrega

| Zona | Plazo | Coste |
|------|-------|-------|
| Península | 24-48h | Gratis +€50 / €4.99 |
| Baleares | 3-5 días | €9.99 |
| Canarias | 5-7 días | €14.99 |
| Ceuta y Melilla | 5-7 días | €14.99 |

## 📦 Procesamiento de Pedidos

- Pedidos realizados antes de las **14:00h** se procesan el mismo día
- Pedidos posteriores se procesan al siguiente día laborable
- Recibirás email con número de seguimiento

## 🔍 Seguimiento del Pedido

Una vez enviado tu pedido:
1. Recibirás un email con el número de seguimiento
2. Podrás rastrear tu paquete en tiempo real
3. El transportista te avisará antes de la entrega

## 📍 Opciones de Entrega

### Entrega a Domicilio
- En la dirección que indiques
- Horario: Lunes a Viernes, 9:00-19:00
- Sábados: Consultar disponibilidad

### Punto de Recogida
- Recoge en tu oficina de correos más cercana
- Horarios extendidos
- Máxima flexibilidad

## ❓ Preguntas Frecuentes

**¿Puedo cambiar mi dirección de envío?**
Sí, si el pedido aún no ha sido procesado. Contacta con nosotros inmediatamente.

**¿Qué pasa si no estoy en casa?**
El transportista dejará un aviso para recoger en oficina o coordinar nueva entrega.

**¿Hacen envíos internacionales?**
Actualmente solo enviamos a España. Próximamente Portugal y Francia.

## 📞 ¿Necesitas Ayuda?

Contacta con nuestro equipo:
- 📧 envios@herramientasyaccesorios.store
- 💬 Chat en línea
```

---

## 4. POLÍTICA DE DEVOLUCIONES

**Slug:** /devoluciones

**Título SEO:** Política de Devoluciones - 30 Días Garantía | HerramientasyAccesorios.store

**Contenido:**

```markdown
# ↩️ Política de Devoluciones

## 30 Días de Garantía

**Tienes 30 días desde la recepción para devolver cualquier producto sin preguntas.**

## ✅ Condiciones de Devolución

Para que tu devolución sea aceptada:

1. **Plazo:** Dentro de los 30 días desde la recepción
2. **Estado:** Producto sin usar, en su embalaje original
3. **Accesorios:** Con todos los accesorios y documentación
4. **Factura:** Copia de la factura de compra

## 🔄 Proceso de Devolución

### Paso 1: Solicitar Devolución
- Email a: devoluciones@herramientasyaccesorios.store
- Indica número de pedido y motivo
- Te enviaremos etiqueta de devolución

### Paso 2: Enviar el Producto
- Embala el producto de forma segura
- Pega la etiqueta de devolución
- Lleva a oficina de correos

### Paso 3: Reembolso
- Verificamos el producto (1-2 días)
- Procesamos el reembolso
- Dinero en tu cuenta en 5-7 días laborables

## 💰 Reembolsos

- **Método:** Mismo método de pago usado
- **Plazo:** 5-7 días laborables tras verificación
- **Gastos de envío:** No reembolsables (excepto productos defectuosos)

## 🔧 Productos Defectuosos

Si recibes un producto defectuoso:

1. **Contacta inmediatamente** (máximo 7 días)
2. Envía fotos del defecto
3. Te enviamos reemplazo o reembolso completo
4. **Incluye gastos de envío**

## 🔄 Cambios

¿Quieres cambiar por otro modelo?

1. Solicita devolución del producto original
2. Realiza nuevo pedido del producto deseado
3. Te aplicamos descuento del 5% en el nuevo

## ❌ Excepciones

No se aceptan devoluciones de:
- Productos personalizados
- Productos deteriorados por mal uso
- Productos sin embalaje original

## 📞 Contacto Devoluciones

- 📧 devoluciones@herramientasyaccesorios.store
- 📞 [Tu teléfono]
- Horario: Lun-Vie 9:00-18:00
```

---

## 5. PREGUNTAS FRECUENTES (FAQ)

**Slug:** /faq

**Título SEO:** Preguntas Frecuentes - Todo lo que Necesitas Saber | HerramientasyAccesorios.store

**Contenido:**

```markdown
# ❓ Preguntas Frecuentes (FAQ)

## 🛒 Sobre Pedidos

**¿Cómo realizo un pedido?**
1. Añade productos al carrito
2. Procede al checkout
3. Completa datos de envío
4. Selecciona método de pago
5. Confirma pedido

**¿Puedo modificar mi pedido?**
Sí, si aún no ha sido procesado. Contacta inmediatamente.

**¿Recibiré confirmación de mi pedido?**
Sí, recibirás email de confirmación inmediatamente.

## 💳 Sobre Pagos

**¿Qué métodos de pago aceptan?**
- Tarjeta de crédito/débito (Visa, Mastercard)
- PayPal
- Transferencia bancaria
- Pago contra reembolso (+€3)

**¿Es seguro pagar en su web?**
100% seguro. Usamos encriptación SSL y PCI DSS.

**¿Emiten facturas?**
Sí, incluida en el paquete y por email.

## 🚚 Sobre Envíos

**¿Cuánto tarda mi pedido?**
- Península: 24-48h
- Islas: 3-7 días

**¿Puedo rastrear mi pedido?**
Sí, recibirás número de seguimiento por email.

**¿Envían sin gastos?**
Sí, gratis en pedidos +€50 en Península.

## ↩️ Sobre Devoluciones

**¿Puedo devolver un producto?**
Sí, 30 días sin preguntas.

**¿Quién paga el envío de devolución?**
Tú pagas (excepto productos defectuosos).

## 🛠️ Sobre Productos

**¿Los productos tienen garantía?**
Sí, 2 años de garantía del fabricante.

**¿Son herramientas nuevas?**
Sí, 100% nuevas, nunca reacondicionadas.

**¿Tienen instrucciones en español?**
Sí, todos los productos incluyen manual en español.

## 📞 Atención al Cliente

**¿Cómo puedo contactarlos?**
- Email: info@herramientasyaccesorios.store
- Teléfono: [Tu teléfono]
- Chat: Lun-Vie 9:00-18:00

**¿Cuánto tardan en responder?**
Máximo 24h laborables (normalmente en horas).
```

---

## INSTRUCCIONES DE IMPLEMENTACIÓN EN WORDPRESS:

1. **Crear páginas:**
   - WordPress → Páginas → Añadir nueva
   - Copiar el contenido HTML/Markdown
   - Asignar slug correcto
   - Publicar

2. **Menú principal:**
   ```
   - Inicio
   - Tienda
   - Ofertas 🔥
   - Sobre Nosotros
   - Blog
   - Contacto
   ```

3. **Menú Footer:**
   ```
   Información:
   - Sobre Nosotros
   - Envíos
   - Devoluciones
   - FAQ
   
   Legal:
   - Política de Privacidad
   - Términos y Condiciones
   - Cookies
   ```

4. **Configurar SEO (Yoast/RankMath):**
   - Meta title: Máx 60 caracteres
   - Meta description: Máx 155 caracteres
   - Focus keyword en cada página
   - URL amigable

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN:

- [ ] Crear página Inicio con shortcodes
- [ ] Crear página Sobre Nosotros
- [ ] Crear página Envíos
- [ ] Crear página Devoluciones
- [ ] Crear página FAQ
- [ ] Configurar menús
- [ ] Instalar plugin SEO
- [ ] Optimizar meta tags
```
