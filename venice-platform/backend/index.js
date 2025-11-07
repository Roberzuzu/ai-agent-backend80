/**
 * Venice Platform - Orquestador Central
 * Entry point del backend que coordina AI, herramientas y servicios
 * @author Roberzuzu
 * @version 2.0.0
 */

const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const apiRoutes = require('./routes/api');
const internalRoutes = require('./routes/internal');
const logging = require('./middlewares/logging');
const auth = require('./middlewares/auth');

// Cargar variables de entorno
dotenv.config();

const app = express();
const PORT = process.env.PORT || 8080;

// Middlewares globales
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(logging);

// Rutas públicas (chat, herramientas)
app.use('/api', auth, apiRoutes);

// Rutas internas (monitorización, health checks)
app.use('/internal', internalRoutes);

// Manejador de errores global
app.use((err, req, res, next) => {
  console.error('Error:', err.stack);
  res.status(500).json({
    error: 'Error interno del servidor',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`\n🚀 Venice Platform Orchestrator iniciado`);
  console.log(`📡 Puerto: ${PORT}`);
  console.log(`🌍 Entorno: ${process.env.NODE_ENV || 'development'}`);
  console.log(`✅ Listo para recibir peticiones\n`);
});

module.exports = app;
