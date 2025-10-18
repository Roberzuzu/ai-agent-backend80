import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const StatCard = ({ 
  title, 
  value, 
  icon: Icon, 
  color = 'blue',
  comparison = null, // { value: 12.5, isPositive: true, period: 'vs mes anterior' }
  suffix = '',
  prefix = '',
  loading = false,
  onClick = null
}) => {
  const colorClasses = {
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    green: 'bg-green-500',
    pink: 'bg-pink-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500',
    yellow: 'bg-yellow-500',
    indigo: 'bg-indigo-500',
    teal: 'bg-teal-500',
  };

  const bgColorClasses = {
    blue: 'bg-blue-50',
    purple: 'bg-purple-50',
    green: 'bg-green-50',
    pink: 'bg-pink-50',
    orange: 'bg-orange-50',
    red: 'bg-red-50',
    yellow: 'bg-yellow-50',
    indigo: 'bg-indigo-50',
    teal: 'bg-teal-50',
  };

  const getTrendIcon = () => {
    if (!comparison) return null;
    if (comparison.value === 0) return <Minus className="w-4 h-4" />;
    return comparison.isPositive ? 
      <TrendingUp className="w-4 h-4" /> : 
      <TrendingDown className="w-4 h-4" />;
  };

  const getTrendColor = () => {
    if (!comparison) return '';
    if (comparison.value === 0) return 'text-gray-500';
    return comparison.isPositive ? 'text-green-600' : 'text-red-600';
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}`}>
        <div className="animate-pulse">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-24 mb-3"></div>
              <div className="h-8 bg-gray-200 rounded w-20"></div>
            </div>
            <div className={`${bgColorClasses[color]} p-3 rounded-lg`}>
              <div className="w-6 h-6 bg-gray-300 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-gray-600 text-sm font-medium mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">
            {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
          </p>
          
          {comparison && (
            <div className={`flex items-center gap-1 mt-2 ${getTrendColor()}`}>
              {getTrendIcon()}
              <span className="text-sm font-semibold">
                {Math.abs(comparison.value)}%
              </span>
              <span className="text-xs text-gray-500">
                {comparison.period || 'vs anterior'}
              </span>
            </div>
          )}
        </div>
        
        <div className={`${colorClasses[color]} p-3 rounded-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );
};

export default StatCard;
