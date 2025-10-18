import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { 
  DollarSign, 
  ShoppingBag, 
  TrendingUp, 
  Users,
  RefreshCw,
  Download
} from 'lucide-react';
import axiosInstance from '../lib/axiosConfig';
import StatCard from '../components/StatCard';
import ChartCard from '../components/ChartCard';
import DateRangeFilter from '../components/DateRangeFilter';
import AffiliateWidget from '../components/widgets/AffiliateWidget';
import CartWidget from '../components/widgets/CartWidget';
import ABTestWidget from '../components/widgets/ABTestWidget';
import EmailWidget from '../components/widgets/EmailWidget';
import { toast } from 'sonner';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function DashboardEnhanced() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedRange, setSelectedRange] = useState(30);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadAnalytics();
  }, [selectedRange]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get(`/analytics/dashboard-enhanced?days=${selectedRange}`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
      toast.error('Error al cargar analytics');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadAnalytics();
    setRefreshing(false);
    toast.success('Dashboard actualizado');
  };

  const handleExport = () => {
    // Simulate export functionality
    toast.info('Exportando datos...');
    setTimeout(() => {
      toast.success('Datos exportados correctamente');
    }, 1500);
  };

  // Chart configurations
  const revenueChartData = {
    labels: analytics?.charts?.revenue_timeline?.map(item => {
      const date = new Date(item.date);
      return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
    }) || [],
    datasets: [
      {
        label: 'Ingresos ($)',
        data: analytics?.charts?.revenue_timeline?.map(item => item.revenue) || [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const revenueChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            return `$${context.parsed.y.toFixed(2)}`;
          }
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '$' + value;
          }
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
  };

  const conversionSourcesData = {
    labels: Object.keys(analytics?.charts?.conversion_sources || {}),
    datasets: [
      {
        data: Object.values(analytics?.charts?.conversion_sources || {}),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(249, 115, 22, 0.8)',
          'rgba(168, 85, 247, 0.8)',
          'rgba(236, 72, 153, 0.8)',
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(16, 185, 129)',
          'rgb(249, 115, 22)',
          'rgb(168, 85, 247)',
          'rgb(236, 72, 153)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const conversionSourcesOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    },
  };

  const campaignPerformanceData = {
    labels: analytics?.charts?.campaign_performance?.map(c => c.name) || [],
    datasets: [
      {
        label: 'Impresiones',
        data: analytics?.charts?.campaign_performance?.map(c => c.impressions) || [],
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
      {
        label: 'Clicks',
        data: analytics?.charts?.campaign_performance?.map(c => c.clicks) || [],
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 1,
      },
      {
        label: 'Conversiones',
        data: analytics?.charts?.campaign_performance?.map(c => c.conversions) || [],
        backgroundColor: 'rgba(249, 115, 22, 0.8)',
        borderColor: 'rgb(249, 115, 22)',
        borderWidth: 1,
      },
    ],
  };

  const campaignPerformanceOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      }
    },
  };

  if (loading && !analytics) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard Avanzado</h1>
          <p className="text-gray-600 mt-1">
            Vista completa de métricas y análisis
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          <DateRangeFilter 
            selectedRange={selectedRange} 
            onRangeChange={setSelectedRange}
          />
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="p-3 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-5 h-5 text-gray-600 ${refreshing ? 'animate-spin' : ''}`} />
          </button>
          <button
            onClick={handleExport}
            className="p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Ingresos Totales"
          value={analytics?.metrics?.revenue?.current || 0}
          icon={DollarSign}
          color="green"
          prefix="$"
          comparison={{
            value: Math.abs(analytics?.metrics?.revenue?.change_percent || 0),
            isPositive: analytics?.metrics?.revenue?.is_positive,
            period: `vs ${selectedRange} días anteriores`
          }}
          loading={loading}
        />
        <StatCard
          title="Transacciones"
          value={analytics?.metrics?.transactions?.current || 0}
          icon={ShoppingBag}
          color="blue"
          comparison={{
            value: Math.abs(analytics?.metrics?.transactions?.change_percent || 0),
            isPositive: analytics?.metrics?.transactions?.change_percent >= 0,
            period: 'vs periodo anterior'
          }}
          loading={loading}
        />
        <StatCard
          title="Productos"
          value={analytics?.metrics?.products?.total || 0}
          icon={TrendingUp}
          color="purple"
          loading={loading}
        />
        <StatCard
          title="Campañas Activas"
          value={analytics?.metrics?.campaigns?.active || 0}
          icon={Users}
          color="orange"
          loading={loading}
        />
      </div>

      {/* Revenue Chart */}
      <ChartCard
        title="Ingresos en el Tiempo"
        description={`Últimos ${selectedRange} días`}
        loading={loading}
        height="300px"
      >
        <Line data={revenueChartData} options={revenueChartOptions} />
      </ChartCard>

      {/* Conversion & Campaign Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Fuentes de Conversión"
          description="Distribución de conversiones por canal"
          loading={loading}
          height="300px"
        >
          <Pie data={conversionSourcesData} options={conversionSourcesOptions} />
        </ChartCard>

        <ChartCard
          title="Performance de Campañas"
          description="Top 5 campañas"
          loading={loading}
          height="300px"
        >
          <Bar data={campaignPerformanceData} options={campaignPerformanceOptions} />
        </ChartCard>
      </div>

      {/* Affiliate Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-gray-900">Programa de Afiliados</h2>
        <AffiliateWidget data={analytics?.metrics?.affiliates} loading={loading} />
      </div>

      {/* Cart Abandonment Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-gray-900">Carritos Abandonados</h2>
        <CartWidget data={analytics?.metrics?.cart_abandonment} loading={loading} />
      </div>

      {/* A/B Testing Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-gray-900">Tests A/B</h2>
        <ABTestWidget data={analytics?.metrics?.ab_tests} loading={loading} />
      </div>

      {/* Email Marketing Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-gray-900">Email Marketing</h2>
        <EmailWidget data={analytics?.metrics?.email_campaigns} loading={loading} />
      </div>

      {/* Footer Info */}
      <div className="text-center text-sm text-gray-500 pt-6 border-t">
        Última actualización: {analytics?.generated_at ? new Date(analytics.generated_at).toLocaleString('es-ES') : 'N/A'}
      </div>
    </div>
  );
}

export default DashboardEnhanced;
