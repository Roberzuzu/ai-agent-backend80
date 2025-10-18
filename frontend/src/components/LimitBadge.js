import React, { useState, useEffect } from 'react';
import { AlertCircle, TrendingUp, Zap, Crown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../lib/axiosConfig';
import { useAuth } from '../contexts/AuthContext';

const LimitBadge = ({ resourceType, showDetails = false }) => {
  const [limitInfo, setLimitInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      checkLimit();
    }
  }, [user, resourceType]);

  const checkLimit = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get(
        `/limits/check/${resourceType}?user_email=${user.email}`
      );
      setLimitInfo(response.data);
    } catch (error) {
      console.error('Error checking limit:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !limitInfo) {
    return null;
  }

  const getColor = () => {
    if (!limitInfo.allowed) return 'red';
    if (limitInfo.percentage >= 80) return 'yellow';
    return 'green';
  };

  const colors = {
    red: {
      bg: 'bg-red-100 dark:bg-red-900',
      text: 'text-red-800 dark:text-red-200',
      border: 'border-red-300 dark:border-red-700'
    },
    yellow: {
      bg: 'bg-yellow-100 dark:bg-yellow-900',
      text: 'text-yellow-800 dark:text-yellow-200',
      border: 'border-yellow-300 dark:border-yellow-700'
    },
    green: {
      bg: 'bg-green-100 dark:bg-green-900',
      text: 'text-green-800 dark:text-green-200',
      border: 'border-green-300 dark:border-green-700'
    }
  };

  const color = colors[getColor()];

  if (!showDetails) {
    // Compact badge
    return (
      <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm ${color.bg} ${color.text}`}>
        <span>
          {limitInfo.limit === -1 
            ? '∞' 
            : `${limitInfo.current_usage}/${limitInfo.limit}`
          }
        </span>
      </div>
    );
  }

  // Detailed view
  return (
    <div className={`rounded-lg border-2 p-4 ${color.border} ${color.bg}`}>
      <div className="flex items-start justify-between mb-2">
        <div>
          <h3 className={`font-semibold ${color.text}`}>
            {limitInfo.message}
          </h3>
          <p className={`text-sm ${color.text} opacity-80 mt-1`}>
            Plan: {limitInfo.tier.charAt(0).toUpperCase() + limitInfo.tier.slice(1)}
          </p>
        </div>
        {limitInfo.needs_upgrade && (
          <AlertCircle className={`w-5 h-5 ${color.text}`} />
        )}
      </div>

      {limitInfo.limit !== -1 && (
        <div className="mb-3">
          <div className="flex justify-between text-sm mb-1">
            <span className={color.text}>Uso</span>
            <span className={color.text}>
              {limitInfo.current_usage} / {limitInfo.limit} ({limitInfo.percentage}%)
            </span>
          </div>
          <div className="w-full bg-white dark:bg-gray-700 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all ${
                !limitInfo.allowed ? 'bg-red-600' :
                limitInfo.percentage >= 80 ? 'bg-yellow-600' :
                'bg-green-600'
              }`}
              style={{ width: `${Math.min(limitInfo.percentage, 100)}%` }}
            ></div>
          </div>
        </div>
      )}

      {limitInfo.needs_upgrade && (
        <button
          onClick={() => navigate('/subscriptions')}
          className="w-full mt-2 flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all font-medium"
        >
          <Crown className="w-4 h-4" />
          Mejorar Plan
        </button>
      )}
    </div>
  );
};

export default LimitBadge;
