/**
 * WooCommerce Service - Las Herramientas de Cerebro
 * @author Roberzuzu
 */

const axios = require('axios');

exports.getProducts = async ({ siteUrl, category, limit = 20 }) => {
  try {
    const apiUrl = `${siteUrl}/wp-json/wc/v3/products`;
    const response = await axios.get(apiUrl, {
      params: { category, per_page: limit },
      auth: {
        username: process.env.WC_CONSUMER_KEY,
        password: process.env.WC_CONSUMER_SECRET
      }
    });
    return response.data;
  } catch (error) {
    console.error('[WooCommerce Error]:', error.message);
    throw error;
  }
};

exports.createOrder = async (siteUrl, orderData) => {
  try {
    const apiUrl = `${siteUrl}/wp-json/wc/v3/orders`;
    const response = await axios.post(apiUrl, orderData, {
      auth: {
        username: process.env.WC_CONSUMER_KEY,
        password: process.env.WC_CONSUMER_SECRET
      }
    });
    return response.data;
  } catch (error) {
    console.error('[WooCommerce Order Error]:', error.message);
    throw error;
  }
};

module.exports = exports;
