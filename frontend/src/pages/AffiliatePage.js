import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, TrendingUp, DollarSign, Link as LinkIcon, Copy, CheckCircle, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const AffiliatePage = () => {
  const [isRegistered, setIsRegistered] = useState(false);
  const [affiliateEmail, setAffiliateEmail] = useState(localStorage.getItem('affiliate_email') || '');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    payment_email: '',
    payment_method: 'paypal'
  });

  useEffect(() => {
    if (affiliateEmail) {
      checkAffiliateStatus();
    }
  }, []);

  const checkAffiliateStatus = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/affiliates/by-email/${affiliateEmail}`);
      if (response.data) {
        setIsRegistered(true);
      }
    } catch (error) {
      // Not registered
      localStorage.removeItem('affiliate_email');
      setAffiliateEmail('');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(`${BACKEND_URL}/api/affiliates/register`, formData);
      
      if (response.data.affiliate) {
        localStorage.setItem('affiliate_email', formData.email);
        setAffiliateEmail(formData.email);
        setIsRegistered(true);
        alert('¡Registro exitoso! Bienvenido al programa de afiliados.');
      }
    } catch (error) {
      console.error('Error registering:', error);
      alert(error.response?.data?.detail || 'Error al registrarse');
    } finally {
      setLoading(false);
    }
  };

  if (isRegistered) {
    window.location.href = '/affiliate-dashboard';
    return null;
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white mb-8">
        <h1 className="text-4xl font-bold mb-4">
          💰 Programa de Afiliados
        </h1>
        <p className="text-xl mb-6">
          Gana comisiones promoviendo nuestros productos. ¡Es gratis unirse!
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <DollarSign className="w-12 h-12 mb-4" />
            <h3 className="text-xl font-semibold mb-2">10% de Comisión</h3>
            <p className="text-white/80">Por cada venta que generes</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <LinkIcon className="w-12 h-12 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Links Únicos</h3>
            <p className="text-white/80">Para trackear tus referidos</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <TrendingUp className="w-12 h-12 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Dashboard Completo</h3>
            <p className="text-white/80">Estadísticas en tiempo real</p>
          </div>
        </div>
      </div>

      {/* How it Works */}
      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">¿Cómo Funciona?</h2>
        
        <div className="space-y-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              1
            </div>
            <div>
              <h3 className="font-semibold text-lg text-gray-900">Regístrate Gratis</h3>
              <p className="text-gray-600">
                Completa el formulario y obtén tu código único de afiliado
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-10 h-10 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">
              2
            </div>
            <div>
              <h3 className="font-semibold text-lg text-gray-900">Genera Links</h3>
              <p className="text-gray-600">
                Crea links únicos para cualquier producto del catálogo
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-10 h-10 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
              3
            </div>
            <div>
              <h3 className="font-semibold text-lg text-gray-900">Promociona</h3>
              <p className="text-gray-600">
                Comparte tus links en redes sociales, blog, email, etc.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-10 h-10 bg-yellow-600 text-white rounded-full flex items-center justify-center font-bold">
              4
            </div>
            <div>
              <h3 className="font-semibold text-lg text-gray-900">Gana Dinero</h3>
              <p className="text-gray-600">
                Recibe 10% de comisión por cada venta. Pagos mensuales vía PayPal o transferencia
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Registration Form */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Únete Ahora</h2>
        
        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nombre Completo *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Juan Pérez"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email *
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="tu@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Método de Pago
            </label>
            <select
              value={formData.payment_method}
              onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="paypal">PayPal</option>
              <option value="bank_transfer">Transferencia Bancaria</option>
              <option value="stripe">Stripe</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email de Pago (PayPal)
            </label>
            <input
              type="email"
              value={formData.payment_email}
              onChange={(e) => setFormData({ ...formData, payment_email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="pagos@email.com (opcional)"
            />
            <p className="text-sm text-gray-500 mt-1">
              Si está vacío, usaremos tu email principal
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin mr-2" />
                Registrando...
              </>
            ) : (
              'Registrarse como Afiliado'
            )}
          </button>
        </form>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Nota:</strong> Al registrarte aceptas nuestros términos y condiciones del programa de afiliados. 
            Las comisiones se pagan mensualmente con un mínimo de $50 USD.
          </p>
        </div>
      </div>

      {/* Benefits */}
      <div className="mt-8 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Beneficios Exclusivos</h2>
        <ul className="space-y-3">
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Sin cuota de inscripción</span>
          </li>
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Pagos automáticos mensuales</span>
          </li>
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Dashboard con estadísticas en tiempo real</span>
          </li>
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Tracking automático de clicks y conversiones</span>
          </li>
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Materiales de marketing incluidos</span>
          </li>
          <li className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <span className="text-gray-700">Soporte dedicado para afiliados</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default AffiliatePage;
