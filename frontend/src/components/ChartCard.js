import React from 'react';

const ChartCard = ({ 
  title, 
  children, 
  loading = false,
  actions = null,
  description = null,
  height = 'auto'
}) => {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-40 mb-2"></div>
          {description && <div className="h-4 bg-gray-200 rounded w-64 mb-4"></div>}
          <div className="h-64 bg-gray-100 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{title}</h3>
          {description && (
            <p className="text-sm text-gray-600 mt-1">{description}</p>
          )}
        </div>
        {actions && <div>{actions}</div>}
      </div>
      <div style={{ height: height }}>
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
