/**
 * Rutas API Públicas - Las Herramientas de Cerebro
 * Define los endpoints accesibles desde el exterior
 * @author Roberzuzu
 */

const express = require('express');
const { handleChatRequest } = require('../controllers/veniceController');
const router = express.Router();

/**
 * POST /api/chat
 * Endpoint principal para interactuar con Venice
 * 
 * Body:
 *   - message: string (obligatorio)
 *   - userId: string (obligatorio)
 *   - context: object (opcional)
 * 
 * Response:
 *   - agent: string (agente que procesó la petición)
 *   - response: any (respuesta del agente)
 *   - timestamp: string
 */
router.post('/chat', handleChatRequest);

/**
 * GET /api/status
 * Obtener estado de los servicios disponibles
 */
router.get('/status', async (req, res) => {
  try {
    const services = require('../config/services');
    
    const status = {
      platform: 'Las Herramientas de Cerebro',
      version: '2.0.0',
      services: {
        openrouter: !!services.openrouter.apiKey,
        perplexity: !!services.perplexity,
        n8n: !!services.n8n,
        woocommerce: !!services.woo,
        mongodb: !!services.mongo
      },
      timestamp: new Date().toISOString()
    };
    
    res.json(status);
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener estado de servicios' });
  }
});

/**
 * POST /api/webhook/:service
 * Endpoint genérico para recibir webhooks de servicios externos
 * 
 * Params:
 *   - service: n8n | telegram | woocommerce
 */
router.post('/webhook/:service', async (req, res) => {
  try {
    const { service } = req.params;
    const payload = req.body;
    
    console.log(`Webhook recibido de ${service}:`, payload);
    
    // TODO: Procesar webhook según el servicio
    // Por ahora solo lo registramos
    
    res.json({ 
      received: true, 
      service, 
      timestamp: new Date().toISOString() 
    });
  } catch (error) {
    console.error('Error procesando webhook:', error);
    res.status(500).json({ error: 'Error procesando webhook' });
  }
});

module.exports = router;
