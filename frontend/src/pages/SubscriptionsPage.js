import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Check, Crown, Zap, Star, Loader2, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const SubscriptionsPage = () => {
  const [plans, setPlans] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingPlan, setProcessingPlan] = useState(null);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    fetchPlans();
    fetchSubscriptions();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/subscriptions/plans`);
      setPlans(response.data);
    } catch (error) {
      console.error('Error fetching plans:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubscriptions = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/subscriptions`);
      setSubscriptions(response.data);
    } catch (error) {
      console.error('Error fetching subscriptions:', error);
    }
  };

  const handleSubscribe = async (planId) => {
    if (!userEmail) {
      alert('Por favor ingresa tu email');
      return;
    }

    setProcessingPlan(planId);
    
    try {
      const originUrl = window.location.origin;
      const response = await axios.post(`${BACKEND_URL}/api/payments/checkout/session`, {
        payment_type: 'subscription',
        plan_id: planId,
        user_email: userEmail,
        origin_url: originUrl,
        metadata: {
          source: 'subscription_page'
        }
      });

      // Redirect to Stripe checkout
      if (response.data.url) {
        window.location.href = response.data.url;
      }
    } catch (error) {
      console.error('Error creating checkout:', error);
      alert('Error al crear la sesión de pago. Intenta de nuevo.');
      setProcessingPlan(null);
    }
  };

  const handleCancelSubscription = async (subscriptionId) => {
    if (!window.confirm('¿Estás seguro de que quieres cancelar esta suscripción?')) {
      return;
    }

    try {
      await axios.post(`${BACKEND_URL}/api/subscriptions/${subscriptionId}/cancel`);
      alert('Suscripción cancelada exitosamente');
      fetchSubscriptions();
    } catch (error) {
      console.error('Error cancelling subscription:', error);
      alert('Error al cancelar la suscripción');
    }
  };

  const getPlanIcon = (planId) => {
    switch (planId) {
      case 'basic':
        return <Star className="w-8 h-8 text-blue-500" />;
      case 'pro':
        return <Zap className="w-8 h-8 text-purple-500" />;
      case 'enterprise':
        return <Crown className="w-8 h-8 text-yellow-500" />;
      default:
        return <Star className="w-8 h-8 text-gray-500" />;
    }
  };

  const getPlanColor = (planId) => {
    switch (planId) {
      case 'basic':
        return 'border-blue-500';
      case 'pro':
        return 'border-purple-500';
      case 'enterprise':
        return 'border-yellow-500';
      default:
        return 'border-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Planes de Suscripción</h1>
        <p className="text-gray-600">Elige el plan perfecto para hacer crecer tu negocio</p>
      </div>

      {/* Email Input */}
      <div className="mb-8 max-w-md">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Email para la suscripción
        </label>
        <input
          type="email"
          value={userEmail}
          onChange={(e) => setUserEmail(e.target.value)}
          placeholder="tu@email.com"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Plans Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className={`bg-white rounded-xl shadow-lg border-2 ${getPlanColor(plan.id)} overflow-hidden transform transition-all hover:scale-105`}
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                {getPlanIcon(plan.id)}
                {plan.id === 'pro' && (
                  <span className="bg-purple-100 text-purple-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    Popular
                  </span>
                )}
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
              
              <div className="mb-4">
                <span className="text-4xl font-bold text-gray-900">${plan.price}</span>
                <span className="text-gray-600">/mes</span>
              </div>

              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start">
                    <Check className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleSubscribe(plan.id)}
                disabled={processingPlan === plan.id}
                className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-colors ${
                  plan.id === 'pro'
                    ? 'bg-purple-600 hover:bg-purple-700'
                    : plan.id === 'enterprise'
                    ? 'bg-yellow-600 hover:bg-yellow-700'
                    : 'bg-blue-600 hover:bg-blue-700'
                } disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center`}
              >
                {processingPlan === plan.id ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin mr-2" />
                    Procesando...
                  </>
                ) : (
                  'Suscribirse Ahora'
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Active Subscriptions */}
      {subscriptions.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Tus Suscripciones Activas</h2>
          
          <div className="space-y-4">
            {subscriptions.map((subscription) => {
              const plan = plans.find(p => p.id === subscription.plan_id);
              return (
                <div
                  key={subscription.id}
                  className="border border-gray-200 rounded-lg p-4 flex items-center justify-between"
                >
                  <div className="flex items-center space-x-4">
                    {getPlanIcon(subscription.plan_id)}
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {plan?.name || subscription.plan_id}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {subscription.user_email}
                      </p>
                      <p className="text-sm text-gray-500">
                        Periodo: {new Date(subscription.current_period_start).toLocaleDateString()} - {new Date(subscription.current_period_end).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      subscription.status === 'active'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {subscription.status === 'active' ? 'Activa' : subscription.status}
                    </span>

                    {subscription.status === 'active' && !subscription.cancel_at_period_end && (
                      <button
                        onClick={() => handleCancelSubscription(subscription.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Cancelar suscripción"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    )}

                    {subscription.cancel_at_period_end && (
                      <span className="text-sm text-orange-600 font-medium">
                        Se cancela al finalizar periodo
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default SubscriptionsPage;
