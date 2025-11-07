/**
 * OpenRouter Service - Las Herramientas de Cerebro
 * Cliente para OpenRouter API - Hub principal de modelos AI
 * @author Roberzuzu
 */

const axios = require('axios');

const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';
const API_KEY = process.env.OPENROUTER_API_KEY;
const DEFAULT_MODEL = process.env.OPENROUTER_DEFAULT_MODEL || 'openai/gpt-4-turbo';

/**
 * Enviar mensaje al modelo de OpenRouter
 * @param {string} message - Mensaje del usuario
 * @param {Object} context - Contexto adicional de la conversación
 * @returns {Promise<string>} Respuesta del modelo
 */
exports.chat = async (message, context = {}) => {
  try {
    if (!API_KEY) {
      throw new Error('OPENROUTER_API_KEY no está configurado');
    }

    const messages = [];

    // Agregar contexto del sistema si existe
    if (context.systemPrompt) {
      messages.push({
        role: 'system',
        content: context.systemPrompt
      });
    }

    // Agregar historial de conversación si existe
    if (context.history && Array.isArray(context.history)) {
      messages.push(...context.history);
    }

    // Agregar mensaje actual del usuario
    messages.push({
      role: 'user',
      content: message
    });

    const requestData = {
      model: context.model || DEFAULT_MODEL,
      messages,
      temperature: context.temperature || 0.7,
      max_tokens: context.maxTokens || 2000
    };

    console.log(`[OpenRouter] Sending request to model: ${requestData.model}`);

    const response = await axios.post(OPENROUTER_API_URL, requestData, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': process.env.APP_URL || 'https://localhost:3000',
        'X-Title': 'Las Herramientas de Cerebro'
      },
      timeout: 30000
    });

    if (response.data && response.data.choices && response.data.choices.length > 0) {
      const aiResponse = response.data.choices[0].message.content;
      
      console.log('[OpenRouter] Response received successfully');
      
      return {
        text: aiResponse,
        model: requestData.model,
        usage: response.data.usage,
        metadata: {
          tokensUsed: response.data.usage?.total_tokens || 0,
          timestamp: new Date().toISOString()
        }
      };
    }

    throw new Error('No response from OpenRouter API');

  } catch (error) {
    console.error('[OpenRouter Error]:', error.message);
    
    if (error.response) {
      console.error('API Response Error:', error.response.data);
      throw new Error(`OpenRouter API Error: ${error.response.data.error?.message || 'Unknown error'}`);
    }
    
    throw error;
  }
};

/**
 * Listar modelos disponibles en OpenRouter
 * @returns {Promise<Array>} Lista de modelos
 */
exports.listModels = async () => {
  try {
    if (!API_KEY) {
      throw new Error('OPENROUTER_API_KEY no está configurado');
    }

    const response = await axios.get('https://openrouter.ai/api/v1/models', {
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      }
    });

    return response.data.data || [];

  } catch (error) {
    console.error('[OpenRouter Models Error]:', error.message);
    throw error;
  }
};

/**
 * Verificar conexión con OpenRouter
 * @returns {Promise<boolean>} Estado de la conexión
 */
exports.healthCheck = async () => {
  try {
    if (!API_KEY) {
      return false;
    }

    await axios.get('https://openrouter.ai/api/v1/models', {
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      },
      timeout: 5000
    });

    return true;

  } catch (error) {
    console.error('[OpenRouter Health Check Failed]:', error.message);
    return false;
  }
};

module.exports = exports;
