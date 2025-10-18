import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, Eye, ShoppingCart, ExternalLink } from 'lucide-react';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';

const RecommendationsWidget = ({ 
  limit = 6, 
  algorithm = "hybrid",
  category = null,
  title = "Recomendado para ti"
}) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadRecommendations();
    }
  }, [user, algorithm, category]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.post('/recommendations', {
        user_email: user.email,
        limit: limit,
        algorithm: algorithm,
        exclude_purchased: true,
        category: category
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const trackInteraction = async (productId, interactionType) => {
    try {
      await axiosInstance.post('/recommendations/track', null, {
        params: {
          user_email: user.email,
          product_id: productId,
          interaction_type: interactionType
        }
      });
    } catch (error) {
      console.error('Error tracking interaction:', error);
    }
  };

  const handleProductView = (productId) => {
    trackInteraction(productId, 'view');
  };

  const handleProductClick = (productId) => {
    trackInteraction(productId, 'click');
  };

  const getAlgorithmIcon = (algorithm) => {
    const iconMap = {
      similarity: <Sparkles className="w-4 h-4" />,
      collaborative: <TrendingUp className="w-4 h-4" />,
      popular: <Eye className="w-4 h-4" />,
      hybrid: <Sparkles className="w-4 h-4" />
    };
    return iconMap[algorithm] || <Sparkles className="w-4 h-4" />;
  };

  const getAlgorithmColor = (algorithm) => {
    const colorMap = {
      similarity: 'text-purple-600 bg-purple-100',
      collaborative: 'text-blue-600 bg-blue-100',
      popular: 'text-orange-600 bg-orange-100',
      hybrid: 'text-pink-600 bg-pink-100'
    };
    return colorMap[algorithm] || 'text-gray-600 bg-gray-100';
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-gray-200 h-48 rounded-lg mb-3"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        </div>
        <div className="text-center py-8 text-gray-500">
          <Sparkles className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No hay recomendaciones disponibles aún</p>
          <p className="text-sm mt-2">Explora productos para recibir recomendaciones personalizadas</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        </div>
        <span className="text-sm text-gray-500">
          Basado en IA
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((rec) => (
          <div
            key={rec.product_id}
            className="group relative bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer"
            onMouseEnter={() => handleProductView(rec.product_id)}
            onClick={() => handleProductClick(rec.product_id)}
          >
            {/* Badge */}
            <div className="absolute top-2 right-2 z-10">
              <span className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getAlgorithmColor(rec.algorithm_used)}`}>
                {getAlgorithmIcon(rec.algorithm_used)}
                AI
              </span>
            </div>

            {/* Image */}
            <div className="relative h-48 bg-gray-100">
              {rec.product_image ? (
                <img
                  src={rec.product_image}
                  alt={rec.product_name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <ShoppingCart className="w-12 h-12 text-gray-300" />
                </div>
              )}
            </div>

            {/* Content */}
            <div className="p-4">
              <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-purple-600 transition-colors">
                {rec.product_name}
              </h3>
              
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {rec.product_description}
              </p>

              {/* Reason */}
              <div className="flex items-center gap-1 text-xs text-purple-600 mb-3">
                <Sparkles className="w-3 h-3" />
                <span>{rec.reason}</span>
              </div>

              {/* Footer */}
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-2xl font-bold text-gray-900">
                    ${rec.product_price.toFixed(2)}
                  </span>
                  <div className="text-xs text-gray-500 mt-1">
                    {rec.product_category}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleProductClick(rec.product_id);
                    toast.success('Producto agregado a carrito');
                  }}
                  className="flex items-center gap-1 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
                >
                  <ShoppingCart className="w-4 h-4" />
                  Ver
                </button>
              </div>

              {/* Score (for debugging) */}
              {process.env.NODE_ENV === 'development' && (
                <div className="mt-2 text-xs text-gray-400">
                  Score: {(rec.score * 100).toFixed(1)}%
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationsWidget;
