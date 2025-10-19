# PÁGINA DE CONTACTO OPTIMIZADA

**Slug:** /contacto  
**Título SEO:** Contacto - Atención al Cliente 24/7 | HerramientasyAccesorios.store  
**Meta Description:** Contacta con nosotros. Atención al cliente por email, teléfono y chat. Respuesta en menos de 24h. Estamos aquí para ayudarte.

**Contenido HTML:**

```html
<div class="contact-page" style="max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
    
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="font-size: 42px; margin-bottom: 20px;">📞 Contacta con Nosotros</h1>
        <p style="font-size: 20px; color: #666;">Estamos aquí para ayudarte. Respuesta garantizada en menos de 24h</p>
    </div>

    <!-- Contact Methods Grid -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-bottom: 50px;">
        
        <!-- Email -->
        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">📧</div>
            <h3>Email</h3>
            <p style="color: #666; margin: 15px 0;">La forma más rápida de contactarnos</p>
            <a href="mailto:info@herramientasyaccesorios.store" style="color: #667eea; font-weight: bold; text-decoration: none;">
                info@herramientasyaccesorios.store
            </a>
            <p style="font-size: 14px; color: #999; margin-top: 10px;">Respuesta en 24h</p>
        </div>

        <!-- Phone -->
        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">📱</div>
            <h3>Teléfono</h3>
            <p style="color: #666; margin: 15px 0;">Llámanos de Lunes a Viernes</p>
            <a href="tel:+34XXXXXXXXX" style="color: #667eea; font-weight: bold; text-decoration: none; font-size: 20px;">
                +34 XXX XXX XXX
            </a>
            <p style="font-size: 14px; color: #999; margin-top: 10px;">Lun-Vie: 9:00-18:00</p>
        </div>

        <!-- WhatsApp -->
        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">💬</div>
            <h3>WhatsApp</h3>
            <p style="color: #666; margin: 15px 0;">Escríbenos directamente</p>
            <a href="https://wa.me/34XXXXXXXXX" target="_blank" style="display: inline-block; background: #25D366; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px;">
                Abrir WhatsApp
            </a>
            <p style="font-size: 14px; color: #999; margin-top: 10px;">Respuesta rápida</p>
        </div>

    </div>

    <!-- Contact Form Section -->
    <div style="background: #f8f9fa; padding: 50px 30px; border-radius: 12px; margin-bottom: 50px;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 30px;">✉️ Envíanos un Mensaje</h2>
            
            <!-- Usar plugin Contact Form 7 o WPForms -->
            [contact-form-7 id="1234"]
            
            <!-- O formulario HTML simple -->
            <form method="post" action="/enviar-contacto">
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Nombre *</label>
                    <input type="text" name="name" required style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px;">
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Email *</label>
                    <input type="email" name="email" required style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px;">
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Asunto *</label>
                    <select name="subject" required style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px;">
                        <option value="">Selecciona un asunto</option>
                        <option value="pedido">Consulta sobre pedido</option>
                        <option value="producto">Información de producto</option>
                        <option value="devolucion">Devolución</option>
                        <option value="tecnico">Soporte técnico</option>
                        <option value="otro">Otro</option>
                    </select>
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Número de Pedido (opcional)</label>
                    <input type="text" name="order" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px;">
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Mensaje *</label>
                    <textarea name="message" required rows="6" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; resize: vertical;"></textarea>
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" name="privacy" required>
                        <span style="font-size: 14px;">He leído y acepto la <a href="/politica-privacidad" style="color: #667eea;">Política de Privacidad</a></span>
                    </label>
                </div>

                <button type="submit" style="width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer;">
                    Enviar Mensaje
                </button>
            </form>
        </div>
    </div>

    <!-- FAQ Section -->
    <div style="margin-bottom: 50px;">
        <h2 style="text-align: center; margin-bottom: 40px;">❓ Preguntas Frecuentes</h2>
        
        <div style="max-width: 800px; margin: 0 auto;">
            
            <div style="background: white; padding: 25px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 10px 0;">¿Cuánto tardáis en responder?</h4>
                <p style="margin: 0; color: #666;">Respondemos en menos de 24h laborables. Emails recibidos en fin de semana se responden el lunes.</p>
            </div>

            <div style="background: white; padding: 25px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 10px 0;">¿Puedo consultar el estado de mi pedido?</h4>
                <p style="margin: 0; color: #666;">Sí, escríbenos con tu número de pedido y te informamos inmediatamente. También puedes rastrear tu pedido con el código de seguimiento.</p>
            </div>

            <div style="background: white; padding: 25px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 10px 0;">¿Atendéis consultas técnicas?</h4>
                <p style="margin: 0; color: #666;">Por supuesto. Nuestro equipo de expertos está disponible para resolver dudas sobre productos, uso y mantenimiento.</p>
            </div>

            <div style="background: white; padding: 25px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 10px 0;">¿Tenéis tienda física?</h4>
                <p style="margin: 0; color: #666;">Somos 100% online. Esto nos permite ofrecer mejores precios al tener menos gastos estructurales.</p>
            </div>

        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/faq" style="color: #667eea; font-weight: bold; font-size: 18px;">Ver todas las preguntas frecuentes →</a>
        </div>
    </div>

    <!-- Business Hours -->
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px 30px; border-radius: 12px; text-align: center;">
        <h2 style="margin-bottom: 30px;">🕐 Horario de Atención</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 800px; margin: 0 auto;">
            <div>
                <h4 style="margin: 0 0 10px 0;">Lunes - Viernes</h4>
                <p style="margin: 0; font-size: 18px;">9:00 - 18:00</p>
            </div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Sábados</h4>
                <p style="margin: 0; font-size: 18px;">Cerrado</p>
            </div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Domingos</h4>
                <p style="margin: 0; font-size: 18px;">Cerrado</p>
            </div>
        </div>
        <p style="margin-top: 30px; font-size: 16px; opacity: 0.9;">
            Emails recibidos fuera de horario se responden el siguiente día laborable
        </p>
    </div>

    <!-- Social Media -->
    <div style="text-align: center; margin-top: 50px;">
        <h3 style="margin-bottom: 25px;">Síguenos en Redes Sociales</h3>
        <div style="display: flex; justify-content: center; gap: 20px;">
            <a href="https://facebook.com/[TU-PAGINA]" target="_blank" style="display: inline-block; width: 50px; height: 50px; background: #1877F2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; text-decoration: none;">
                f
            </a>
            <a href="https://instagram.com/[TU-CUENTA]" target="_blank" style="display: inline-block; width: 50px; height: 50px; background: #E4405F; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; text-decoration: none;">
                📷
            </a>
            <a href="https://youtube.com/[TU-CANAL]" target="_blank" style="display: inline-block; width: 50px; height: 50px; background: #FF0000; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; text-decoration: none;">
                ▶
            </a>
        </div>
    </div>

</div>
```

---

# PÁGINA "GARANTÍAS Y DEVOLUCIONES" EXTENDIDA

**Slug:** /garantias  
**Título SEO:** Garantías - 2 Años + 30 Días Devolución | HerramientasyAccesorios.store

**Contenido:**

```html
<div style="max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
    
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="font-size: 42px; margin-bottom: 20px;">🛡️ Garantías y Devoluciones</h1>
        <p style="font-size: 20px; color: #666;">Compra con total tranquilidad. Estamos contigo</p>
    </div>

    <!-- Garantías Grid -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-bottom: 50px;">
        
        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
            <h3>Garantía 2 Años</h3>
            <p style="color: #666;">Todos los productos con garantía legal de 2 años contra defectos de conformidad</p>
        </div>

        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">↩️</div>
            <h3>30 Días Devolución</h3>
            <p style="color: #666;">Si no estás satisfecho, devuélvelo en 30 días sin preguntas</p>
        </div>

        <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">🔄</div>
            <h3>Cambio Gratis</h3>
            <p style="color: #666;">Cambia por otro modelo si lo prefieres. Nosotros gestionamos todo</p>
        </div>

    </div>

    <!-- Detailed Sections -->
    <div style="background: #f8f9fa; padding: 40px 30px; border-radius: 12px; margin-bottom: 40px;">
        <h2>🛡️ Garantía Legal de 2 Años</h2>
        
        <h3>¿Qué cubre?</h3>
        <ul style="font-size: 16px; line-height: 1.8;">
            <li>✅ Defectos de fabricación</li>
            <li>✅ Fallos de conformidad con lo anunciado</li>
            <li>✅ Productos que no funcionan correctamente</li>
            <li>✅ Vicios ocultos descubiertos tras la compra</li>
        </ul>

        <h3 style="margin-top: 30px;">¿Cómo reclamar?</h3>
        <ol style="font-size: 16px; line-height: 1.8;">
            <li>Contacta con nosotros: garantias@herramientasyaccesorios.store</li>
            <li>Indica número de pedido y describe el problema</li>
            <li>Envía fotos o video del defecto</li>
            <li>Te enviamos etiqueta de devolución gratuita</li>
            <li>Recibimos el producto y lo verificamos (1-2 días)</li>
            <li>Reparación, sustitución o reembolso según caso</li>
        </ol>

        <div style="background: #fff3cd; padding: 20px; border-left: 4px solid #ffc107; margin-top: 20px; border-radius: 8px;">
            <strong>💡 Importante:</strong> La garantía legal es gratuita y cubre gastos de envío en ambos sentidos para productos defectuosos.
        </div>
    </div>

    <!-- Devoluciones -->
    <div style="background: white; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 40px;">
        <h2>↩️ Derecho de Desistimiento (30 días)</h2>
        
        <h3>Condiciones</h3>
        <ul style="font-size: 16px; line-height: 1.8;">
            <li>✅ Producto sin usar</li>
            <li>✅ Embalaje original intacto</li>
            <li>✅ Todos los accesorios incluidos</li>
            <li>✅ Factura de compra</li>
            <li>✅ Dentro de 30 días desde recepción</li>
        </ul>

        <h3 style="margin-top: 30px;">Proceso Paso a Paso</h3>
        
        <div style="display: flex; align-items: start; gap: 20px; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 32px; min-width: 50px; height: 50px; background: #667eea; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Solicitar Devolución</h4>
                <p style="margin: 0; color: #666;">Email a devoluciones@herramientasyaccesorios.store con número de pedido</p>
            </div>
        </div>

        <div style="display: flex; align-items: start; gap: 20px; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 32px; min-width: 50px; height: 50px; background: #667eea; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Recibir Etiqueta</h4>
                <p style="margin: 0; color: #666;">Te enviamos etiqueta de devolución por email (24h)</p>
            </div>
        </div>

        <div style="display: flex; align-items: start; gap: 20px; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 32px; min-width: 50px; height: 50px; background: #667eea; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">3</div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Enviar Producto</h4>
                <p style="margin: 0; color: #666;">Empaqueta bien y lleva a oficina de correos con etiqueta</p>
            </div>
        </div>

        <div style="display: flex; align-items: start; gap: 20px; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 32px; min-width: 50px; height: 50px; background: #667eea; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">4</div>
            <div>
                <h4 style="margin: 0 0 10px 0;">Reembolso</h4>
                <p style="margin: 0; color: #666;">Dinero en tu cuenta en 5-7 días tras recepción</p>
            </div>
        </div>

        <div style="background: #d1ecf1; padding: 20px; border-left: 4px solid #17a2b8; margin-top: 30px; border-radius: 8px;">
            <strong>📦 Gastos de envío:</strong> Los gastos de devolución son a tu cargo (excepto en productos defectuosos o error nuestro, que asumimos nosotros).
        </div>
    </div>

    <!-- CTA Final -->
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px 30px; border-radius: 12px; text-align: center;">
        <h2 style="margin-bottom: 20px;">¿Tienes dudas sobre garantías?</h2>
        <p style="font-size: 18px; margin-bottom: 30px;">Estamos aquí para ayudarte</p>
        <a href="/contacto" style="display: inline-block; background: white; color: #667eea; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 18px;">
            Contactar Soporte →
        </a>
    </div>

</div>
```

---

## INSTRUCCIONES IMPLEMENTACIÓN:

1. **WordPress → Páginas → Añadir nueva**
2. Copiar contenido HTML
3. Cambiar a modo "Texto" o "HTML" (no Visual)
4. Pegar código
5. Publicar
6. Añadir al menú correspondiente

**Nota:** Reemplazar `[TU-PAGINA]`, `[TU-CUENTA]`, teléfonos, etc. con tu información real.
```
