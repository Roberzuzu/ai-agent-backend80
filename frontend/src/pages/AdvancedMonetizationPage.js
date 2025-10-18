import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  ShoppingBag, 
  Package, 
  Crown, 
  Heart,
  ExternalLink,
  Plus,
  TrendingUp,
  DollarSign,
  Users,
  Target
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const AdvancedMonetizationPage = () => {
  const [activeTab, setActiveTab] = useState('amazon');
  const [stats, setStats] = useState({
    amazon: null,
    dropshipping: null,
    donations: null
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [amazonRes, dropshippingRes, donationsRes] = await Promise.all([
        axios.get(`${BACKEND_URL}/api/amazon/analytics`).catch(() => ({ data: null })),
        axios.get(`${BACKEND_URL}/api/dropshipping/analytics`).catch(() => ({ data: null })),
        axios.get(`${BACKEND_URL}/api/donations/stats`).catch(() => ({ data: null }))
      ]);

      setStats({
        amazon: amazonRes.data,
        dropshipping: dropshippingRes.data,
        donations: donationsRes.data
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'amazon', label: 'Amazon Associates', icon: ShoppingBag },
    { id: 'dropshipping', label: 'Dropshipping', icon: Package },
    { id: 'memberships', label: 'Membresías', icon: Crown },
    { id: 'donations', label: 'Donaciones', icon: Heart }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          💰 Monetización Avanzada
        </h1>
        <p className="text-gray-600">
          Múltiples fuentes de ingresos para maximizar ganancias
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <ShoppingBag className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">
            ${stats.amazon?.estimated_earnings?.toFixed(2) || '0.00'}
          </h3>
          <p className="text-orange-100 text-sm">Amazon Associates</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Package className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">
            ${stats.dropshipping?.total_revenue?.toFixed(2) || '0.00'}
          </h3>
          <p className="text-blue-100 text-sm">Dropshipping</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Crown className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">
            0
          </h3>
          <p className="text-purple-100 text-sm">Miembros Premium</p>
        </div>

        <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Heart className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">
            ${stats.donations?.total_amount?.toFixed(2) || '0.00'}
          </h3>
          <p className="text-pink-100 text-sm">Donaciones</p>
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
          {activeTab === 'amazon' && <AmazonTab />}
          {activeTab === 'dropshipping' && <DropshippingTab />}
          {activeTab === 'memberships' && <MembershipsTab />}
          {activeTab === 'donations' && <DonationsTab />}
        </div>
      </div>
    </div>
  );
};

// Amazon Associates Tab
const AmazonTab = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Amazon Associates</h2>
      <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-orange-900 mb-2">🛒 Integración con Amazon</h3>
        <p className="text-orange-800 mb-4">
          Vincula productos de tu catálogo con Amazon y gana comisiones por cada venta referida.
        </p>
        <div className="space-y-2 text-sm text-orange-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Links de afiliado automáticos con tu Associate Tag</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Tracking de clicks y conversiones estimadas</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Comisión promedio 4% por venta</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="border border-gray-200 rounded-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Cómo Funciona</h3>
          <ol className="space-y-3 text-sm text-gray-700">
            <li className="flex items-start">
              <span className="font-bold text-blue-600 mr-2">1.</span>
              <span>Registra tu Amazon Associate Tag</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold text-blue-600 mr-2">2.</span>
              <span>Vincula productos con su ASIN de Amazon</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold text-blue-600 mr-2">3.</span>
              <span>El sistema genera links de afiliado automáticamente</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold text-blue-600 mr-2">4.</span>
              <span>Comparte los links y gana comisiones</span>
            </li>
          </ol>
        </div>

        <div className="border border-gray-200 rounded-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
          <div className="space-y-3">
            <button className="w-full bg-orange-600 text-white py-2 px-4 rounded-lg hover:bg-orange-700 transition-colors flex items-center justify-center">
              <Plus className="w-5 h-5 mr-2" />
              Vincular Producto con Amazon
            </button>
            <button className="w-full bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors flex items-center justify-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              Ver Analytics
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dropshipping Tab
const DropshippingTab = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Dropshipping Automation</h2>
      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-blue-900 mb-2">📦 Vende Sin Inventario</h3>
        <p className="text-blue-800 mb-4">
          Automatiza todo el proceso de dropshipping: desde la orden hasta la entrega.
        </p>
        <div className="space-y-2 text-sm text-blue-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Conexión con proveedores (AliExpress, CJ Dropshipping)</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Fulfillment automático de órdenes</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Tracking de envíos en tiempo real</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="text-center mb-4">
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
              <Package className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Órdenes Pendientes</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">0</p>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="text-center mb-4">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
              <Target className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900">En Camino</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">0</p>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="text-center mb-4">
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
              <DollarSign className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Completadas</h3>
            <p className="text-3xl font-bold text-purple-600 mt-2">0</p>
          </div>
        </div>
      </div>

      <div className="text-center py-8 text-gray-500">
        <Package className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <p>No hay órdenes de dropshipping aún</p>
        <p className="text-sm mt-2">Configura proveedores y comienza a vender</p>
      </div>
    </div>
  );
};

// Memberships Tab
const MembershipsTab = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Membresías & Contenido Premium</h2>
      <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-purple-900 mb-2">👑 Monetiza tu Contenido</h3>
        <p className="text-purple-800 mb-4">
          Crea contenido exclusivo y ofrece membresías de pago con diferentes niveles de acceso.
        </p>
        <div className="space-y-2 text-sm text-purple-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>4 niveles: Free, Basic ($9.99), Pro ($29.99), VIP ($99.99)</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Contenido bloqueado por nivel de membresía</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Ingresos recurrentes mensuales</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {['Free', 'Basic', 'Pro', 'VIP'].map((level, index) => (
          <div key={level} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="text-center">
              <Crown className={`w-12 h-12 mx-auto mb-2 ${
                index === 0 ? 'text-gray-400' :
                index === 1 ? 'text-blue-500' :
                index === 2 ? 'text-purple-500' : 'text-yellow-500'
              }`} />
              <h3 className="font-bold text-gray-900">{level}</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">
                ${index === 0 ? '0' : index === 1 ? '9.99' : index === 2 ? '29.99' : '99.99'}
              </p>
              <p className="text-sm text-gray-600">/mes</p>
              <p className="text-sm text-gray-600 mt-2">0 miembros</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <button className="bg-purple-600 text-white py-3 px-6 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center">
          <Plus className="w-5 h-5 mr-2" />
          Crear Contenido Premium
        </button>
        <button className="bg-gray-200 text-gray-800 py-3 px-6 rounded-lg hover:bg-gray-300 transition-colors flex items-center justify-center">
          <Users className="w-5 h-5 mr-2" />
          Gestionar Miembros
        </button>
      </div>
    </div>
  );
};

// Donations Tab
const DonationsTab = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Donaciones & Tips</h2>
      <div className="bg-pink-50 border-2 border-pink-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-pink-900 mb-2">💝 Recibe Apoyo de tu Comunidad</h3>
        <p className="text-pink-800 mb-4">
          Permite que tus seguidores te apoyen con donaciones voluntarias y tips por contenido.
        </p>
        <div className="space-y-2 text-sm text-pink-700">
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Donaciones one-time con mensaje personalizado</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Tips por contenido específico</span>
          </div>
          <div className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Leaderboard de donadores top</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Total Donaciones</h3>
          <p className="text-3xl font-bold text-pink-600">$0.00</p>
          <p className="text-sm text-gray-500 mt-1">0 donadores</p>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Total Tips</h3>
          <p className="text-3xl font-bold text-pink-600">$0.00</p>
          <p className="text-sm text-gray-500 mt-1">0 tips</p>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-sm text-gray-600 mb-2">Promedio</h3>
          <p className="text-3xl font-bold text-pink-600">$0.00</p>
          <p className="text-sm text-gray-500 mt-1">por donación</p>
        </div>
      </div>

      <div className="text-center py-8 text-gray-500">
        <Heart className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <p>No has recibido donaciones aún</p>
        <p className="text-sm mt-2">Comparte tu link de donaciones con tu audiencia</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <button className="bg-pink-600 text-white py-3 px-6 rounded-lg hover:bg-pink-700 transition-colors flex items-center justify-center">
          <Plus className="w-5 h-5 mr-2" />
          Crear Meta de Donación
        </button>
        <button className="bg-gray-200 text-gray-800 py-3 px-6 rounded-lg hover:bg-gray-300 transition-colors flex items-center justify-center">
          <Users className="w-5 h-5 mr-2" />
          Ver Leaderboard
        </button>
      </div>
    </div>
  );
};

export default AdvancedMonetizationPage;
