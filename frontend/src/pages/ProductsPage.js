import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { DollarSign, Plus, Star, Trash2, Edit, Upload, RefreshCw, ShoppingCart } from 'lucide-react';

function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: 0,
    category: 'tools',
    affiliate_link: '',
    discount_code: '',
    discount_percentage: 0,
    image_url: '',
    is_featured: false
  });

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/products`, formData);
      setShowForm(false);
      setFormData({
        name: '',
        description: '',
        price: 0,
        category: 'tools',
        affiliate_link: '',
        discount_code: '',
        discount_percentage: 0,
        image_url: '',
        is_featured: false
      });
      loadProducts();
    } catch (error) {
      console.error('Error creating product:', error);
    }
  };

  const deleteProduct = async (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await axios.delete(`${API}/products/${productId}`);
        loadProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    }
  };

  const toggleFeatured = async (productId, currentStatus) => {
    try {
      await axios.patch(`${API}/products/${productId}`, { is_featured: !currentStatus });
      loadProducts();
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };

  const handleBuyProduct = async (product) => {
    try {
      const originUrl = window.location.origin;
      
      // Check if there's an affiliate code in URL or localStorage
      const urlParams = new URLSearchParams(window.location.search);
      const affiliateCode = urlParams.get('ref') || localStorage.getItem('affiliate_ref');
      
      const requestData = {
        payment_type: 'product',
        product_id: product.id,
        user_email: 'guest@example.com', // In production, get from auth
        origin_url: originUrl,
        metadata: {
          source: 'products_page'
        }
      };
      
      // Add affiliate code if exists
      if (affiliateCode) {
        requestData.affiliate_code = affiliateCode;
      }
      
      const response = await axios.post(`${API}/payments/checkout/session`, requestData);

      // Redirect to Stripe checkout
      if (response.data.url) {
        window.location.href = response.data.url;
      }
    } catch (error) {
      console.error('Error creating checkout:', error);
      alert('Error al crear la sesión de pago. Intenta de nuevo.');
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><div className="loading-spinner"></div></div>;
  }

  return (
    <div data-testid="products-page" className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-2">
            <DollarSign className="w-8 h-8" />
            <span>Monetization Manager</span>
          </h1>
          <p className="text-gray-600 mt-1">Manage products, affiliates, and discount codes</p>
        </div>
        <button
          data-testid="add-product-btn"
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Product</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Add New Product</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Product Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="input-field"
                >
                  <option value="tools">Tools</option>
                  <option value="accessories">Accessories</option>
                  <option value="equipment">Equipment</option>
                  <option value="parts">Parts</option>
                  <option value="safety">Safety</option>
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Price ($)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Discount Code</label>
                <input
                  type="text"
                  value={formData.discount_code}
                  onChange={(e) => setFormData({ ...formData, discount_code: e.target.value })}
                  className="input-field"
                  placeholder="SAVE20"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Discount %</label>
                <input
                  type="number"
                  value={formData.discount_percentage}
                  onChange={(e) => setFormData({ ...formData, discount_percentage: parseFloat(e.target.value) })}
                  className="input-field"
                  min="0"
                  max="100"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Affiliate Link</label>
              <input
                type="url"
                value={formData.affiliate_link}
                onChange={(e) => setFormData({ ...formData, affiliate_link: e.target.value })}
                className="input-field"
                placeholder="https://..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Image URL</label>
              <input
                type="url"
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                className="input-field"
                placeholder="https://..."
              />
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_featured"
                checked={formData.is_featured}
                onChange={(e) => setFormData({ ...formData, is_featured: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="is_featured" className="text-sm font-medium text-gray-700">Featured Product</label>
            </div>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">Save Product</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.length === 0 ? (
          <div className="col-span-full card text-center py-12">
            <DollarSign className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No products yet. Add your first product!</p>
          </div>
        ) : (
          products.map((product) => (
            <div key={product.id} className="card relative">
              {product.is_featured && (
                <div className="absolute top-4 right-4">
                  <Star className="w-6 h-6 text-yellow-500 fill-yellow-500" />
                </div>
              )}
              {product.image_url && (
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                  onError={(e) => { e.target.style.display = 'none'; }}
                />
              )}
              <span className="badge badge-info mb-2">{product.category}</span>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{product.name}</h3>
              <p className="text-gray-600 text-sm mb-4">{product.description}</p>
              <div className="flex items-center justify-between mb-3">
                <span className="text-2xl font-bold text-green-600">${product.price}</span>
                {product.discount_percentage > 0 && (
                  <span className="badge badge-danger">{product.discount_percentage}% OFF</span>
                )}
              </div>
              {product.discount_code && (
                <div className="bg-yellow-50 p-2 rounded mb-3">
                  <p className="text-sm text-yellow-800">Code: <strong>{product.discount_code}</strong></p>
                </div>
              )}
              {product.affiliate_link && (
                <a
                  href={product.affiliate_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 text-sm hover:underline block mb-3"
                >
                  View Affiliate Link →
                </a>
              )}
              
              {/* Buy Button */}
              <button
                onClick={() => handleBuyProduct(product)}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2 mb-3"
              >
                <ShoppingCart className="w-5 h-5" />
                <span>Comprar ${product.price}</span>
              </button>
              
              <div className="flex space-x-2 mt-4">
                <button
                  onClick={() => toggleFeatured(product.id, product.is_featured)}
                  className="btn-secondary text-sm flex-1"
                >
                  <Star className="w-4 h-4 inline mr-1" />
                  {product.is_featured ? 'Unfeature' : 'Feature'}
                </button>
                <button
                  onClick={() => deleteProduct(product.id)}
                  className="btn-secondary text-sm text-red-600 border-red-600 hover:bg-red-600"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ProductsPage;