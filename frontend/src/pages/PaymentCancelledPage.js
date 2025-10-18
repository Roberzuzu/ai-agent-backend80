import React from 'react';
import { useNavigate } from 'react-router-dom';
import { XCircle } from 'lucide-react';

const PaymentCancelledPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-100 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full text-center">
        <div className="bg-orange-100 rounded-full p-4 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
          <XCircle className="w-12 h-12 text-orange-600" />
        </div>
        
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Pago Cancelado
        </h2>
        
        <p className="text-gray-600 mb-6">
          Has cancelado el proceso de pago. No se realizó ningún cargo.
        </p>

        <div className="space-x-4">
          <button
            onClick={() => navigate('/subscriptions')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Volver a Planes
          </button>
          <button
            onClick={() => navigate('/')}
            className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Ir al Inicio
          </button>
        </div>
      </div>
    </div>
  );
};

export default PaymentCancelledPage;
