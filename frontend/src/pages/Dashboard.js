import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { TrendingUp, FileText, Package, MessageSquare, Target, ArrowUp } from 'lucide-react';

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/analytics/dashboard`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  const statCards = [
    { label: 'Trends', value: analytics?.totals.trends || 0, icon: TrendingUp, color: 'blue' },
    { label: 'Content Ideas', value: analytics?.totals.content || 0, icon: FileText, color: 'purple' },
    { label: 'Products', value: analytics?.totals.products || 0, icon: Package, color: 'green' },
    { label: 'Social Posts', value: analytics?.totals.posts || 0, icon: MessageSquare, color: 'pink' },
    { label: 'Campaigns', value: analytics?.totals.campaigns || 0, icon: Target, color: 'orange' },
  ];

  const colorClasses = {
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    green: 'bg-green-500',
    pink: 'bg-pink-500',
    orange: 'bg-orange-500',
  };

  return (
    <div data-testid="dashboard-page" className="space-y-8 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Social Media Monetization Agent</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} data-testid={`stat-${stat.label.toLowerCase().replace(' ', '-')}`} className="stat-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${colorClasses[stat.color]} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Active Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="bg-green-100 p-3 rounded-lg">
              <ArrowUp className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-gray-600 text-sm">Published Posts</p>
              <p className="text-2xl font-bold text-gray-900">{analytics?.stats.published_posts || 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="bg-purple-100 p-3 rounded-lg">
              <Target className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-gray-600 text-sm">Active Campaigns</p>
              <p className="text-2xl font-bold text-gray-900">{analytics?.stats.active_campaigns || 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="bg-yellow-100 p-3 rounded-lg">
              <Package className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-gray-600 text-sm">Featured Products</p>
              <p className="text-2xl font-bold text-gray-900">{analytics?.stats.featured_products || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Trends */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Trends</h3>
          <div className="space-y-3">
            {analytics?.recent_trends && analytics.recent_trends.length > 0 ? (
              analytics.recent_trends.map((trend, index) => (
                <div key={index} className="trend-item">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-900">{trend.topic}</p>
                      <p className="text-sm text-gray-600">{trend.platform}</p>
                    </div>
                    <span className="badge badge-info">Score: {trend.engagement_score}</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No trends yet</p>
            )}
          </div>
        </div>

        {/* Top Posts */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Top Performing Posts</h3>
          <div className="space-y-3">
            {analytics?.top_posts && analytics.top_posts.length > 0 ? (
              analytics.top_posts.map((post, index) => (
                <div key={index} className="trend-item">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{post.platform}</p>
                      <p className="text-sm text-gray-600 truncate">{post.content.substring(0, 50)}...</p>
                    </div>
                    <span className="badge badge-success ml-2">❤️ {post.engagement?.likes || 0}</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No published posts yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;