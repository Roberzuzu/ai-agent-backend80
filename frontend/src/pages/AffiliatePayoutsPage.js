import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { DollarSign, CreditCard, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const AffiliatePayoutsPage = () => {
  const navigate = useNavigate();
  const [affiliateEmail] = useState(localStorage.getItem('affiliate_email') || '');
  const [payouts, setPayouts] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);
  const [requestForm, setRequestForm] = useState({
    amount: '',
    payment_method: 'paypal',
    payment_email: ''
  });

  useEffect(() => {
    if (!affiliateEmail) {
      navigate('/affiliate');
      return;
    }
    
    fetchData();
  }, [affiliateEmail]);

  const fetchData = async () => {
    try {
      const [dashboardRes, payoutsRes] = await Promise.all([
        axios.get(`${BACKEND_URL}/api/affiliates/dashboard/${affiliateEmail}`),
        axios.get(`${BACKEND_URL}/api/affiliates/payouts/${affiliateEmail}`)
      ]);
      
      setDashboard(dashboardRes.data);
      setPayouts(payoutsRes.data);
      
      // Set default payment email
      if (dashboardRes.data.affiliate.payment_email) {
        setRequestForm(prev => ({
          ...prev,
          payment_email: dashboardRes.data.affiliate.payment_email
        }));
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestPayout = async (e) => {
    e.preventDefault();
    
    if (!requestForm.amount || parseFloat(requestForm.amount) < 50) {
      alert('El monto mínimo de retiro es $50 USD');
      return;
    }

    if (parseFloat(requestForm.amount) > dashboard.stats.approved_commissions) {
      alert('No tienes suficiente balance aprobado');
      return;
    }

    setRequesting(true);
    
    try {
      await axios.post(
        `${BACKEND_URL}/api/affiliates/payouts/request?affiliate_email=${affiliateEmail}`,
        requestForm
      );
      
      alert('¡Solicitud de pago enviada exitosamente!');
      setRequestForm({ amount: '', payment_method: 'paypal', payment_email: dashboard.affiliate.payment_email });
      fetchData();
    } catch (error) {
      console.error('Error requesting payout:', error);
      alert(error.response?.data?.detail || 'Error al solicitar pago');
    } finally {
      setRequesting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="p-6 text-center">
        <p className="text-gray-600">No se pudo cargar la información</p>
      </div>
    );
  }

  const { stats } = dashboard;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-8">
        <button
          onClick={() => navigate('/affiliate-dashboard')}
          className="text-blue-600 hover:text-blue-700 mb-4"
        >
          ← Volver al Dashboard
        </button>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Solicitar Pago
        </h1>
        <p className="text-gray-600">
          Gestiona tus solicitudes de pago y retiros
        </p>
      </div>

      {/* Balance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-yellow-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-yellow-100 p-2 rounded-lg">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Pendientes</p>
              <p className="text-2xl font-bold text-gray-900">${stats.pending_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-green-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-green-100 p-2 rounded-lg">
              <DollarSign className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Disponible para Retiro</p>
              <p className="text-2xl font-bold text-gray-900">${stats.approved_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-blue-100 p-2 rounded-lg">
              <CheckCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Pagado</p>
              <p className="text-2xl font-bold text-gray-900">${stats.paid_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Request Form */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Solicitar Nuevo Pago</h2>
        
        {stats.approved_commissions < 50 ? (
          <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6 text-center">
            <p className="text-yellow-800 font-semibold mb-2">
              Balance insuficiente
            </p>
            <p className="text-yellow-700">
              Necesitas al menos $50 USD en comisiones aprobadas para solicitar un pago.
              Actualmente tienes: ${stats.approved_commissions.toFixed(2)}
            </p>
          </div>
        ) : (
          <form onSubmit={handleRequestPayout} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monto a Retirar *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <DollarSign className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="number"
                  step="0.01"
                  min="50"
                  max={stats.approved_commissions}
                  required
                  value={requestForm.amount}
                  onChange={(e) => setRequestForm({ ...requestForm, amount: e.target.value })}
                  className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="50.00"
                />
              </div>
              <p className="text-sm text-gray-500 mt-1">
                Mínimo: $50 USD | Disponible: ${stats.approved_commissions.toFixed(2)}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Método de Pago
              </label>
              <select
                value={requestForm.payment_method}
                onChange={(e) => setRequestForm({ ...requestForm, payment_method: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="paypal">PayPal</option>
                <option value="bank_transfer">Transferencia Bancaria</option>
                <option value="stripe">Stripe</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email de Pago (PayPal) *
              </label>
              <input
                type="email"
                required
                value={requestForm.payment_email}
                onChange={(e) => setRequestForm({ ...requestForm, payment_email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="pagos@email.com"
              />
            </div>

            <button
              type="submit"
              disabled={requesting}
              className="w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {requesting ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Procesando...
                </>
              ) : (
                <>
                  <CreditCard className="w-5 h-5 mr-2" />
                  Solicitar Pago
                </>
              )}
            </button>
          </form>
        )}
      </div>

      {/* Payout History */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Historial de Pagos</h2>
        
        {payouts.length === 0 ? (
          <p className="text-gray-600 text-center py-8">
            No tienes solicitudes de pago aún
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Método</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Solicitud</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Proceso</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {payouts.map((payout) => (
                  <tr key={payout.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-gray-900">
                        ${payout.amount.toFixed(2)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900 capitalize">
                        {payout.method.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-600">
                        {payout.payment_email}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        payout.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : payout.status === 'processing'
                          ? 'bg-blue-100 text-blue-800'
                          : payout.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {payout.status === 'completed' ? 'Completado' :
                         payout.status === 'processing' ? 'Procesando' :
                         payout.status === 'failed' ? 'Fallido' : 'Pendiente'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(payout.requested_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {payout.processed_at ? new Date(payout.processed_at).toLocaleDateString() : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Info Box */}
      <div className="mt-8 bg-blue-50 rounded-xl p-6">
        <h3 className="font-semibold text-blue-900 mb-2">Información Importante</h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• Monto mínimo de retiro: $50 USD</li>
          <li>• Los pagos se procesan en 5-7 días hábiles</li>
          <li>• Recibirás una confirmación por email cuando se procese tu pago</li>
          <li>• Solo puedes tener una solicitud pendiente a la vez</li>
          <li>• Asegúrate de que tu email de pago sea correcto</li>
        </ul>
      </div>
    </div>
  );
};

export default AffiliatePayoutsPage;
