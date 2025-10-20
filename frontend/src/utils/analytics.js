// Google Analytics Hook
// Tracking de eventos y conversiones

// Función para enviar eventos a Google Analytics
export const trackEvent = (eventName, eventParams = {}) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, eventParams);
  }
};

// Función para tracking de páginas
export const trackPageView = (pagePath, pageTitle) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', 'G-EMQDLMQ0S3', {
      page_path: pagePath,
      page_title: pageTitle
    });
  }
};

// Eventos predefinidos comunes
export const analytics = {
  // E-commerce
  viewProduct: (productId, productName, price) => {
    trackEvent('view_item', {
      currency: 'EUR',
      value: price,
      items: [{
        item_id: productId,
        item_name: productName,
        price: price
      }]
    });
  },

  addToCart: (productId, productName, price, quantity = 1) => {
    trackEvent('add_to_cart', {
      currency: 'EUR',
      value: price * quantity,
      items: [{
        item_id: productId,
        item_name: productName,
        price: price,
        quantity: quantity
      }]
    });
  },

  purchase: (transactionId, value, items) => {
    trackEvent('purchase', {
      transaction_id: transactionId,
      value: value,
      currency: 'EUR',
      items: items
    });
  },

  // Engagement
  search: (searchTerm) => {
    trackEvent('search', {
      search_term: searchTerm
    });
  },

  share: (contentType, itemId) => {
    trackEvent('share', {
      content_type: contentType,
      item_id: itemId
    });
  },

  // Bot de Telegram
  botCommand: (command, userId) => {
    trackEvent('telegram_command', {
      command: command,
      user_id: userId,
      event_category: 'Telegram Bot',
      event_label: command
    });
  },

  botError: (errorMessage) => {
    trackEvent('telegram_error', {
      error_message: errorMessage,
      event_category: 'Telegram Bot',
      event_label: 'Error'
    });
  },

  // AI Agent
  aiQuery: (query, toolsUsed) => {
    trackEvent('ai_query', {
      query: query,
      tools_used: toolsUsed,
      event_category: 'AI Agent',
      event_label: 'Query Processed'
    });
  },

  // Conversiones
  signUp: (method) => {
    trackEvent('sign_up', {
      method: method
    });
  },

  login: (method) => {
    trackEvent('login', {
      method: method
    });
  },

  // Custom events
  customEvent: (eventName, params) => {
    trackEvent(eventName, params);
  }
};

// Hook de React para tracking automático de páginas
export const usePageTracking = () => {
  if (typeof window !== 'undefined') {
    const path = window.location.pathname;
    const title = document.title;
    trackPageView(path, title);
  }
};

export default analytics;
