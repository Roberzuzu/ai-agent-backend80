import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API } from '../App';
import { 
  Store, 
  Package, 
  DollarSign, 
  TrendingUp, 
  RefreshCw, 
  Zap,
  Image as ImageIcon,
  Video,
  ShoppingCart,
  AlertCircle,
  CheckCircle,
  Loader,
  ExternalLink,
  Settings
} from 'lucide-react';
import { toast } from 'sonner';

function WooCommercePage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [stats, setStats] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [generatingContent, setGeneratingContent] = useState({});

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/woocommerce/products`);
      setProducts(response.data.products || []);
      
      // Calculate basic stats
      const validPriceProducts = response.data.products.filter(p => 
        p.price && p.price !== '0' && p.price !== ''
      );
      const noPriceProducts = response.data.products.filter(p => 
        !p.price || p.price === '0' || p.price === ''
      );
      
      setStats({
        total: response.data.products.length,
        with_price: validPriceProducts.length,
        without_price: noPriceProducts.length,
        featured: response.data.products.filter(p => p.featured).length
      });
      
      toast.success(`${response.data.products.length} productos cargados`);
    } catch (error) {
      console.error('Error loading products:', error);
      toast.error('Error al cargar productos de WooCommerce');
    } finally {
      setLoading(false);
    }
  };

  const calculatePrice = async (supplierPrice) => {
    try {
      const response = await axios.post(`${API}/dropshipping/calculate-price`, {
        supplier_price: parseFloat(supplierPrice),
        currency: 'EUR'
      });
      return response.data;
    } catch (error) {
      console.error('Error calculating price:', error);
      return null;
    }
  };

  const updateProductPrice = async (productId, price) => {
    try {
      await axios.put(`${API}/woocommerce/products/${productId}/price`, {
        regular_price: price.toString()
      });
      toast.success('Precio actualizado correctamente');
      loadProducts();
    } catch (error) {
      console.error('Error updating price:', error);
      toast.error('Error al actualizar precio');
    }
  };

  const processProduct = async (productId) => {
    try {
      setProcessing(true);
      toast.info('Procesando producto...');
      
      const response = await axios.post(
        `${API}/dropshipping/process-product/${productId}`,
        {
          supplier_price: 25.0, // Default, se puede ajustar
          generate_content: false
        }
      );
      
      toast.success('Producto procesado exitosamente');
      loadProducts();
    } catch (error) {
      console.error('Error processing product:', error);
      toast.error('Error al procesar producto');
    } finally {
      setProcessing(false);
    }
  };

  const processAllProducts = async () => {
    if (!window.confirm('¿Procesar todos los productos? Esto puede tomar varios minutos.')) {
      return;
    }
    
    try {
      setProcessing(true);
      toast.info('Procesando todos los productos...');
      
      const response = await axios.post(
        `${API}/dropshipping/process-all?generate_content=false`
      );
      
      toast.success(`${response.data.processed} productos procesados`);
      loadProducts();
    } catch (error) {
      console.error('Error processing all products:', error);
      toast.error('Error al procesar productos');
    } finally {
      setProcessing(false);
    }
  };

  const generateContent = async (productId) => {
    try {
      setGeneratingContent(prev => ({ ...prev, [productId]: true }));
      toast.info('Generando contenido con IA...');
      
      const response = await axios.post(
        `${API}/dropshipping/generate-content/${productId}`
      );
      
      toast.success('Contenido generado exitosamente');
      loadProducts();
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Error al generar contenido');
    } finally {
      setGeneratingContent(prev => ({ ...prev, [productId]: false }));
    }
  };

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{label}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  const ProductCard = ({ product }) => {
    const hasPrice = product.price && product.price !== '0' && product.price !== '';
    const isGenerating = generatingContent[product.id];
    
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
        {/* Product Image */}
        <div className="relative h-48 bg-gray-100 dark:bg-gray-700 rounded-lg mb-4 overflow-hidden">
          {product.images && product.images[0] ? (
            <img 
              src={product.images[0].src} 
              alt={product.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Package className="w-12 h-12 text-gray-400" />
            </div>
          )}
          {product.featured && (
            <div className="absolute top-2 right-2 bg-yellow-500 text-white text-xs px-2 py-1 rounded">
              Destacado
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="space-y-3">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white line-clamp-2 min-h-[3rem]">
              {product.name || 'Sin nombre'}
            </h3>
            <a 
              href={product.permalink} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1 mt-1"
            >
              Ver en tienda <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          {/* Price Status */}
          <div className="flex items-center justify-between">
            {hasPrice ? (
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-lg font-bold text-green-600">
                  €{parseFloat(product.price).toFixed(2)}
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-orange-500" />
                <span className="text-sm text-orange-600">Sin precio</span>
              </div>
            )}
            <span className="text-xs text-gray-500">ID: {product.id}</span>
          </div>

          {/* Actions */}
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => processProduct(product.id)}
              disabled={processing || isGenerating}
              className="px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white text-sm rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              <Zap className="w-4 h-4" />
              Procesar
            </button>
            <button
              onClick={() => generateContent(product.id)}
              disabled={processing || isGenerating}
              className="px-3 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white text-sm rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              {isGenerating ? (
                <Loader className="w-4 h-4 animate-spin" />
              ) : (
                <ImageIcon className="w-4 h-4" />
              )}
              IA
            </button>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Loader className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Cargando productos de WooCommerce...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <Store className="w-8 h-8" />
            WooCommerce Manager
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Gestiona tu tienda herramientasyaccesorios.store
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={loadProducts}
            disabled={loading || processing}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Recargar
          </button>
          <button
            onClick={processAllProducts}
            disabled={processing}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-lg flex items-center gap-2 transition-all"
          >
            {processing ? (
              <Loader className="w-4 h-4 animate-spin" />
            ) : (
              <Zap className="w-4 h-4" />
            )}
            Procesar Todo
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatCard
            icon={Package}
            label="Total Productos"
            value={stats.total}
            color="bg-blue-500"
          />
          <StatCard
            icon={CheckCircle}
            label="Con Precio"
            value={stats.with_price}
            color="bg-green-500"
          />
          <StatCard
            icon={AlertCircle}
            label="Sin Precio"
            value={stats.without_price}
            color="bg-orange-500"
          />
          <StatCard
            icon={TrendingUp}
            label="Destacados"
            value={stats.featured}
            color="bg-purple-500"
          />
        </div>
      )}

      {/* Info Banner */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <Settings className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-blue-900 dark:text-blue-100">
              Sistema de Dropshipping Automatizado Activo
            </h3>
            <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
              • <strong>Procesar:</strong> Calcula precio óptimo con margen del 50% y actualiza en WooCommerce
              <br />
              • <strong>IA:</strong> Genera imágenes profesionales y videos demostrativos con FAL AI Wan 2.5
              <br />
              • <strong>Procesar Todo:</strong> Optimiza todos los productos de una vez
            </p>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Productos ({products.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>

      {products.length === 0 && (
        <div className="text-center py-12">
          <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            No hay productos
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Importa productos desde SharkDropship para comenzar
          </p>
        </div>
      )}
    </div>
  );
}

export default WooCommercePage;
