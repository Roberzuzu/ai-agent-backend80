import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import '@/App.css';
import Dashboard from './pages/Dashboard';
import TrendsPage from './pages/TrendsPage';
import ContentPage from './pages/ContentPage';
import ProductsPage from './pages/ProductsPage';
import SocialPage from './pages/SocialPage';
import CampaignsPage from './pages/CampaignsPage';
import SubscriptionsPage from './pages/SubscriptionsPage';
import PaymentSuccessPage from './pages/PaymentSuccessPage';
import PaymentCancelledPage from './pages/PaymentCancelledPage';
import RevenueAnalyticsPage from './pages/RevenueAnalyticsPage';
import { TrendingUp, Sparkles, DollarSign, Share2, Megaphone, LayoutDashboard, CreditCard, BarChart3 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/trends', icon: TrendingUp, label: 'Growth Hacker' },
    { path: '/content', icon: Sparkles, label: 'Content Creator' },
    { path: '/products', icon: DollarSign, label: 'Monetization' },
    { path: '/social', icon: Share2, label: 'Social Manager' },
    { path: '/campaigns', icon: Megaphone, label: 'Ad Manager' },
    { path: '/subscriptions', icon: CreditCard, label: 'Suscripciones' },
    { path: '/revenue', icon: BarChart3, label: 'Ingresos' }
  ];
  
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <DollarSign className="w-8 h-8" />
            <span className="text-xl font-bold">Monetization Agent</span>
          </div>
          <div className="flex space-x-1">
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
      </div>
    </nav>
  );
}

function App() {
  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/trends" element={<TrendsPage />} />
            <Route path="/content" element={<ContentPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/social" element={<SocialPage />} />
            <Route path="/campaigns" element={<CampaignsPage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;