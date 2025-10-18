import React from 'react';
import { ShoppingCart, XCircle, CheckCircle, TrendingDown } from 'lucide-react';
import StatCard from '../StatCard';

const CartWidget = ({ data, loading }) => {
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
        title="Carritos Totales"
        value={data?.total_carts || 0}
        icon={ShoppingCart}
        color="blue"
      />
      <StatCard
        title="Abandonados"
        value={data?.abandoned || 0}
        icon={XCircle}
        color="red"
      />
      <StatCard
        title="Recuperados"
        value={data?.recovered || 0}
        icon={CheckCircle}
        color="green"
        comparison={{
          value: 12.5,
          isPositive: true,
          period: 'vs mes anterior'
        }}
      />
      <StatCard
        title="Tasa Abandono"
        value={data?.abandonment_rate || 0}
        icon={TrendingDown}
        color="orange"
        suffix="%"
      />
    </div>
  );
};

export default CartWidget;