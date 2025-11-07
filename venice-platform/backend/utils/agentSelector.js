/**
 * Agent Selector - Las Herramientas de Cerebro
 * @author Roberzuzu
 */

const perplexityService = require('../services/perplexity');

exports.selectAgent = (message, context = {}) => {
  // Si el contexto especifica un agente, usarlo
  if (context.agent) {
    return context.agent;
  }

  // Detectar si requiere búsqueda en internet
  if (perplexityService.requiresInternetSearch(message)) {
    return 'perplexity';
  }

  // Por defecto, usar OpenRouter
  return 'openrouter';
};

module.exports = exports;
