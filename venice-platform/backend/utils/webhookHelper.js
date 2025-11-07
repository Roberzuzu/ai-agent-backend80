/**
 * Webhook Helper - Las Herramientas de Cerebro
 * @author Roberzuzu
 */

exports.validateWebhook = (req, signature) => {
  // Implementar validación de webhook si es necesario
  return true;
};

exports.parseWebhookData = (req) => {
  return {
    source: req.headers['x-webhook-source'] || 'unknown',
    data: req.body,
    timestamp: new Date().toISOString()
  };
};

module.exports = exports;
