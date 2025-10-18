import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Share2, Plus, Calendar, CheckCircle } from 'lucide-react';

function SocialPage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    platform: 'instagram',
    content: '',
    media_urls: '',
    scheduled_time: ''
  });

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const response = await axios.get(`${API}/social/posts`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/social/posts`, {
        ...formData,
        media_urls: formData.media_urls ? formData.media_urls.split(',').map(u => u.trim()) : [],
        scheduled_time: formData.scheduled_time || undefined
      });
      setShowForm(false);
      setFormData({ platform: 'instagram', content: '', media_urls: '', scheduled_time: '' });
      loadPosts();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const updateStatus = async (postId, newStatus) => {
    try {
      await axios.patch(`${API}/social/posts/${postId}/status?status=${newStatus}`);
      loadPosts();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const platformColors = {
    instagram: 'bg-pink-500',
    tiktok: 'bg-black',
    youtube: 'bg-red-500',
    facebook: 'bg-blue-600',
    twitter: 'bg-blue-400'
  };

  const statusColors = {
    pending: 'badge-warning',
    scheduled: 'badge-info',
    published: 'badge-success',
    failed: 'badge-danger'
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><div className="loading-spinner"></div></div>;
  }

  return (
    <div data-testid="social-page" className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-2">
            <Share2 className="w-8 h-8" />
            <span>Social Manager</span>
          </h1>
          <p className="text-gray-600 mt-1">Schedule and manage social media posts</p>
        </div>
        <button
          data-testid="create-post-btn"
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Create Post</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Create Social Post</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="input-field"
              >
                <option value="instagram">Instagram</option>
                <option value="tiktok">TikTok</option>
                <option value="youtube">YouTube</option>
                <option value="facebook">Facebook</option>
                <option value="twitter">Twitter</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Content</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                className="input-field"
                rows="4"
                placeholder="Write your post content..."
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Media URLs (comma-separated)</label>
              <input
                type="text"
                value={formData.media_urls}
                onChange={(e) => setFormData({ ...formData, media_urls: e.target.value })}
                className="input-field"
                placeholder="https://image1.jpg, https://image2.jpg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Schedule Time (Optional)</label>
              <input
                type="datetime-local"
                value={formData.scheduled_time}
                onChange={(e) => setFormData({ ...formData, scheduled_time: e.target.value })}
                className="input-field"
              />
            </div>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">Create Post</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {posts.length === 0 ? (
          <div className="card text-center py-12">
            <Share2 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No posts yet. Create your first post!</p>
          </div>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className={`${platformColors[post.platform]} p-3 rounded-lg`}>
                    <Share2 className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{post.platform}</h3>
                    <span className={`badge ${statusColors[post.status]}`}>{post.status}</span>
                  </div>
                </div>
                {post.scheduled_time && (
                  <div className="flex items-center space-x-2 text-gray-600">
                    <Calendar className="w-4 h-4" />
                    <span className="text-sm">{new Date(post.scheduled_time).toLocaleString()}</span>
                  </div>
                )}
              </div>
              <p className="text-gray-700 mb-4 whitespace-pre-wrap">{post.content}</p>
              {post.media_urls && post.media_urls.length > 0 && (
                <div className="flex space-x-2 mb-4 overflow-x-auto">
                  {post.media_urls.map((url, idx) => (
                    <img
                      key={idx}
                      src={url}
                      alt={`Media ${idx + 1}`}
                      className="w-32 h-32 object-cover rounded"
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                  ))}
                </div>
              )}
              {post.engagement && Object.keys(post.engagement).length > 0 && (
                <div className="flex space-x-4 mb-4">
                  {post.engagement.likes && (
                    <span className="text-sm text-gray-600">❤️ {post.engagement.likes} likes</span>
                  )}
                  {post.engagement.comments && (
                    <span className="text-sm text-gray-600">💬 {post.engagement.comments} comments</span>
                  )}
                  {post.engagement.shares && (
                    <span className="text-sm text-gray-600">🔄 {post.engagement.shares} shares</span>
                  )}
                </div>
              )}
              <div className="flex space-x-2">
                {post.status === 'pending' && (
                  <>
                    <button
                      onClick={() => updateStatus(post.id, 'scheduled')}
                      className="btn-secondary text-sm"
                    >
                      <Calendar className="w-4 h-4 inline mr-1" />
                      Schedule
                    </button>
                    <button
                      onClick={() => updateStatus(post.id, 'published')}
                      className="btn-primary text-sm"
                    >
                      <CheckCircle className="w-4 h-4 inline mr-1" />
                      Publish Now
                    </button>
                  </>
                )}
                {post.status === 'scheduled' && (
                  <button
                    onClick={() => updateStatus(post.id, 'published')}
                    className="btn-primary text-sm"
                  >
                    <CheckCircle className="w-4 h-4 inline mr-1" />
                    Publish Now
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

export default SocialPage;