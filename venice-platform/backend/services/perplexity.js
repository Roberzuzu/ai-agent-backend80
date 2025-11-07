/**
 * Perplexity Service - Las Herramientas de Cerebro
 * Cliente para Perplexity API - Búsquedas en internet
 * @author Roberzuzu
 */

const axios = require('axios');

const PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions';
const API_KEY = process.env.PERPLEXITY_API_KEY;
const DEFAULT_MODEL = process.env.PERPLEXITY_MODEL || 'llama-3.1-sonar-small-128k-online';

/**
 * Realizar búsqueda en internet usando Perplexity
 * @param {string} query - Consulta de búsqueda
 * @param {Object} options - Opciones adicionales
 * @returns {Promise<Object>} Resultados de la búsqueda
 */
exports.search = async (query, options = {}) => {
  try {
    if (!API_KEY) {
      throw new Error('PERPLEXITY_API_KEY no está configurado');
    }

    const messages = [
      {
        role: 'system',
        content: 'Eres un asistente útil que busca información actualizada en internet. Proporciona respuestas precisas y bien fundamentadas con fuentes cuando sea posible.'
      },
      {
        role: 'user',
        content: query
      }
    ];

    const requestData = {
      model: options.model || DEFAULT_MODEL,
      messages,
      temperature: options.temperature || 0.2,
      max_tokens: options.maxTokens || 1500,
      return_citations: true,
      return_images: options.includeImages || false
    };

    console.log('[Perplexity] Searching:', query.substring(0, 100));

    const response = await axios.post(PERPLEXITY_API_URL, requestData, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });

    if (response.data && response.data.choices && response.data.choices.length > 0) {
      const choice = response.data.choices[0];
      
      console.log('[Perplexity] Search completed successfully');
      
      return {
        text: choice.message.content,
        citations: response.data.citations || [],
        images: response.data.images || [],
        model: requestData.model,
        usage: response.data.usage,
        metadata: {
          tokensUsed: response.data.usage?.total_tokens || 0,
          timestamp: new Date().toISOString()
        }
      };
    }

    throw new Error('No response from Perplexity API');

  } catch (error) {
    console.error('[Perplexity Error]:', error.message);
    
    if (error.response) {
      console.error('API Response Error:', error.response.data);
      throw new Error(`Perplexity API Error: ${error.response.data.error?.message || 'Unknown error'}`);
    }
    
    throw error;
  }
};

/**
 * Verificar si una consulta requiere búsqueda en internet
 * @param {string} message - Mensaje del usuario
 * @returns {boolean} True si requiere búsqueda
 */
exports.requiresInternetSearch = (message) => {
  const searchKeywords = [
    'busca', 'buscar', 'encuentra', 'encontrar',
    'qué es', 'quién es', 'cuál es',
    'información sobre', 'datos sobre',
    'actualidad', 'noticias', 'últimas',
    'precio', 'costo', 'valor actual',
    'dónde', 'donde',
    'web', 'sitio', 'página'
  ];

  const lowerMessage = message.toLowerCase();
  return searchKeywords.some(keyword => lowerMessage.includes(keyword));
};

/**
 * Health check para Perplexity API
 * @returns {Promise<boolean>} Estado de conexión
 */
exports.healthCheck = async () => {
  try {
    if (!API_KEY) {
      return false;
    }

    const response = await axios.post(
      PERPLEXITY_API_URL,
      {
        model: DEFAULT_MODEL,
        messages: [{ role: 'user', content: 'test' }],
        max_tokens: 10
      },
      {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      }
    );

    return response.status === 200;

  } catch (error) {
    console.error('[Perplexity Health Check Failed]:', error.message);
    return false;
  }
};

module.exports = exports;
