import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to console in development
    console.error('Error caught by boundary:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // Here you could send to error tracking service like Sentry
    // logErrorToService(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.href = '/';
  };

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center">
              {/* Icon */}
              <div className="inline-flex items-center justify-center w-20 h-20 bg-red-100 rounded-full mb-6">
                <AlertTriangle className="w-10 h-10 text-red-600" />
              </div>

              {/* Title */}
              <h1 className="text-3xl font-bold text-gray-900 mb-3">
                ¡Oops! Algo salió mal
              </h1>

              {/* Description */}
              <p className="text-gray-600 text-lg mb-8">
                Lo sentimos, hemos encontrado un error inesperado. No te preocupes, 
                nuestro equipo ha sido notificado y estamos trabajando en solucionarlo.
              </p>

              {/* Error Details (only in development) */}
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <div className="bg-gray-50 rounded-lg p-4 mb-6 text-left">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Detalles técnicos:</p>
                  <pre className="text-xs text-red-600 overflow-auto max-h-40">
                    {this.state.error.toString()}
                    {this.state.errorInfo && this.state.errorInfo.componentStack}
                  </pre>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={this.handleReload}
                  className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors duration-200"
                >
                  <RefreshCw className="w-5 h-5 mr-2" />
                  Recargar página
                </button>
                
                <button
                  onClick={this.handleReset}
                  className="inline-flex items-center justify-center px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors duration-200"
                >
                  <Home className="w-5 h-5 mr-2" />
                  Ir al inicio
                </button>
              </div>

              {/* Support Link */}
              <p className="text-sm text-gray-500 mt-8">
                ¿Necesitas ayuda? {' '}
                <a href="mailto:support@example.com" className="text-blue-600 hover:text-blue-700 font-medium">
                  Contacta a soporte
                </a>
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
