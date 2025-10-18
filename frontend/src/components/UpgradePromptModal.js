import React from 'react';
import { X, Check, Crown, Zap, Star } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const UpgradePromptModal = ({ isOpen, onClose, currentTier, limitType }) => {
  const navigate = useNavigate();

  if (!isOpen) return null;

  const tiers = {
    basic: {
      name: 'Básico',
      price: 0,
      icon: Star,
      color: 'gray',
      features: [
        '10 productos',
        '20 posts al mes',
        '3 campañas',
        '5 afiliados',
        '100MB almacenamiento'
      ]
    },
    pro: {
      name: 'Pro',
      price: 29.99,
      icon: Zap,
      color: 'blue',
      features: [
        'Productos ilimitados',
        '100 posts al mes',
        '10 campañas',
        '25 afiliados',
        '1GB almacenamiento',
        'Soporte prioritario',
        'Analytics avanzado'
      ]
    },
    vip: {
      name: 'VIP',
      price: 99.99,
      icon: Crown,
      color: 'purple',
      features: [
        'TODO ilimitado',
        'API dedicada',
        'Soporte 24/7',
        'Branded experience',
        'Consultoría mensual',
        'Custom features'
      ]
    }
  };

  const handleUpgrade = (tier) => {
    onClose();
    navigate(`/subscriptions?plan=${tier}`);
  };

  const messages = {
    products: '¡Has alcanzado el límite de productos!',
    posts_per_month: '¡Has alcanzado el límite de posts este mes!',
    campaigns: '¡Has alcanzado el límite de campañas!',
    affiliates: '¡Has alcanzado el límite de afiliados!'
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div 
        className="fixed inset-0 bg-black bg-opacity-60 transition-opacity"
        onClick={onClose}
      ></div>

      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-5xl w-full transform transition-all animate-scaleIn">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 z-10"
          >
            <X className="w-6 h-6" />
          </button>

          {/* Header */}
          <div className="text-center p-8 border-b border-gray-200 dark:border-gray-700">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full mb-4">
              <Crown className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              {messages[limitType] || '¡Mejora tu Plan!'}
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Desbloquea más funcionalidades con un plan superior
            </p>
          </div>

          {/* Plans */}
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(tiers).map(([key, tier]) => {
                const Icon = tier.icon;
                const isCurrentTier = key === currentTier;
                const isRecommended = key === 'pro';

                return (
                  <div
                    key={key}
                    className={`relative rounded-xl border-2 p-6 transition-all ${
                      isCurrentTier
                        ? 'border-gray-300 dark:border-gray-600 opacity-75'
                        : isRecommended
                        ? 'border-blue-500 shadow-lg transform scale-105'
                        : 'border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600'
                    }`}
                  >
                    {isRecommended && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                          Recomendado
                        </span>
                      </div>
                    )}

                    {isCurrentTier && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span className="bg-gray-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                          Plan Actual
                        </span>
                      </div>
                    )}

                    <div className="text-center mb-6">
                      <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full mb-3 ${
                        tier.color === 'gray' ? 'bg-gray-100 dark:bg-gray-700' :
                        tier.color === 'blue' ? 'bg-blue-100 dark:bg-blue-900' :
                        'bg-purple-100 dark:bg-purple-900'
                      }`}>
                        <Icon className={`w-6 h-6 ${
                          tier.color === 'gray' ? 'text-gray-600' :
                          tier.color === 'blue' ? 'text-blue-600' :
                          'text-purple-600'
                        }`} />
                      </div>
                      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                        {tier.name}
                      </h3>
                      <div className="text-4xl font-bold text-gray-900 dark:text-white">
                        ${tier.price}
                        {tier.price > 0 && (
                          <span className="text-lg text-gray-500 font-normal">/mes</span>
                        )}
                      </div>
                    </div>

                    <ul className="space-y-3 mb-6">
                      {tier.features.map((feature, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <button
                      onClick={() => handleUpgrade(key)}
                      disabled={isCurrentTier}
                      className={`w-full py-3 rounded-lg font-semibold transition-all ${
                        isCurrentTier
                          ? 'bg-gray-200 dark:bg-gray-700 text-gray-500 cursor-not-allowed'
                          : isRecommended
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
                          : 'bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-gray-100'
                      }`}
                    >
                      {isCurrentTier ? 'Plan Actual' : 'Seleccionar Plan'}
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 bg-gray-50 dark:bg-gray-900 rounded-b-2xl text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              ¿Preguntas? <a href="mailto:support@example.com" className="text-blue-600 hover:text-blue-700 underline">Contacta con soporte</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UpgradePromptModal;
