import React, { useState, useEffect } from 'react';
import { Settings, Save, BarChart3, TrendingUp, Activity, Eye } from 'lucide-react';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';

function AnalyticsConfigPage() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get('/analytics/config');
      setConfig(response.data);
    } catch (error) {
      console.error('Error loading config:', error);
      toast.error('Error al cargar configuración');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axiosInstance.patch('/analytics/config', config);
      toast.success('✅ Configuración guardada correctamente');
    } catch (error) {
      console.error('Error saving config:', error);
      toast.error('Error al guardar configuración');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setConfig({ ...config, [field]: value });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in max-w-5xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Settings className="w-8 h-8 text-blue-600" />
            Configuración de Analytics
          </h1>
          <p className="text-gray-600 mt-1">
            Configura integraciones con Google Analytics, Meta Pixel y Heatmaps
          </p>
        </div>
        
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          <Save className="w-5 h-5" />
          {saving ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>

      {/* Google Analytics 4 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-yellow-100 rounded-lg">
            <BarChart3 className="w-6 h-6 text-yellow-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Google Analytics 4</h2>
            <p className="text-sm text-gray-600">Tracking avanzado con GA4</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="flex items-center gap-2 mb-4">
              <input
                type="checkbox"
                checked={config?.is_ga4_enabled || false}
                onChange={(e) => handleChange('is_ga4_enabled', e.target.checked)}
                className="w-5 h-5 text-blue-600 rounded"
              />
              <span className="font-medium text-gray-900">Habilitar Google Analytics 4</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Measurement ID
            </label>
            <input
              type="text"
              placeholder="G-XXXXXXXXXX"
              value={config?.ga4_measurement_id || ''}
              onChange={(e) => handleChange('ga4_measurement_id', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500 mt-1">
              Encuentra tu Measurement ID en Admin → Data Streams
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Secret (opcional)
            </label>
            <input
              type="text"
              placeholder="Para Measurement Protocol"
              value={config?.ga4_api_secret || ''}
              onChange={(e) => handleChange('ga4_api_secret', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Meta Pixel */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-blue-100 rounded-lg">
            <TrendingUp className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Meta Pixel (Facebook)</h2>
            <p className="text-sm text-gray-600">Tracking de conversiones para Facebook Ads</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="flex items-center gap-2 mb-4">
              <input
                type="checkbox"
                checked={config?.is_meta_pixel_enabled || false}
                onChange={(e) => handleChange('is_meta_pixel_enabled', e.target.checked)}
                className="w-5 h-5 text-blue-600 rounded"
              />
              <span className="font-medium text-gray-900">Habilitar Meta Pixel</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Pixel ID
            </label>
            <input
              type="text"
              placeholder="123456789012345"
              value={config?.meta_pixel_id || ''}
              onChange={(e) => handleChange('meta_pixel_id', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500 mt-1">
              Encuentra tu Pixel ID en Events Manager
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Access Token (opcional)
            </label>
            <input
              type="text"
              placeholder="Para Conversions API"
              value={config?.meta_access_token || ''}
              onChange={(e) => handleChange('meta_access_token', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Heatmaps */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-red-100 rounded-lg">
            <Eye className="w-6 h-6 text-red-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Heatmaps</h2>
            <p className="text-sm text-gray-600">Visualiza el comportamiento de usuarios</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="flex items-center gap-2 mb-4">
              <input
                type="checkbox"
                checked={config?.is_heatmap_enabled || false}
                onChange={(e) => handleChange('is_heatmap_enabled', e.target.checked)}
                className="w-5 h-5 text-red-600 rounded"
              />
              <span className="font-medium text-gray-900">Habilitar Heatmaps</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Proveedor
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => handleChange('heatmap_provider', 'clarity')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  config?.heatmap_provider === 'clarity'
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <h3 className="font-semibold">Microsoft Clarity</h3>
                <p className="text-sm text-gray-600">Gratis y fácil de usar</p>
              </button>
              <button
                onClick={() => handleChange('heatmap_provider', 'hotjar')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  config?.heatmap_provider === 'hotjar'
                    ? 'border-orange-600 bg-orange-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <h3 className="font-semibold">Hotjar</h3>
                <p className="text-sm text-gray-600">Más características</p>
              </button>
            </div>
          </div>

          {config?.heatmap_provider === 'clarity' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Clarity Project ID
              </label>
              <input
                type="text"
                placeholder="abcdefghij"
                value={config?.clarity_project_id || ''}
                onChange={(e) => handleChange('clarity_project_id', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          )}

          {config?.heatmap_provider === 'hotjar' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hotjar Site ID
              </label>
              <input
                type="text"
                placeholder="1234567"
                value={config?.hotjar_site_id || ''}
                onChange={(e) => handleChange('hotjar_site_id', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          )}
        </div>
      </div>

      {/* Status Summary */}
      <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Estado de Integraciones</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Google Analytics 4</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              config?.is_ga4_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'
            }`}>
              {config?.is_ga4_enabled ? '✅ Habilitado' : 'Deshabilitado'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Meta Pixel</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              config?.is_meta_pixel_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'
            }`}>
              {config?.is_meta_pixel_enabled ? '✅ Habilitado' : 'Deshabilitado'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Heatmaps ({config?.heatmap_provider})</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              config?.is_heatmap_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'
            }`}>
              {config?.is_heatmap_enabled ? '✅ Habilitado' : 'Deshabilitado'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsConfigPage;
