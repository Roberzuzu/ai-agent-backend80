/**
 * Auth Middleware - Las Herramientas de Cerebro
 * @author Roberzuzu
 */

module.exports = (req, res, next) => {
  try {
    const apiKey = req.headers['x-api-key'] || req.query.apiKey;
    
    if (!apiKey) {
      return res.status(401).json({
        success: false,
        error: 'API key requerida'
      });
    }

    if (apiKey !== process.env.API_KEY) {
      return res.status(403).json({
        success: false,
        error: 'API key inválida'
      });
    }

    next();
  } catch (error) {
    console.error('[Auth Error]:', error);
    res.status(500).json({ success: false, error: 'Error de autenticación' });
  }
};
