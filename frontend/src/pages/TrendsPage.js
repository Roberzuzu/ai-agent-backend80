import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { TrendingUp, Plus, Sparkles } from 'lucide-react';

function TrendsPage() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    platform: 'youtube',
    topic: '',
    engagement_score: 50,
    keywords: ''
  });
  const [analyzing, setAnalyzing] = useState(null);

  useEffect(() => {
    loadTrends();
  }, []);

  const loadTrends = async () => {
    try {
      const response = await axios.get(`${API}/trends`);
      setTrends(response.data);
    } catch (error) {
      console.error('Error loading trends:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/trends`, {
        ...formData,
        keywords: formData.keywords.split(',').map(k => k.trim())
      });
      setShowForm(false);
      setFormData({ platform: 'youtube', topic: '', engagement_score: 50, keywords: '' });
      loadTrends();
    } catch (error) {
      console.error('Error creating trend:', error);
    }
  };

  const handleAnalyze = async (trendId) => {
    setAnalyzing(trendId);
    try {
      const response = await axios.post(`${API}/trends/${trendId}/analyze`);
      alert('Analysis complete! Check the trend details.');
      loadTrends();
    } catch (error) {
      console.error('Error analyzing trend:', error);
      alert('Error analyzing trend');
    } finally {
      setAnalyzing(null);
    }
  };

  const platformColors = {
    youtube: 'bg-red-100 text-red-700',
    tiktok: 'bg-black text-white',
    instagram: 'bg-pink-100 text-pink-700',
    twitter: 'bg-blue-100 text-blue-700',
    facebook: 'bg-blue-100 text-blue-700'
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><div className="loading-spinner"></div></div>;
  }

  return (
    <div data-testid="trends-page" className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-2">
            <TrendingUp className="w-8 h-8" />
            <span>Growth Hacker</span>
          </h1>
          <p className="text-gray-600 mt-1">Discover and analyze trending topics</p>
        </div>
        <button
          data-testid="add-trend-btn"
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Trend</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Add New Trend</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="input-field"
              >
                <option value="youtube">YouTube</option>
                <option value="tiktok">TikTok</option>
                <option value="instagram">Instagram</option>
                <option value="twitter">Twitter</option>
                <option value="facebook">Facebook</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Topic</label>
              <input
                type="text"
                value={formData.topic}
                onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                className="input-field"
                placeholder="e.g., DIY Home Tools"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Engagement Score (1-100)</label>
              <input
                type="number"
                min="1"
                max="100"
                value={formData.engagement_score}
                onChange={(e) => setFormData({ ...formData, engagement_score: parseInt(e.target.value) })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Keywords (comma-separated)</label>
              <input
                type="text"
                value={formData.keywords}
                onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                className="input-field"
                placeholder="tools, diy, accessories"
                required
              />
            </div>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">Save Trend</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {trends.length === 0 ? (
          <div className="card text-center py-12">
            <TrendingUp className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No trends yet. Add your first trend!</p>
          </div>
        ) : (
          trends.map((trend) => (
            <div key={trend.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className={`badge ${platformColors[trend.platform] || 'badge-info'}`}>
                      {trend.platform}
                    </span>
                    <span className="badge badge-success">Score: {trend.engagement_score}</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{trend.topic}</h3>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {trend.keywords.map((keyword, idx) => (
                      <span key={idx} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                        #{keyword}
                      </span>
                    ))}
                  </div>
                  {trend.analysis && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                      <p className="text-sm text-gray-700 whitespace-pre-wrap">{trend.analysis}</p>
                    </div>
                  )}
                </div>
                <button
                  data-testid={`analyze-trend-${trend.id}`}
                  onClick={() => handleAnalyze(trend.id)}
                  disabled={analyzing === trend.id}
                  className="btn-secondary flex items-center space-x-2 ml-4"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>{analyzing === trend.id ? 'Analyzing...' : 'Analyze'}</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default TrendsPage;