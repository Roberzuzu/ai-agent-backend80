import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Megaphone, Plus, DollarSign, TrendingUp } from 'lucide-react';

function CampaignsPage() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    budget: 0,
    platform: 'facebook',
    start_date: '',
    end_date: ''
  });

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const response = await axios.get(`${API}/campaigns`);
      setCampaigns(response.data);
    } catch (error) {
      console.error('Error loading campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/campaigns`, {
        ...formData,
        budget: parseFloat(formData.budget),
        start_date: new Date(formData.start_date).toISOString(),
        end_date: new Date(formData.end_date).toISOString()
      });
      setShowForm(false);
      setFormData({
        name: '',
        description: '',
        budget: 0,
        platform: 'facebook',
        start_date: '',
        end_date: ''
      });
      loadCampaigns();
    } catch (error) {
      console.error('Error creating campaign:', error);
    }
  };

  const updateStatus = async (campaignId, newStatus) => {
    try {
      await axios.patch(`${API}/campaigns/${campaignId}/status?status=${newStatus}`);
      loadCampaigns();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const statusColors = {
    active: 'badge-success',
    paused: 'badge-warning',
    completed: 'badge-info'
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><div className="loading-spinner"></div></div>;
  }

  return (
    <div data-testid="campaigns-page" className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-2">
            <Megaphone className="w-8 h-8" />
            <span>Ad Manager</span>
          </h1>
          <p className="text-gray-600 mt-1">Manage advertising campaigns</p>
        </div>
        <button
          data-testid="create-campaign-btn"
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Create Campaign</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Create New Campaign</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
                <select
                  value={formData.platform}
                  onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                  className="input-field"
                >
                  <option value="facebook">Facebook Ads</option>
                  <option value="instagram">Instagram Ads</option>
                  <option value="google">Google Ads</option>
                  <option value="tiktok">TikTok Ads</option>
                  <option value="youtube">YouTube Ads</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="input-field"
                rows="3"
                required
              />
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Budget ($)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.budget}
                  onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
            </div>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">Create Campaign</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {campaigns.length === 0 ? (
          <div className="card text-center py-12">
            <Megaphone className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No campaigns yet. Create your first campaign!</p>
          </div>
        ) : (
          campaigns.map((campaign) => (
            <div key={campaign.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="badge badge-info">{campaign.platform}</span>
                    <span className={`badge ${statusColors[campaign.status]}`}>{campaign.status}</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{campaign.name}</h3>
                  <p className="text-gray-600 mb-3">{campaign.description}</p>
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-2">
                      <DollarSign className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-gray-600">Budget: <strong>${campaign.budget}</strong></span>
                    </div>
                    <div className="text-sm text-gray-600">
                      {new Date(campaign.start_date).toLocaleDateString()} - {new Date(campaign.end_date).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>
              
              {campaign.performance && Object.keys(campaign.performance).length > 0 && (
                <div className="grid grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg mb-4">
                  <div>
                    <p className="text-sm text-gray-600">Impressions</p>
                    <p className="text-xl font-bold text-gray-900">{campaign.performance.impressions || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Clicks</p>
                    <p className="text-xl font-bold text-gray-900">{campaign.performance.clicks || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Conversions</p>
                    <p className="text-xl font-bold text-gray-900">{campaign.performance.conversions || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Spend</p>
                    <p className="text-xl font-bold text-green-600">${campaign.performance.spend || 0}</p>
                  </div>
                </div>
              )}
              
              <div className="flex space-x-2">
                {campaign.status === 'active' && (
                  <button
                    onClick={() => updateStatus(campaign.id, 'paused')}
                    className="btn-secondary text-sm"
                  >
                    Pause
                  </button>
                )}
                {campaign.status === 'paused' && (
                  <button
                    onClick={() => updateStatus(campaign.id, 'active')}
                    className="btn-primary text-sm"
                  >
                    Resume
                  </button>
                )}
                {(campaign.status === 'active' || campaign.status === 'paused') && (
                  <button
                    onClick={() => updateStatus(campaign.id, 'completed')}
                    className="btn-secondary text-sm"
                  >
                    Complete
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default CampaignsPage;