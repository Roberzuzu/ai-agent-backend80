/**
 * Venice Controller - Las Herramientas de Cerebro
 * Controlador principal del orquestador de IA
 * @author Roberzuzu
 */

const agentSelector = require('../utils/agentSelector');
const openRouterService = require('../services/openrouter');
const perplexityService = require('../services/perplexity');
const n8nService = require('../services/n8n');
const mongoDBService = require('../services/mongoDB');

/**
 * Procesar mensaje de chat y enrutar al agente apropiado
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.processChat = async (req, res) => {
  try {
    const { message, userId, sessionId, context } = req.body;

    // Validar datos requeridos
    if (!message) {
      return res.status(400).json({
        success: false,
        error: 'Message is required'
      });
    }

    // Seleccionar agente apropiado
    const selectedAgent = agentSelector.selectAgent(message, context);
    
    console.log(`[Venice] Processing message with agent: ${selectedAgent}`);

    let response;

    // Enrutar al servicio correspondiente
    switch (selectedAgent) {
      case 'perplexity':
        response = await perplexityService.search(message);
        break;
      
      case 'openrouter':
      default:
        response = await openRouterService.chat(message, context);
        break;
    }

    // Guardar en MongoDB si está habilitado
    if (process.env.MONGODB_ENABLED === 'true') {
      await mongoDBService.saveConversation({
        userId,
        sessionId,
        message,
        response,
        agent: selectedAgent,
        timestamp: new Date()
      });
    }

    // Enviar respuesta
    res.json({
      success: true,
      agent: selectedAgent,
      response,
      sessionId: sessionId || Date.now().toString()
    });

  } catch (error) {
    console.error('[Venice Controller Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error processing chat',
      message: error.message
    });
  }
};

/**
 * Obtener historial de conversaciones
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.getHistory = async (req, res) => {
  try {
    const { userId, sessionId, limit = 50 } = req.query;

    if (!userId && !sessionId) {
      return res.status(400).json({
        success: false,
        error: 'userId or sessionId is required'
      });
    }

    const history = await mongoDBService.getConversationHistory({
      userId,
      sessionId,
      limit: parseInt(limit)
    });

    res.json({
      success: true,
      history,
      count: history.length
    });

  } catch (error) {
    console.error('[Venice History Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error retrieving conversation history',
      message: error.message
    });
  }
};

/**
 * Ejecutar workflow de n8n
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.executeWorkflow = async (req, res) => {
  try {
    const { workflowId, data } = req.body;

    if (!workflowId) {
      return res.status(400).json({
        success: false,
        error: 'workflowId is required'
      });
    }

    const result = await n8nService.triggerWorkflow(workflowId, data);

    res.json({
      success: true,
      workflowId,
      result
    });

  } catch (error) {
    console.error('[Venice Workflow Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error executing n8n workflow',
      message: error.message
    });
  }
};

/**
 * Obtener estado del sistema
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.getStatus = async (req, res) => {
  try {
    const status = {
      service: 'Las Herramientas de Cerebro',
      version: '2.0.0',
      timestamp: new Date().toISOString(),
      agents: {
        openrouter: process.env.OPENROUTER_API_KEY ? 'enabled' : 'disabled',
        perplexity: process.env.PERPLEXITY_API_KEY ? 'enabled' : 'disabled',
        n8n: process.env.N8N_WEBHOOK_URL ? 'enabled' : 'disabled'
      },
      database: {
        mongodb: process.env.MONGODB_ENABLED === 'true' ? 'enabled' : 'disabled'
      }
    };

    res.json({
      success: true,
      status
    });

  } catch (error) {
    console.error('[Venice Status Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error retrieving system status'
    });
  }
};

module.exports = exports;
