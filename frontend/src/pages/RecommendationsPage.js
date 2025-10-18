import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  TrendingUp, 
  Users, 
  Eye,
  MousePointer,
  ShoppingBag,
  BarChart3,
  Settings,
  RefreshCw
} from 'lucide-react';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import RecommendationsWidget from '../components/RecommendationsWidget';

function RecommendationsPage() {
  const [stats, setStats] = useState({
    total_interactions: 0,
    unique_users: 0,
    views: 0,
    clicks: 0,
    purchases: 0,
    click_through_rate: 0
  });
  const [algorithm, setAlgorithm] = useState('hybrid');
  const [generating, setGenerating] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      // Simulate stats for now
      // In production, create an endpoint to get these stats
      setStats({
        total_interactions: 1234,
        unique_users: 156,
        views: 890,
        clicks: 234,
        purchases: 45,
        click_through_rate: 26.3
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleGenerateEmbeddings = async () => {
    try {
      setGenerating(true);
      toast.info('Generando embeddings para todos los productos...');
      
      const response = await axiosInstance.post('/recommendations/generate-embeddings');
      
      toast.success(`✅ ${response.data.generated} embeddings generados, ${response.data.skipped} ya existían`);
    } catch (error) {
      console.error('Error generating embeddings:', error);
      toast.error('Error al generar embeddings');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-purple-600" />
            Recomendaciones IA
          </h1>
          <p className="text-gray-600 mt-1">
            Sistema avanzado de recomendaciones con Machine Learning
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={handleGenerateEmbeddings}
            disabled={generating}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${generating ? 'animate-spin' : ''}`} />
            {generating ? 'Generando...' : 'Generar Embeddings'}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <BarChart3 className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">{stats.total_interactions.toLocaleString()}</h3>
          <p className="text-purple-100 text-sm">Interacciones Totales</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <Users className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">{stats.unique_users.toLocaleString()}</h3>
          <p className="text-blue-100 text-sm">Usuarios Únicos</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <MousePointer className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">{stats.clicks.toLocaleString()}</h3>
          <p className="text-green-100 text-sm">Clicks en Recomendaciones</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-bold mb-1">{stats.click_through_rate}%</h3>
          <p className="text-orange-100 text-sm">Click Through Rate</p>
        </div>
      </div>

      {/* Algorithm Selector */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Algoritmo de Recomendación</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button
            onClick={() => setAlgorithm('hybrid')}
            className={`p-4 rounded-lg border-2 transition-all ${
              algorithm === 'hybrid'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Sparkles className={`w-6 h-6 mb-2 ${
              algorithm === 'hybrid' ? 'text-purple-600' : 'text-gray-400'
            }`} />
            <h3 className="font-semibold mb-1">Híbrido</h3>
            <p className="text-sm text-gray-600">
              Combina similarity y collaborative filtering
            </p>
          </button>

          <button
            onClick={() => setAlgorithm('similarity')}
            className={`p-4 rounded-lg border-2 transition-all ${
              algorithm === 'similarity'
                ? 'border-blue-600 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Sparkles className={`w-6 h-6 mb-2 ${
              algorithm === 'similarity' ? 'text-blue-600' : 'text-gray-400'
            }`} />
            <h3 className="font-semibold mb-1">Similarity</h3>
            <p className="text-sm text-gray-600">
              Basado en OpenAI embeddings
            </p>
          </button>

          <button
            onClick={() => setAlgorithm('collaborative')}
            className={`p-4 rounded-lg border-2 transition-all ${
              algorithm === 'collaborative'
                ? 'border-green-600 bg-green-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Users className={`w-6 h-6 mb-2 ${
              algorithm === 'collaborative' ? 'text-green-600' : 'text-gray-400'
            }`} />
            <h3 className="font-semibold mb-1">Collaborative</h3>
            <p className="text-sm text-gray-600">
              Basado en usuarios similares
            </p>
          </button>

          <button
            onClick={() => setAlgorithm('popular')}
            className={`p-4 rounded-lg border-2 transition-all ${
              algorithm === 'popular'
                ? 'border-orange-600 bg-orange-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <TrendingUp className={`w-6 h-6 mb-2 ${
              algorithm === 'popular' ? 'text-orange-600' : 'text-gray-400'
            }`} />
            <h3 className="font-semibold mb-1">Popular</h3>
            <p className="text-sm text-gray-600">
              Productos más populares
            </p>
          </button>
        </div>
      </div>

      {/* Recommendations */}
      <RecommendationsWidget 
        algorithm={algorithm}
        limit={6}
        title={`Recomendaciones (Algoritmo: ${algorithm})`}
      />

      {/* How It Works */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">¿Cómo Funciona?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-4 bg-purple-50 rounded-lg">
            <Sparkles className="w-8 h-8 text-purple-600 mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">1. OpenAI Embeddings</h3>
            <p className="text-sm text-gray-600">
              Cada producto se convierte en un vector de 1536 dimensiones usando text-embedding-ada-002.
              Esto permite encontrar productos similares basándose en su descripción y características.
            </p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <Users className="w-8 h-8 text-blue-600 mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">2. Collaborative Filtering</h3>
            <p className="text-sm text-gray-600">
              Analiza el comportamiento de usuarios similares. Si un usuario compra productos que tú
              también compraste, es probable que te gusten sus otras compras.
            </p>
          </div>

          <div className="p-4 bg-green-50 rounded-lg">
            <TrendingUp className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">3. Feedback Loop</h3>
            <p className="text-sm text-gray-600">
              Cada interacción (views, clicks, compras) se registra con diferentes pesos.
              El sistema aprende de tus preferencias en tiempo real.
            </p>
          </div>
        </div>
      </div>

      {/* Interaction Weights */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Pesos de Interacción</h2>
        <div className="space-y-3">
          {[
            { type: 'View', score: 0.5, color: 'bg-blue-500' },
            { type: 'Click', score: 1.0, color: 'bg-purple-500' },
            { type: 'Wishlist', score: 1.5, color: 'bg-pink-500' },
            { type: 'Add to Cart', score: 2.0, color: 'bg-orange-500' },
            { type: 'Purchase', score: 5.0, color: 'bg-green-500' }
          ].map((item) => (
            <div key={item.type} className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${item.color}`}></div>
                <span className="font-medium text-gray-900">{item.type}</span>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-48 bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${item.color}`}
                    style={{ width: `${(item.score / 5) * 100}%` }}
                  ></div>
                </div>
                <span className="font-semibold text-gray-700 w-12 text-right">
                  {item.score}x
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RecommendationsPage;
