import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  DollarSign,
  MousePointer,
  TrendingUp,
  Link as LinkIcon,
  Copy,
  Check,
  Loader2,
  ExternalLink,
  Eye,
  ShoppingCart,
  Percent
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const AffiliateDashboardPage = () => {
  const navigate = useNavigate();
  const [affiliateEmail] = useState(localStorage.getItem('affiliate_email') || '');
  const [dashboard, setDashboard] = useState(null);
  const [links, setLinks] = useState([]);
  const [commissions, setCommissions] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [copiedLink, setCopiedLink] = useState(null);
  const [generatingLink, setGeneratingLink] = useState(null);

  useEffect(() => {
    if (!affiliateEmail) {
      navigate('/affiliate');
      return;
    }
    
    fetchDashboard();
    fetchLinks();
    fetchCommissions();
    fetchProducts();
  }, [affiliateEmail]);

  const fetchDashboard = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/affiliates/dashboard/${affiliateEmail}`);
      setDashboard(response.data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLinks = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/affiliates/links/${affiliateEmail}`);
      setLinks(response.data);
    } catch (error) {
      console.error('Error fetching links:', error);
    }
  };

  const fetchCommissions = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/affiliates/commissions/${affiliateEmail}`);
      setCommissions(response.data);
    } catch (error) {
      console.error('Error fetching commissions:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const generateLink = async (productId = null) => {
    setGeneratingLink(productId);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/affiliates/links/generate?affiliate_email=${affiliateEmail}`,
        { product_id: productId }
      );
      
      await fetchLinks();
      alert('Link generado exitosamente');
    } catch (error) {
      console.error('Error generating link:', error);
      alert('Error al generar link');
    } finally {
      setGeneratingLink(null);
    }
  };

  const copyLink = (link) => {
    const fullLink = `${window.location.origin}/track/${link.unique_code}${link.product_id ? `?product_id=${link.product_id}` : ''}`;
    navigator.clipboard.writeText(fullLink);
    setCopiedLink(link.id);
    setTimeout(() => setCopiedLink(null), 2000);
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
        <p className="text-gray-600">No se pudo cargar el dashboard</p>
      </div>
    );
  }

  const { affiliate, stats } = dashboard;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Dashboard de Afiliado
        </h1>
        <p className="text-gray-600">
          Bienvenido, <strong>{affiliate.name}</strong> - Código: <span className="font-mono text-blue-600">{affiliate.unique_code}</span>
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <DollarSign className="w-8 h-8" />
          </div>
          <h3 className="text-3xl font-bold mb-1">
            ${stats.total_earnings.toFixed(2)}
          </h3>
          <p className="text-green-100 text-sm">Ganancias Totales</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <MousePointer className="w-8 h-8" />
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {stats.total_clicks}
          </h3>
          <p className="text-blue-100 text-sm">Clicks Totales</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <ShoppingCart className="w-8 h-8" />
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {stats.total_conversions}
          </h3>
          <p className="text-purple-100 text-sm">Conversiones</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Percent className="w-8 h-8" />
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {stats.conversion_rate.toFixed(1)}%
          </h3>
          <p className="text-orange-100 text-sm">Tasa de Conversión</p>
        </div>
      </div>

      {/* Commission Balance */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-yellow-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-yellow-100 p-2 rounded-lg">
              <DollarSign className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Comisiones Pendientes</p>
              <p className="text-2xl font-bold text-gray-900">${stats.pending_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-green-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-green-100 p-2 rounded-lg">
              <Check className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Comisiones Aprobadas</p>
              <p className="text-2xl font-bold text-gray-900">${stats.approved_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-400">
          <div className="flex items-center space-x-3 mb-2">
            <div className="bg-blue-100 p-2 rounded-lg">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Comisiones Pagadas</p>
              <p className="text-2xl font-bold text-gray-900">${stats.paid_commissions.toFixed(2)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Generate Links Section */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Generar Links de Afiliado</h2>
        
        <div className="mb-4">
          <button
            onClick={() => generateLink(null)}
            disabled={generatingLink === null}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center space-x-2"
          >
            {generatingLink === null ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Generando...</span>
              </>
            ) : (
              <>
                <LinkIcon className="w-5 h-5" />
                <span>Generar Link General</span>
              </>
            )}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {products.slice(0, 6).map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{product.name}</h3>
                  <p className="text-sm text-gray-600">${product.price}</p>
                </div>
                <button
                  onClick={() => generateLink(product.id)}
                  disabled={generatingLink === product.id}
                  className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors disabled:opacity-50 flex items-center space-x-1"
                >
                  {generatingLink === product.id ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      <LinkIcon className="w-4 h-4" />
                      <span>Link</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* My Links */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Mis Links de Afiliado</h2>
        
        {links.length === 0 ? (
          <p className="text-gray-600 text-center py-8">
            No tienes links generados aún. Genera uno arriba.
          </p>
        ) : (
          <div className="space-y-4">
            {links.map((link) => (
              <div key={link.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">
                      {link.product_name || 'Link General'}
                    </h3>
                    {link.product_price && (
                      <p className="text-sm text-gray-600">${link.product_price}</p>
                    )}
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Clicks</p>
                      <p className="text-xl font-bold text-blue-600">{link.clicks}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Conversiones</p>
                      <p className="text-xl font-bold text-green-600">{link.conversions}</p>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3 flex items-center justify-between">
                  <code className="text-sm text-gray-700 flex-1 overflow-x-auto">
                    {window.location.origin}/track/{link.unique_code}{link.product_id ? `?product_id=${link.product_id}` : ''}
                  </code>
                  <button
                    onClick={() => copyLink(link)}
                    className="ml-2 p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                  >
                    {copiedLink === link.id ? (
                      <Check className="w-5 h-5 text-green-600" />
                    ) : (
                      <Copy className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Commissions */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Comisiones Recientes</h2>
        
        {commissions.length === 0 ? (
          <p className="text-gray-600 text-center py-8">
            No tienes comisiones aún. ¡Empieza a promocionar tus links!
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto Orden</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comisión</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {commissions.map((commission) => (
                  <tr key={commission.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">
                        {commission.product_name || 'N/A'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">
                        ${commission.order_amount.toFixed(2)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-green-600">
                        ${commission.commission_amount.toFixed(2)}
                      </span>
                      <span className="text-xs text-gray-500 ml-1">
                        ({commission.commission_rate}%)
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        commission.status === 'paid'
                          ? 'bg-green-100 text-green-800'
                          : commission.status === 'approved'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {commission.status === 'paid' ? 'Pagada' : commission.status === 'approved' ? 'Aprobada' : 'Pendiente'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(commission.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Request Payout Button */}
      {stats.approved_commissions >= 50 && (
        <div className="mt-8 bg-green-50 border-2 border-green-400 rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                ¡Tienes ${stats.approved_commissions.toFixed(2)} disponibles para retiro!
              </h3>
              <p className="text-gray-600">
                Solicita tu pago ahora y recíbelo en 5-7 días hábiles.
              </p>
            </div>
            <button
              onClick={() => navigate('/affiliate-payouts')}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold"
            >
              Solicitar Pago
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AffiliateDashboardPage;
