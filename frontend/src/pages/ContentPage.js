import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Sparkles, Plus, CheckCircle, Edit } from 'lucide-react';

function ContentPage() {
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [formData, setFormData] = useState({
    platform: 'youtube',
    content_type: 'tutorial',
    keywords: '',
    custom_prompt: ''
  });

  useEffect(() => {
    loadContent();
  }, []);

  const loadContent = async () => {
    try {
      const response = await axios.get(`${API}/content`);
      setContent(response.data);
    } catch (error) {
      console.error('Error loading content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setGenerating(true);
    try {
      await axios.post(`${API}/content/generate`, {
        ...formData,
        keywords: formData.keywords.split(',').map(k => k.trim()),
        custom_prompt: formData.custom_prompt || undefined
      });
      setShowForm(false);
      setFormData({ platform: 'youtube', content_type: 'tutorial', keywords: '', custom_prompt: '' });
      loadContent();
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Error generating content');
    } finally {
      setGenerating(false);
    }
  };

  const updateStatus = async (contentId, newStatus) => {
    try {
      await axios.patch(`${API}/content/${contentId}/status?status=${newStatus}`);
      loadContent();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const statusColors = {
    draft: 'badge-warning',
    approved: 'badge-info',
    published: 'badge-success'
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><div className="loading-spinner"></div></div>;
  }

  return (
    <div data-testid="content-page" className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-2">
            <Sparkles className="w-8 h-8" />
            <span>Content Creator</span>
          </h1>
          <p className="text-gray-600 mt-1">Generate AI-powered content ideas</p>
        </div>
        <button
          data-testid="generate-content-btn"
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Generate Content</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Generate New Content</h3>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
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
                  <option value="facebook">Facebook</option>
                  <option value="twitter">Twitter</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Content Type</label>
                <select
                  value={formData.content_type}
                  onChange={(e) => setFormData({ ...formData, content_type: e.target.value })}
                  className="input-field"
                >
                  <option value="tutorial">Tutorial</option>
                  <option value="review">Product Review</option>
                  <option value="comparison">Comparison</option>
                  <option value="tips">Tips & Tricks</option>
                  <option value="diy">DIY Project</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Keywords (comma-separated)</label>
              <input
                type="text"
                value={formData.keywords}
                onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                className="input-field"
                placeholder="power tools, drill, woodworking"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Custom Prompt (Optional)</label>
              <textarea
                value={formData.custom_prompt}
                onChange={(e) => setFormData({ ...formData, custom_prompt: e.target.value })}
                className="input-field"
                rows="3"
                placeholder="Add specific instructions for content generation..."
              />
            </div>
            <div className="flex space-x-3">
              <button type="submit" disabled={generating} className="btn-primary">
                {generating ? 'Generating...' : 'Generate with AI'}
              </button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {content.length === 0 ? (
          <div className="card text-center py-12">
            <Sparkles className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No content yet. Generate your first content idea!</p>
          </div>
        ) : (
          content.map((item) => (
            <div key={item.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="badge badge-info">{item.platform}</span>
                    <span className="badge badge-warning">{item.content_type}</span>
                    <span className={`badge ${statusColors[item.status]}`}>{item.status}</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-gray-600 mb-3">{item.description}</p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {item.keywords.map((keyword, idx) => (
                      <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                        #{keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              {item.generated_content && (
                <div className="p-4 bg-gray-50 rounded-lg mb-4">
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{item.generated_content}</p>
                </div>
              )}
              <div className="flex space-x-2">
                {item.status === 'draft' && (
                  <button
                    onClick={() => updateStatus(item.id, 'approved')}
                    className="btn-secondary text-sm flex items-center space-x-1"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span>Approve</span>
                  </button>
                )}
                {item.status === 'approved' && (
                  <button
                    onClick={() => updateStatus(item.id, 'published')}
                    className="btn-primary text-sm flex items-center space-x-1"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span>Publish</span>
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

export default ContentPage;