import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  DollarSign,
  TrendingUp,
  ShoppingCart,
  Users,
  CreditCard,
  Target,
  Percent,
  Package,
  Loader2,
  RefreshCw
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const RevenueAnalyticsPage = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/analytics/dashboard-advanced`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchAnalytics();
  };

  if (loading && !analytics) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="p-6">
        <div className="text-center text-gray-500">
          No se pudieron cargar los datos
        </div>
      </div>
    );
  }

  const revenue = analytics.revenue;
  const campaignRoi = analytics.campaign_roi;
  const affiliate = analytics.affiliate_commissions;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Dashboard de Ingresos 💰
          </h1>
          <p className="text-gray-600">
            Analytics completo de monetización y ROI
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
          <span>Actualizar</span>
        </button>
      </div>

      {/* Revenue Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <DollarSign className="w-8 h-8" />
            <span className="text-green-100 text-sm font-medium">Total</span>
          </div>
          <h3 className="text-3xl font-bold mb-1">
            ${revenue.total_revenue.toFixed(2)}
          </h3>
          <p className="text-green-100 text-sm">Ingresos Totales</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <ShoppingCart className="w-8 h-8" />
            <span className="text-blue-100 text-sm font-medium">Productos</span>
          </div>
          <h3 className="text-3xl font-bold mb-1">
            ${revenue.product_revenue.toFixed(2)}
          </h3>
          <p className="text-blue-100 text-sm">{revenue.product_sales} ventas</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <CreditCard className="w-8 h-8" />
            <span className="text-purple-100 text-sm font-medium">Suscripciones</span>
          </div>
          <h3 className="text-3xl font-bold mb-1">
            ${revenue.subscription_revenue.toFixed(2)}
          </h3>
          <p className="text-purple-100 text-sm">{revenue.subscription_sales} ventas</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Users className="w-8 h-8" />
            <span className="text-orange-100 text-sm font-medium">Activas</span>
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {revenue.active_subscriptions}
          </h3>
          <p className="text-orange-100 text-sm">MRR: ${revenue.mrr.toFixed(2)}</p>
        </div>
      </div>

      {/* Discount Code Tracking */}
      {Object.keys(revenue.discount_code_tracking).length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex items-center space-x-2 mb-6">
            <Percent className="w-6 h-6 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-900">
              Tracking por Código de Descuento
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Código
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Producto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Descuento
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ventas
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ingresos
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.values(revenue.discount_code_tracking).map((item, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-mono font-semibold text-blue-600">
                        {item.discount_code}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{item.product_name}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{item.discount_percentage}%</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-gray-900">{item.sales_count}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-green-600">
                        ${item.revenue.toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Campaign ROI */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div className="flex items-center space-x-2 mb-6">
          <Target className="w-6 h-6 text-purple-600" />
          <h2 className="text-2xl font-bold text-gray-900">
            ROI por Campaña Publicitaria
          </h2>
        </div>

        {campaignRoi.campaigns.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            No hay campañas registradas
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Gasto Total en Ads</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${campaignRoi.total_ad_spend.toFixed(2)}
                </p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Ingresos Generados</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${campaignRoi.total_revenue.toFixed(2)}
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">ROI Promedio</p>
                <p className="text-2xl font-bold text-gray-900">
                  {campaignRoi.average_roi.toFixed(1)}%
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {campaignRoi.campaigns.map((campaign) => (
                <div
                  key={campaign.campaign_id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-gray-900">{campaign.campaign_name}</h3>
                      <p className="text-sm text-gray-600">{campaign.platform}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      campaign.roi >= 0
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      ROI: {campaign.roi_formatted}
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mt-4">
                    <div>
                      <p className="text-xs text-gray-500">Presupuesto</p>
                      <p className="text-sm font-semibold text-gray-900">
                        ${campaign.budget.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Ingresos</p>
                      <p className="text-sm font-semibold text-green-600">
                        ${campaign.revenue.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Estado</p>
                      <p className="text-sm font-semibold text-gray-900 capitalize">
                        {campaign.status}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Affiliate Commissions */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Package className="w-6 h-6 text-orange-600" />
          <h2 className="text-2xl font-bold text-gray-900">
            Comisiones de Afiliados
          </h2>
        </div>

        {affiliate.commissions.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            No hay productos con enlaces de afiliados
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-orange-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Comisiones Totales</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${affiliate.total_commissions.toFixed(2)}
                </p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Tasa de Comisión</p>
                <p className="text-2xl font-bold text-gray-900">
                  {affiliate.commission_rate}%
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Productos Afiliados</p>
                <p className="text-2xl font-bold text-gray-900">
                  {affiliate.affiliate_products}
                </p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Producto
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Categoría
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ventas
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ingresos
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Comisión
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {affiliate.commissions.map((item) => (
                    <tr key={item.product_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-medium text-gray-900">
                          {item.product_name}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-600">{item.category}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-semibold text-gray-900">
                          {item.sales_count}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-900">
                          ${item.revenue.toFixed(2)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-bold text-orange-600">
                          ${item.commission_earned.toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default RevenueAnalyticsPage;
