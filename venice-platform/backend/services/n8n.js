/**
 * n8n Service - Las Herramientas de Cerebro
 * Cliente para n8n automation webhooks
 * @author Roberzuzu
 */

const axios = require('axios');

const N8N_WEBHOOK_URL = process.env.N8N_WEBHOOK_URL;

/**
 * Ejecutar workflow de n8n mediante webhook
 * @param {string} workflowId - ID del workflow
 * @param {Object} data - Datos a enviar
 * @returns {Promise<Object>} Resultado del workflow
 */
exports.triggerWorkflow = async (workflowId, data = {}) => {
  try {
    if (!N8N_WEBHOOK_URL) {
      throw new Error('N8N_WEBHOOK_URL no configurado');
    }

    const webhookUrl = `${N8N_WEBHOOK_URL}/${workflowId}`;
    
    console.log(`[n8n] Triggering workflow: ${workflowId}`);

    const response = await axios.post(webhookUrl, data, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });

    return response.data;

  } catch (error) {
    console.error('[n8n Error]:', error.message);
    throw error;
  }
};

module.exports = exports;
