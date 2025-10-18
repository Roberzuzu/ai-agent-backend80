import React, { useState, useEffect } from 'react';
import { Settings, Save, Bell, Mail, Smartphone } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';

function NotificationPreferencesPage() {
  const [preferences, setPreferences] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadPreferences();
    }
  }, [user]);

  const loadPreferences = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get(
        `/notifications/preferences?user_email=${user.email}`
      );
      setPreferences(response.data);
    } catch (error) {
      console.error('Error loading preferences:', error);
      toast.error('Error al cargar preferencias');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axiosInstance.patch(
        `/notifications/preferences?user_email=${user.email}`,
        preferences
      );
      toast.success('Preferencias guardadas correctamente');
    } catch (error) {
      console.error('Error saving preferences:', error);
      toast.error('Error al guardar preferencias');
    } finally {
      setSaving(false);
    }
  };

  const handleToggle = (field) => {
    setPreferences({
      ...preferences,
      [field]: !preferences[field]
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Settings className="w-8 h-8" />
            Preferencias de Notificaciones
          </h1>
          <p className="text-gray-600 mt-1">
            Personaliza cómo y cuándo quieres recibir notificaciones
          </p>
        </div>
        
        <button
          onClick={() => navigate('/notifications')}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Volver
        </button>
      </div>

      {/* General Settings */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Bell className="w-6 h-6 text-blue-600" />
          Configuración General
        </h2>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-semibold text-gray-900">Email Notifications</p>
                <p className="text-sm text-gray-600">
                  Recibe notificaciones importantes por correo electrónico
                </p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={preferences?.email_notifications}
                onChange={() => handleToggle('email_notifications')}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <Smartphone className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-semibold text-gray-900">Push Notifications</p>
                <p className="text-sm text-gray-600">
                  Recibe notificaciones push en tu dispositivo (próximamente)
                </p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={preferences?.push_notifications}
                onChange={() => handleToggle('push_notifications')}
                className="sr-only peer"
                disabled
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600 opacity-50"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18.717-.962 5.156-1.358 6.835-.167.711-.5.948-.822.97-.697.066-1.226-.461-1.902-.903-1.056-.693-1.653-1.124-2.678-1.8-1.185-.781-.417-1.211.258-1.913.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.752-.245-1.349-.374-1.297-.789.027-.216.324-.437.892-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.141.121.099.155.232.171.326.016.094.036.308.02.475z"/>
              </svg>
              <div>
                <p className="font-semibold text-gray-900">Telegram Notifications</p>
                <p className="text-sm text-gray-600">
                  Recibe notificaciones instantáneas en Telegram
                </p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={preferences?.telegram_notifications}
                onChange={() => handleToggle('telegram_notifications')}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      {/* Notification Types */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Tipos de Notificaciones
        </h2>
        <p className="text-gray-600 mb-6">
          Elige qué tipos de notificaciones quieres recibir
        </p>

        <div className="space-y-3">
          {[
            {
              key: 'notify_payments',
              icon: '💰',
              title: 'Pagos y Transacciones',
              description: 'Notificaciones sobre pagos recibidos, reembolsos y transacciones'
            },
            {
              key: 'notify_affiliates',
              icon: '🤝',
              title: 'Programa de Afiliados',
              description: 'Comisiones ganadas, nuevas conversiones y pagos de afiliados'
            },
            {
              key: 'notify_campaigns',
              icon: '📢',
              title: 'Campañas Publicitarias',
              description: 'Estado de campañas, rendimiento y alertas importantes'
            },
            {
              key: 'notify_products',
              icon: '🛍️',
              title: 'Productos y Ventas',
              description: 'Nuevas ventas, productos destacados y actualizaciones de inventario'
            },
            {
              key: 'notify_subscriptions',
              icon: '⭐',
              title: 'Suscripciones',
              description: 'Nuevos suscriptores, renovaciones y cancelaciones'
            },
            {
              key: 'notify_system',
              icon: '🔔',
              title: 'Sistema y Actualizaciones',
              description: 'Actualizaciones del sistema, mantenimiento y anuncios'
            }
          ].map((item) => (
            <div
              key={item.key}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{item.icon}</span>
                <div>
                  <p className="font-semibold text-gray-900">{item.title}</p>
                  <p className="text-sm text-gray-600">{item.description}</p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={preferences?.[item.key]}
                  onChange={() => handleToggle(item.key)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Email Digest */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Resumen por Email
        </h2>
        <p className="text-gray-600 mb-6">
          Recibe un resumen de tus notificaciones por correo electrónico
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          {[
            { value: 'none', label: 'Nunca' },
            { value: 'daily', label: 'Diario' },
            { value: 'weekly', label: 'Semanal' },
            { value: 'monthly', label: 'Mensual' }
          ].map((option) => (
            <button
              key={option.value}
              onClick={() => setPreferences({ ...preferences, email_digest: option.value })}
              className={`p-4 rounded-lg border-2 transition-all ${
                preferences?.email_digest === option.value
                  ? 'border-blue-600 bg-blue-50 text-blue-700 font-semibold'
                  : 'border-gray-200 hover:border-gray-300 text-gray-700'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Save className="w-5 h-5" />
          {saving ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>
    </div>
  );
}

export default NotificationPreferencesPage;
