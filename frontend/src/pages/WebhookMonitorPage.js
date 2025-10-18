import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, CheckCircle, XCircle, RefreshCw, Loader2, AlertCircle, Clock } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

const WebhookMonitorPage = () => {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retrying, setRetrying] = useState(null);
  const [filter, setFilter] = useState('all'); // all, failed, processed

  useEffect(() => {
    fetchData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [filter]);

  const fetchData = async () => {
    try {
      const [logsRes, statsRes] = await Promise.all([
        axios.get(`${BACKEND_URL}/api/webhooks/logs${filter !== 'all' ? `?status=${filter}` : ''}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }),
        axios.get(`${BACKEND_URL}/api/webhooks/stats`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
      ]);
      
      setLogs(logsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching webhook data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = async (eventId) => {
    setRetrying(eventId);
    try {
      await axios.post(
        `${BACKEND_URL}/api/webhooks/${eventId}/retry`,
        {},
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      alert('Webhook retried successfully!');
      fetchData();
    } catch (error) {
      alert(`Retry failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setRetrying(null);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-600" />;
      case 'retrying':
        return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'retrying':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
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
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🔔 Monitor de Webhooks
          </h1>
          <p className="text-gray-600">
            Monitoreo en tiempo real de eventos de Stripe
          </p>
        </div>
        <button
          onClick={() => fetchData()}
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <RefreshCw className="w-5 h-5" />
          <span>Actualizar</span>
        </button>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold mb-1">{stats.total_webhooks}</h3>
            <p className="text-blue-100 text-sm">Total Webhooks</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <CheckCircle className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold mb-1">{stats.success_rate}%</h3>
            <p className="text-green-100 text-sm">Tasa de Éxito</p>
          </div>

          <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <XCircle className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold mb-1">{stats.failed_count}</h3>
            <p className="text-red-100 text-sm">Fallidos</p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-8 h-8" />
            </div>
            <h3 className="text-3xl font-bold mb-1">
              {Object.keys(stats.by_type).length}
            </h3>
            <p className="text-purple-100 text-sm">Tipos de Eventos</p>
          </div>
        </div>
      )}

      {/* Event Type Distribution */}
      {stats && (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Distribución por Tipo</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(stats.by_type).map(([type, count]) => (
              <div key={type} className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600 truncate" title={type}>{type}</p>
                <p className="text-2xl font-bold text-gray-900">{count}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
        <div className="border-b border-gray-200">
          <div className="flex">
            {['all', 'processed', 'failed'].map((filterOption) => (
              <button
                key={filterOption}
                onClick={() => setFilter(filterOption)}
                className={`px-6 py-3 font-medium transition-colors ${
                  filter === filterOption
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                {filterOption === 'all' ? 'Todos' : filterOption === 'processed' ? 'Procesados' : 'Fallidos'}
              </button>
            ))}
          </div>
        </div>

        {/* Webhook Logs Table */}
        <div className="overflow-x-auto">
          {logs.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <Activity className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p>No hay webhooks registrados</p>
            </div>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo de Evento</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Event ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reintentos</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Recibido</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Procesado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(log.status)}
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(log.status)}`}>
                          {log.status}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900 font-mono">{log.event_type}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-600 font-mono">{log.event_id}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{log.retry_count}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {log.processed_at ? new Date(log.processed_at).toLocaleString() : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {log.status === 'failed' && (
                        <button
                          onClick={() => handleRetry(log.event_id)}
                          disabled={retrying === log.event_id}
                          className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center space-x-1 disabled:opacity-50"
                        >
                          {retrying === log.event_id ? (
                            <>
                              <Loader2 className="w-4 h-4 animate-spin" />
                              <span>Reintentando...</span>
                            </>
                          ) : (
                            <>
                              <RefreshCw className="w-4 h-4" />
                              <span>Reintentar</span>
                            </>
                          )}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Info Alert */}
      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
        <div className="flex items-start">
          <AlertCircle className="w-6 h-6 text-blue-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-blue-900 mb-2">Configuración de Webhooks</h3>
            <p className="text-blue-800 text-sm mb-2">
              Para configurar los webhooks de Stripe, sigue estos pasos:
            </p>
            <ol className="text-sm text-blue-700 space-y-1 list-decimal list-inside">
              <li>Ve a tu Stripe Dashboard → Webhooks</li>
              <li>Agrega el endpoint: <code className="bg-blue-100 px-2 py-1 rounded">{window.location.origin}/api/webhook/stripe</code></li>
              <li>Copia el webhook secret y agrégalo al archivo .env</li>
              <li>Selecciona los eventos que quieres recibir</li>
            </ol>
            <p className="text-sm text-blue-700 mt-2">
              Para más detalles, consulta <strong>STRIPE_WEBHOOKS_CONFIG.md</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebhookMonitorPage;
