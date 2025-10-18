import React from 'react';
import { Users, MousePointer, DollarSign, TrendingUp } from 'lucide-react';
import StatCard from '../StatCard';

const AffiliateWidget = ({ data, loading }) => {
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
        title="Total Afiliados"
        value={data?.total || 0}
        icon={Users}
        color="purple"
        comparison={{
          value: 15,
          isPositive: true,
          period: 'vs mes anterior'
        }}
      />
      <StatCard
        title="Afiliados Activos"
        value={data?.active || 0}
        icon={TrendingUp}
        color="green"
      />
      <StatCard
        title="Clicks Totales"
        value={data?.total_clicks || 0}
        icon={MousePointer}
        color="blue"
      />
      <StatCard
        title="Comisiones"
        value={data?.commission_amount || 0}
        icon={DollarSign}
        color="orange"
        prefix="$"
        comparison={{
          value: data?.change_percent || 0,
          isPositive: data?.change_percent >= 0,
          period: 'vs periodo anterior'
        }}
      />
    </div>
  );
};

export default AffiliateWidget;