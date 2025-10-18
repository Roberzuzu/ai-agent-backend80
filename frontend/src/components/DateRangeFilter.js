import React from 'react';
import { Calendar } from 'lucide-react';

const DateRangeFilter = ({ selectedRange, onRangeChange }) => {
  const ranges = [
    { value: 7, label: '7 días' },
    { value: 30, label: '30 días' },
    { value: 90, label: '90 días' },
    { value: 365, label: '1 año' },
  ];

  return (
    <div className="flex items-center gap-2 bg-white rounded-lg shadow-sm border border-gray-200 p-1">
      <Calendar className="w-4 h-4 text-gray-500 ml-2" />
      {ranges.map((range) => (
        <button
          key={range.value}
          onClick={() => onRangeChange(range.value)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            selectedRange === range.value
              ? 'bg-blue-600 text-white'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          {range.label}
        </button>
      ))}
    </div>
  );
};

export default DateRangeFilter;