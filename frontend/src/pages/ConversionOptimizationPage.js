import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import RecommendationsWidget from '../components/RecommendationsWidget';
import {
  TestTube,
  Sparkles,
  Mail,
  ShoppingCart,
  TrendingUp,
  Plus,
  Play,
  Pause,
  Check,
  AlertCircle,
  Loader2
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const ConversionOptimizationPage = () => {
  const [activeTab, setActiveTab] = useState('ab-testing');
  const [loading, setLoading] = useState(true);

  const tabs = [
    { id: 'ab-testing', label: 'A/B Testing', icon: TestTube },
    { id: 'recommendations', label: 'Recomendaciones IA', icon: Sparkles },
    { id: 'email', label: 'Email Marketing', icon: Mail },
    { id: 'cart-recovery', label: 'Recuperar Carritos', icon: ShoppingCart }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          📈 Optimización de Conversión
        </h1>
        <p className="text-gray-600">
          Herramientas avanzadas para maximizar tus conversiones
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <TestTube className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">0</h3>
          <p className="text-blue-100 text-sm">Tests A/B Activos</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Sparkles className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">0%</h3>
          <p className="text-purple-100 text-sm">Acierto en Recomendaciones</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Mail className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">0%</h3>
          <p className="text-green-100 text-sm">Tasa de Apertura Emails</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <ShoppingCart className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">0%</h3>
          <p className="text-orange-100 text-sm">Recovery de Carritos</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <div className="flex overflow-x-auto">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'ab-testing' && <ABTestingTab />}
          {activeTab === 'recommendations' && <RecommendationsTab />}
          {activeTab === 'email' && <EmailMarketingTab />}
          {activeTab === 'cart-recovery' && <CartRecoveryTab />}
        </div>
      </div>
    </div>
  );
};

// A/B Testing Tab
const ABTestingTab = () => {
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTests();
  }, []);

  const fetchTests = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/ab-tests`);
      setTests(response.data);
    } catch (error) {
      console.error('Error fetching tests:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">A/B Testing de Códigos de Descuento</h2>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
          <Plus className="w-5 h-5 mr-2" />
          Crear Test
        </button>
      </div>

      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-blue-900 mb-2">🧪 Testea y Optimiza</h3>
        <p className="text-blue-800 mb-4">
          Compara diferentes códigos de descuento y porcentajes para encontrar la combinación que genera más conversiones.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Múltiples variantes por test</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Tracking automático de conversiones</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Análisis estadístico de resultados</span>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500 mx-auto" />
        </div>
      ) : tests.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <TestTube className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p>No hay tests A/B creados aún</p>
          <p className="text-sm mt-2">Crea tu primer test para comparar códigos de descuento</p>
        </div>
      ) : (
        <div className="space-y-4">
          {tests.map((test) => (
            <div key={test.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{test.test_name}</h3>
                  <p className="text-sm text-gray-600">{test.description}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  test.status === 'running' ? 'bg-green-100 text-green-800' :
                  test.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {test.status === 'running' ? 'Activo' : test.status === 'completed' ? 'Completado' : 'Pausado'}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {test.variants.map((variant) => (
                  <div key={variant.variant_name} className="bg-gray-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-gray-900">Variante {variant.variant_name}</span>
                      {test.winner === variant.variant_name && (
                        <Check className="w-5 h-5 text-green-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      Código: <span className="font-mono font-semibold">{variant.discount_code}</span>
                    </p>
                    <p className="text-sm text-gray-600 mb-2">
                      Descuento: <span className="font-semibold">{variant.discount_percentage}%</span>
                    </p>
                    <div className="mt-4 space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Impresiones:</span>
                        <span className="font-semibold">{variant.impressions}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Conversiones:</span>
                        <span className="font-semibold">{variant.conversions}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Tasa:</span>
                        <span className="font-semibold text-blue-600">
                          {variant.conversion_rate || 0}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Revenue:</span>
                        <span className="font-semibold text-green-600">
                          ${variant.revenue?.toFixed(2) || '0.00'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Recommendations Tab
const RecommendationsTab = () => {
  const navigate = useNavigate();
  
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Recomendaciones de Productos con IA</h2>
        <button 
          onClick={() => navigate('/recommendations')}
          className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center"
        >
          <Sparkles className="w-5 h-5 mr-2" />
          Ver Panel Completo
        </button>
      </div>
      
      <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-purple-900 mb-2">🤖 Personalización Inteligente</h3>
        <p className="text-purple-800 mb-4">
          Sistema avanzado con OpenAI Embeddings y Collaborative Filtering para recomendaciones personalizadas en tiempo real.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-purple-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>OpenAI Embeddings</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Collaborative Filtering</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Click Tracking</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Feedback Loop en Tiempo Real</span>
          </div>
        </div>
      </div>

      {/* Widget de Recomendaciones */}
      <RecommendationsWidget 
        algorithm="hybrid"
        limit={6}
        title="Productos Recomendados para Ti"
      />
    </div>
  );
};

// Email Marketing Tab
const EmailMarketingTab = () => {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Email Marketing Automation</h2>
        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center">
          <Plus className="w-5 h-5 mr-2" />
          Nueva Campaña
        </button>
      </div>

      <div className="bg-green-50 border-2 border-green-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-green-900 mb-2">📧 Automatiza tus Emails</h3>
        <p className="text-green-800 mb-4">
          Crea campañas de email personalizadas, programa envíos y trackea resultados en tiempo real.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-green-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Templates personalizables</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Segmentación de audiencia</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Tracking de opens y clicks</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {[
          { label: 'Campañas Activas', value: '0', color: 'blue' },
          { label: 'Tasa de Apertura', value: '0%', color: 'green' },
          { label: 'Click Rate', value: '0%', color: 'purple' },
          { label: 'Conversiones', value: '0', color: 'orange' }
        ].map((stat, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
            <p className={`text-2xl font-bold text-${stat.color}-600`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="text-center py-12 text-gray-500">
        <Mail className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <p>No hay campañas de email creadas</p>
        <p className="text-sm mt-2">Crea tu primera campaña para comenzar</p>
      </div>
    </div>
  );
};

// Cart Recovery Tab
const CartRecoveryTab = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Recuperación de Carritos Abandonados</h2>
      
      <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-orange-900 mb-2">🛒 Recupera Ventas Perdidas</h3>
        <p className="text-orange-800 mb-4">
          Sistema automático para recuperar carritos abandonados con emails personalizados y descuentos especiales.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-orange-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Detección automática de abandono</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Emails de recovery automáticos</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Descuentos personalizados</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Carritos Abandonados</h3>
          <p className="text-4xl font-bold text-orange-600 mb-2">0</p>
          <p className="text-sm text-gray-500">$0.00 en valor</p>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Tasa de Recovery</h3>
          <p className="text-4xl font-bold text-green-600 mb-2">0%</p>
          <p className="text-sm text-gray-500">0 recuperados</p>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Revenue Recuperado</h3>
          <p className="text-4xl font-bold text-blue-600 mb-2">$0.00</p>
          <p className="text-sm text-gray-500">Este mes</p>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-gray-900 mb-4">Configuración de Recovery</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tiempo de espera antes de email
            </label>
            <select className="w-full px-4 py-2 border border-gray-300 rounded-lg">
              <option>1 hora</option>
              <option>3 horas</option>
              <option>6 horas</option>
              <option>24 horas</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Descuento de recovery
            </label>
            <select className="w-full px-4 py-2 border border-gray-300 rounded-lg">
              <option>5%</option>
              <option>10%</option>
              <option>15%</option>
              <option>20%</option>
            </select>
          </div>
        </div>

        <div className="mt-6">
          <button className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 transition-colors">
            Guardar Configuración
          </button>
        </div>
      </div>

      <div className="text-center py-8 text-gray-500">
        <ShoppingCart className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <p>No hay carritos abandonados registrados</p>
        <p className="text-sm mt-2">Los carritos se detectarán automáticamente</p>
      </div>
    </div>
  );
};

export default ConversionOptimizationPage;
