import React from 'react';
import { Mail, Send, Eye, MousePointer } from 'lucide-react';
import StatCard from '../StatCard';

const EmailWidget = ({ data, loading }) => {
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
        title="Campañas Activas"
        value={data?.active_campaigns || 0}
        icon={Mail}
        color="blue"
      />
      <StatCard
        title="Emails Enviados"
        value={data?.emails_sent || 0}
        icon={Send}
        color="purple"
      />
      <StatCard
        title="Tasa Apertura"
        value={data?.open_rate || 0}
        icon={Eye}
        color="green"
        suffix="%"
      />
      <StatCard
        title="Tasa Click"
        value={data?.click_rate || 0}
        icon={MousePointer}
        color="orange"
        suffix="%"
        comparison={{
          value: 8.5,
          isPositive: true,
          period: 'vs mes anterior'
        }}
      />
    </div>
  );
};

export default EmailWidget;