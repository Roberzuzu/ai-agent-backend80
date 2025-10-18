import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { CheckCircle, Loader2, XCircle, AlertCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const PaymentSuccessPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('checking'); // checking, success, failed, error
  const [paymentDetails, setPaymentDetails] = useState(null);
  const [attempts, setAttempts] = useState(0);
  const maxAttempts = 10;

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    
    if (!sessionId) {
      setStatus('error');
      return;
    }

    checkPaymentStatus(sessionId);
  }, [searchParams]);

  const checkPaymentStatus = async (sessionId, attemptCount = 0) => {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/payments/checkout/status/${sessionId}`
      );

      setPaymentDetails(response.data);
      setAttempts(attemptCount + 1);

      if (response.data.payment_status === 'paid') {
        setStatus('success');
      } else if (response.data.status === 'expired') {
        setStatus('failed');
      } else if (attemptCount < maxAttempts) {
        // Continue polling
        setTimeout(() => {
          checkPaymentStatus(sessionId, attemptCount + 1);
        }, 2000); // Poll every 2 seconds
      } else {
        // Max attempts reached
        setStatus('error');
      }
    } catch (error) {
      console.error('Error checking payment status:', error);
      
      if (attemptCount < maxAttempts) {
        setTimeout(() => {
          checkPaymentStatus(sessionId, attemptCount + 1);
        }, 2000);
      } else {
        setStatus('error');
      }
    }
  };

  const renderContent = () => {
    switch (status) {
      case 'checking':
        return (
          <div className="text-center">
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Verificando tu pago...
            </h2>
            <p className="text-gray-600">
              Por favor espera mientras confirmamos tu transacción
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Intento {attempts} de {maxAttempts}
            </p>
          </div>
        );

      case 'success':
        return (
          <div className="text-center">
            <div className="bg-green-100 rounded-full p-4 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
              <CheckCircle className="w-12 h-12 text-green-600" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              ¡Pago Exitoso!
            </h2>
            <p className="text-gray-600 mb-6">
              Tu pago ha sido procesado correctamente
            </p>

            {paymentDetails && (
              <div className="bg-gray-50 rounded-lg p-6 mb-6 text-left max-w-md mx-auto">
                <h3 className="font-semibold text-gray-900 mb-4">Detalles del Pago</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Monto:</span>
                    <span className="font-semibold">
                      ${(paymentDetails.amount_total / 100).toFixed(2)} {paymentDetails.currency.toUpperCase()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Estado:</span>
                    <span className="font-semibold text-green-600">Pagado</span>
                  </div>
                  {paymentDetails.metadata?.payment_type && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Tipo:</span>
                      <span className="font-semibold capitalize">
                        {paymentDetails.metadata.payment_type === 'subscription' ? 'Suscripción' : 'Producto'}
                      </span>
                    </div>
                  )}
                  {paymentDetails.metadata?.product_name && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Producto:</span>
                      <span className="font-semibold">
                        {paymentDetails.metadata.product_name}
                      </span>
                    </div>
                  )}
                  {paymentDetails.metadata?.plan_name && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Plan:</span>
                      <span className="font-semibold">
                        {paymentDetails.metadata.plan_name}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="space-x-4">
              <button
                onClick={() => navigate('/products')}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Ver Productos
              </button>
              <button
                onClick={() => navigate('/subscriptions')}
                className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Mis Suscripciones
              </button>
            </div>
          </div>
        );

      case 'failed':
        return (
          <div className="text-center">
            <div className="bg-red-100 rounded-full p-4 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
              <XCircle className="w-12 h-12 text-red-600" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Pago Fallido
            </h2>
            <p className="text-gray-600 mb-6">
              Tu pago no pudo ser procesado o fue cancelado
            </p>

            <div className="space-x-4">
              <button
                onClick={() => navigate('/subscriptions')}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Intentar de Nuevo
              </button>
              <button
                onClick={() => navigate('/')}
                className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Volver al Inicio
              </button>
            </div>
          </div>
        );

      case 'error':
        return (
          <div className="text-center">
            <div className="bg-yellow-100 rounded-full p-4 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
              <AlertCircle className="w-12 h-12 text-yellow-600" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Error al Verificar
            </h2>
            <p className="text-gray-600 mb-6">
              No pudimos verificar el estado de tu pago. Por favor revisa tu email para la confirmación.
            </p>

            <div className="space-x-4">
              <button
                onClick={() => navigate('/subscriptions')}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Ver Suscripciones
              </button>
              <button
                onClick={() => navigate('/')}
                className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Volver al Inicio
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
        {renderContent()}
      </div>
    </div>
  );
};

export default PaymentSuccessPage;
