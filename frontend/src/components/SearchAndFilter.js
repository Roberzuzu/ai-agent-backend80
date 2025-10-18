import React, { useState } from 'react';
import { Search, X, Filter, Calendar, ChevronDown } from 'lucide-react';

const SearchAndFilter = ({ 
  searchValue,
  onSearchChange,
  filters = [],
  onFilterChange,
  dateRange = null,
  onDateRangeChange = null,
  placeholder = "Buscar..."
}) => {
  const [showFilters, setShowFilters] = useState(false);

  return (
    <div className="space-y-4">
      {/* Search bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={searchValue}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder={placeholder}
            className="w-full pl-10 pr-10 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          />
          {searchValue && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {filters.length > 0 && (
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            <Filter className="w-5 h-5" />
            Filtros
            <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </button>
        )}
      </div>

      {/* Filters panel */}
      {showFilters && filters.length > 0 && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 animate-fadeInDown">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filters.map((filter) => (
              <div key={filter.key}>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {filter.label}
                </label>
                
                {filter.type === 'select' && (
                  <select
                    value={filter.value || ''}
                    onChange={(e) => onFilterChange(filter.key, e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                  >
                    <option value="">Todos</option>
                    {filter.options.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                )}

                {filter.type === 'multiselect' && (
                  <select
                    multiple
                    value={filter.value || []}
                    onChange={(e) => {
                      const values = Array.from(e.target.selectedOptions, option => option.value);
                      onFilterChange(filter.key, values);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    size={Math.min(filter.options.length, 4)}
                  >
                    {filter.options.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                )}

                {filter.type === 'checkbox' && (
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={filter.value || false}
                      onChange={(e) => onFilterChange(filter.key, e.target.checked)}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      {filter.checkboxLabel}
                    </span>
                  </label>
                )}

                {filter.type === 'range' && (
                  <div className="flex gap-2">
                    <input
                      type="number"
                      placeholder="Min"
                      value={filter.value?.min || ''}
                      onChange={(e) => onFilterChange(filter.key, { ...filter.value, min: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    />
                    <input
                      type="number"
                      placeholder="Max"
                      value={filter.value?.max || ''}
                      onChange={(e) => onFilterChange(filter.key, { ...filter.value, max: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    />
                  </div>
                )}
              </div>
            ))}

            {/* Date range filter */}
            {onDateRangeChange && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  <Calendar className="w-4 h-4 inline mr-1" />
                  Rango de Fechas
                </label>
                <div className="flex gap-2">
                  <input
                    type="date"
                    value={dateRange?.start || ''}
                    onChange={(e) => onDateRangeChange({ ...dateRange, start: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                  />
                  <input
                    type="date"
                    value={dateRange?.end || ''}
                    onChange={(e) => onDateRangeChange({ ...dateRange, end: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Clear filters button */}
          <div className="mt-4 flex justify-end">
            <button
              onClick={() => {
                onSearchChange('');
                filters.forEach(filter => onFilterChange(filter.key, filter.type === 'checkbox' ? false : ''));
                if (onDateRangeChange) onDateRangeChange({ start: '', end: '' });
              }}
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white underline"
            >
              Limpiar todos los filtros
            </button>
          </div>
        </div>
      )}

      {/* Active filters display */}
      {(searchValue || filters.some(f => f.value && (Array.isArray(f.value) ? f.value.length > 0 : f.value !== ''))) && (
        <div className="flex flex-wrap gap-2">
          {searchValue && (
            <div className="flex items-center gap-2 px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm">
              <Search className="w-3 h-3" />
              <span>"{searchValue}"</span>
              <button onClick={() => onSearchChange('')} className="hover:text-blue-900 dark:hover:text-blue-100">
                <X className="w-3 h-3" />
              </button>
            </div>
          )}

          {filters.map((filter) => {
            if (!filter.value || (Array.isArray(filter.value) && filter.value.length === 0) || filter.value === '') return null;
            
            const displayValue = Array.isArray(filter.value) 
              ? filter.value.map(v => filter.options.find(o => o.value === v)?.label).join(', ')
              : filter.type === 'checkbox' 
              ? filter.checkboxLabel
              : filter.options?.find(o => o.value === filter.value)?.label || filter.value;

            return (
              <div key={filter.key} className="flex items-center gap-2 px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full text-sm">
                <span>{filter.label}: {displayValue}</span>
                <button 
                  onClick={() => onFilterChange(filter.key, filter.type === 'checkbox' ? false : '')}
                  className="hover:text-purple-900 dark:hover:text-purple-100"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default SearchAndFilter;
