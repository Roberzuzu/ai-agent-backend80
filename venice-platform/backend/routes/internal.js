/**
 * Rutas Internas - Las Herramientas de Cerebro
 * Endpoints para monitoreo y health checks
 * @author Roberzuzu
 */

const express = require('express');
const router = express.Router();

/**
 * GET /internal/health
 * Health check endpoint - usado por Render y otros servicios
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    service: 'Las Herramientas de Cerebro',
    version: '2.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

/**
 * GET /internal/metrics
 * Métricas básicas del servidor
 */
router.get('/metrics', (req, res) => {
  const used = process.memoryUsage();
  
  res.json({
    memory: {
      rss: `${Math.round(used.rss / 1024 / 1024)} MB`,
      heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)} MB`,
      heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)} MB`
    },
    uptime: `${Math.round(process.uptime())} seconds`,
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
