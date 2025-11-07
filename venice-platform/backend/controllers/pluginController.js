/**
 * Plugin Controller - Las Herramientas de Cerebro
 * Interfaz para el plugin de WordPress
 * @author Roberzuzu
 */

const veniceController = require('./veniceController');
const wooCommerceService = require('../services/wooCommerce');

/**
 * Endpoint para recibir mensajes desde el plugin de WordPress
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.receiveMessage = async (req, res) => {
  try {
    const { message, userId, siteUrl, pluginVersion } = req.body;

    // Validar datos requeridos
    if (!message || !userId) {
      return res.status(400).json({
        success: false,
        error: 'Message and userId are required'
      });
    }

    console.log(`[Plugin] Received message from WordPress site: ${siteUrl}`);

    // Agregar contexto del plugin
    const context = {
      source: 'wordpress_plugin',
      siteUrl,
      pluginVersion,
      timestamp: new Date().toISOString()
    };

    // Procesar usando el controlador de Venice
    const processedReq = {
      ...req,
      body: {
        message,
        userId,
        context
      }
    };

    // Usar el método processChat del Venice controller
    await veniceController.processChat(processedReq, res);

  } catch (error) {
    console.error('[Plugin Controller Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error processing WordPress plugin message',
      message: error.message
    });
  }
};

/**
 * Obtener productos de WooCommerce
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.getProducts = async (req, res) => {
  try {
    const { siteUrl, category, limit = 20 } = req.query;

    if (!siteUrl) {
      return res.status(400).json({
        success: false,
        error: 'siteUrl is required'
      });
    }

    const products = await wooCommerceService.getProducts({
      siteUrl,
      category,
      limit: parseInt(limit)
    });

    res.json({
      success: true,
      products,
      count: products.length
    });

  } catch (error) {
    console.error('[Plugin Products Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error retrieving WooCommerce products',
      message: error.message
    });
  }
};

/**
 * Crear orden en WooCommerce
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.createOrder = async (req, res) => {
  try {
    const { siteUrl, orderData } = req.body;

    if (!siteUrl || !orderData) {
      return res.status(400).json({
        success: false,
        error: 'siteUrl and orderData are required'
      });
    }

    const order = await wooCommerceService.createOrder(siteUrl, orderData);

    res.json({
      success: true,
      order
    });

  } catch (error) {
    console.error('[Plugin Order Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error creating WooCommerce order',
      message: error.message
    });
  }
};

/**
 * Verificar conexión con el plugin de WordPress
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.verifyConnection = async (req, res) => {
  try {
    const { siteUrl, apiKey } = req.body;

    if (!siteUrl || !apiKey) {
      return res.status(400).json({
        success: false,
        error: 'siteUrl and apiKey are required'
      });
    }

    // Verificar que el API key sea válido
    const isValid = apiKey === process.env.PLUGIN_API_KEY;

    if (!isValid) {
      return res.status(401).json({
        success: false,
        error: 'Invalid API key'
      });
    }

    res.json({
      success: true,
      message: 'WordPress plugin connection verified',
      siteUrl,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[Plugin Verification Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error verifying WordPress plugin connection',
      message: error.message
    });
  }
};

/**
 * Sincronizar datos entre WordPress y Venice Platform
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
exports.syncData = async (req, res) => {
  try {
    const { siteUrl, dataType, data } = req.body;

    if (!siteUrl || !dataType || !data) {
      return res.status(400).json({
        success: false,
        error: 'siteUrl, dataType, and data are required'
      });
    }

    console.log(`[Plugin Sync] Syncing ${dataType} data from ${siteUrl}`);

    // Aquí se puede implementar lógica de sincronización
    // Por ahora, simplemente confirmamos la recepción
    
    res.json({
      success: true,
      message: `Successfully synced ${dataType} data`,
      dataType,
      itemCount: Array.isArray(data) ? data.length : 1,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[Plugin Sync Error]:', error);
    res.status(500).json({
      success: false,
      error: 'Error syncing WordPress data',
      message: error.message
    });
  }
};

module.exports = exports;
