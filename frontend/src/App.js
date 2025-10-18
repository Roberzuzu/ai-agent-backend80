import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';
import '@/App.css';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import ErrorBoundary from './components/ErrorBoundary';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import DashboardEnhanced from './pages/DashboardEnhanced';
import TrendsPage from './pages/TrendsPage';
import ContentPage from './pages/ContentPage';
import ProductsPage from './pages/ProductsPage';
import SocialPage from './pages/SocialPage';
import CampaignsPage from './pages/CampaignsPage';
import SubscriptionsPage from './pages/SubscriptionsPage';
import PaymentSuccessPage from './pages/PaymentSuccessPage';
import PaymentCancelledPage from './pages/PaymentCancelledPage';
import RevenueAnalyticsPage from './pages/RevenueAnalyticsPage';
import AffiliatePage from './pages/AffiliatePage';
import AffiliateDashboardPage from './pages/AffiliateDashboardPage';
import AffiliatePayoutsPage from './pages/AffiliatePayoutsPage';
import AdvancedMonetizationPage from './pages/AdvancedMonetizationPage';
import ConversionOptimizationPage from './pages/ConversionOptimizationPage';
import WebhookMonitorPage from './pages/WebhookMonitorPage';
import { TrendingUp, Sparkles, DollarSign, Share2, Megaphone, LayoutDashboard, CreditCard, BarChart3, Users, Zap, Target, LogOut, User, Activity, Gauge } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

function Navigation() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/dashboard-enhanced', icon: Gauge, label: 'Analytics' },
    { path: '/trends', icon: TrendingUp, label: 'Growth Hacker' },
    { path: '/content', icon: Sparkles, label: 'Content Creator' },
    { path: '/products', icon: DollarSign, label: 'Monetization' },
    { path: '/social', icon: Share2, label: 'Social Manager' },
    { path: '/campaigns', icon: Megaphone, label: 'Ad Manager' },
    { path: '/subscriptions', icon: CreditCard, label: 'Suscripciones' },
    { path: '/revenue', icon: BarChart3, label: 'Ingresos' },
    { path: '/affiliate', icon: Users, label: 'Afiliados' },
    { path: '/advanced', icon: Zap, label: 'Avanzado' },
    { path: '/conversion', icon: Target, label: 'Conversión' }
  ];

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2">
              <DollarSign className="w-8 h-8" />
              <span className="text-xl font-bold">Monetization Agent</span>
            </div>
            
            <div className="hidden md:flex space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                      isActive
                        ? 'bg-white text-blue-600 shadow-md'
                        : 'hover:bg-white/10'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
            >
              <div className="bg-white/20 w-8 h-8 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <div className="hidden md:block text-left">
                <p className="text-sm font-medium text-white">{user?.full_name}</p>
                <p className="text-xs text-white/70 capitalize">{user?.role}</p>
              </div>
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                <div className="px-4 py-2 border-b border-gray-200">
                  <p className="text-sm font-medium text-gray-900">{user?.email}</p>
                </div>
                <button
                  onClick={() => {
                    logout();
                    setShowUserMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Cerrar Sesión
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <div className="App min-h-screen bg-gray-50">
        <Toaster 
          position="top-right" 
          expand={false}
          richColors
          closeButton
          duration={4000}
        />
        <BrowserRouter>
          <Navigation />
          <main className="max-w-7xl mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard-enhanced" element={<DashboardEnhanced />} />
              <Route path="/trends" element={<TrendsPage />} />
              <Route path="/content" element={<ContentPage />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/social" element={<SocialPage />} />
              <Route path="/campaigns" element={<CampaignsPage />} />
              <Route path="/subscriptions" element={<SubscriptionsPage />} />
              <Route path="/revenue" element={<RevenueAnalyticsPage />} />
              <Route path="/affiliate" element={<AffiliatePage />} />
              <Route path="/affiliate-dashboard" element={<AffiliateDashboardPage />} />
              <Route path="/affiliate-payouts" element={<AffiliatePayoutsPage />} />
              <Route path="/advanced" element={<AdvancedMonetizationPage />} />
              <Route path="/conversion" element={<ConversionOptimizationPage />} />
              <Route path="/payment-success" element={<PaymentSuccessPage />} />
              <Route path="/payment-cancelled" element={<PaymentCancelledPage />} />
            </Routes>
          </main>
        </BrowserRouter>
      </div>
    </ErrorBoundary>
  );
}

export default App;