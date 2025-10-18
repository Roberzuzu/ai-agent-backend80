import React from 'react';
import { TestTube, Play, CheckCircle2, TrendingUp } from 'lucide-react';
import StatCard from '../StatCard';

const ABTestWidget = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <StatCard key={i} loading={true} />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Tests Activos"
        value={data?.active_tests || 0}
        icon={Play}
        color="blue"
      />
      <StatCard
        title="Completados"
        value={data?.completed_tests || 0}
        icon={CheckCircle2}
        color="green"
      />
      <StatCard
        title="Total Tests"
        value={data?.total_tests || 0}
        icon={TestTube}
        color="purple"
      />
      <StatCard
        title="Mejora Promedio"
        value={data?.avg_improvement || 0}
        icon={TrendingUp}
        color="orange"
        suffix="%"
      />
    </div>
  );
};

export default ABTestWidget;