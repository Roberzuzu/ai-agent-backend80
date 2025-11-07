/**
 * MongoDB Service - Las Herramientas de Cerebro
 * @author Roberzuzu
 */

const { MongoClient } = require('mongodb');

let client;
let db;

exports.connect = async () => {
  try {
    if (process.env.MONGODB_ENABLED !== 'true') {
      console.log('[MongoDB] Deshabilitado');
      return null;
    }

    const uri = process.env.MONGODB_URI;
    if (!uri) throw new Error('MONGODB_URI no configurado');

    client = new MongoClient(uri);
    await client.connect();
    db = client.db(process.env.MONGODB_DB_NAME || 'venice');
    
    console.log('[MongoDB] Conectado exitosamente');
    return db;
  } catch (error) {
    console.error('[MongoDB Connection Error]:', error.message);
    throw error;
  }
};

exports.saveConversation = async (data) => {
  try {
    if (!db) await exports.connect();
    if (!db) return null;

    const collection = db.collection('conversations');
    const result = await collection.insertOne(data);
    return result.insertedId;
  } catch (error) {
    console.error('[MongoDB Save Error]:', error.message);
    return null;
  }
};

exports.getConversationHistory = async ({ userId, sessionId, limit = 50 }) => {
  try {
    if (!db) await exports.connect();
    if (!db) return [];

    const collection = db.collection('conversations');
    const query = {};
    if (userId) query.userId = userId;
    if (sessionId) query.sessionId = sessionId;

    const history = await collection
      .find(query)
      .sort({ timestamp: -1 })
      .limit(limit)
      .toArray();
    
    return history;
  } catch (error) {
    console.error('[MongoDB History Error]:', error.message);
    return [];
  }
};

exports.disconnect = async () => {
  if (client) {
    await client.close();
    console.log('[MongoDB] Desconectado');
  }
};

module.exports = exports;
