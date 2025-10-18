import React from 'react';

export const SkeletonCard = ({ className = '' }) => (
  <div className={`animate-pulse bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
    <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
    <div className="h-3 bg-gray-200 rounded w-1/2 mb-3"></div>
    <div className="h-3 bg-gray-200 rounded w-5/6"></div>
  </div>
);

export const SkeletonTable = ({ rows = 5, columns = 4 }) => (
  <div className="animate-pulse bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <div className="p-4 border-b border-gray-200">
      <div className="h-6 bg-gray-200 rounded w-48"></div>
    </div>
    <div className="p-4 space-y-4">
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
          {[...Array(columns)].map((_, j) => (
            <div key={j} className="h-4 bg-gray-200 rounded"></div>
          ))}
        </div>
      ))}
    </div>
  </div>
);

export const SkeletonStatCard = () => (
  <div className="animate-pulse bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <div className="h-4 bg-gray-200 rounded w-24 mb-3"></div>
        <div className="h-8 bg-gray-200 rounded w-20"></div>
      </div>
      <div className="bg-gray-200 p-3 rounded-lg">
        <div className="w-6 h-6 bg-gray-300 rounded"></div>
      </div>
    </div>
  </div>
);

export const SkeletonChart = ({ height = 'h-64' }) => (
  <div className={`animate-pulse bg-white rounded-xl shadow-sm border border-gray-200 p-6`}>
    <div className="h-6 bg-gray-200 rounded w-40 mb-4"></div>
    <div className={`${height} bg-gray-100 rounded`}></div>
  </div>
);

export const SkeletonList = ({ items = 5 }) => (
  <div className="space-y-3">
    {[...Array(items)].map((_, i) => (
      <div key={i} className="animate-pulse bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    ))}
  </div>
);

export const SkeletonProductCard = () => (
  <div className="animate-pulse bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
    <div className="bg-gray-200 h-48"></div>
    <div className="p-4">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
      <div className="h-3 bg-gray-200 rounded w-full mb-3"></div>
      <div className="flex items-center justify-between">
        <div className="h-6 bg-gray-200 rounded w-20"></div>
        <div className="h-8 bg-gray-200 rounded w-24"></div>
      </div>
    </div>
  </div>
);

export const SkeletonDashboard = () => (
  <div className="space-y-6">
    {/* Header */}
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-64 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-96"></div>
    </div>

    {/* Stats Cards */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <SkeletonStatCard key={i} />
      ))}
    </div>

    {/* Chart */}
    <SkeletonChart height="h-80" />

    {/* Table */}
    <SkeletonTable rows={8} columns={5} />
  </div>
);

export default {
  SkeletonCard,
  SkeletonTable,
  SkeletonStatCard,
  SkeletonChart,
  SkeletonList,
  SkeletonProductCard,
  SkeletonDashboard
};
