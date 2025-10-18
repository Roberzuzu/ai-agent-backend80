import React, { useState, useEffect } from 'react';
import { Download, FileSpreadsheet, RefreshCw } from 'lucide-react';
import SearchAndFilter from '../components/SearchAndFilter';
import SortableTable from '../components/SortableTable';
import Pagination from '../components/Pagination';
import { exportToCSV, exportToExcel } from '../utils/exportUtils';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';

function DataTableExample() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(25);
  
  // Search and filter state
  const [searchValue, setSearchValue] = useState('');
  const [filterValues, setFilterValues] = useState({});
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  
  // Sorting state
  const [sortColumn, setSortColumn] = useState('');
  const [sortDirection, setSortDirection] = useState('asc');

  // Define filters
  const filters = [
    {
      key: 'status',
      label: 'Estado',
      type: 'select',
      value: filterValues.status,
      options: [
        { value: 'active', label: 'Activo' },
        { value: 'inactive', label: 'Inactivo' },
        { value: 'pending', label: 'Pendiente' }
      ]
    },
    {
      key: 'category',
      label: 'Categoría',
      type: 'select',
      value: filterValues.category,
      options: [
        { value: 'electronics', label: 'Electrónica' },
        { value: 'clothing', label: 'Ropa' },
        { value: 'food', label: 'Alimentos' }
      ]
    },
    {
      key: 'priceRange',
      label: 'Rango de Precio',
      type: 'range',
      value: filterValues.priceRange
    },
    {
      key: 'featured',
      label: 'Destacado',
      type: 'checkbox',
      value: filterValues.featured,
      checkboxLabel: 'Solo productos destacados'
    }
  ];

  // Define table columns
  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Nombre', sortable: true },
    { 
      key: 'category', 
      label: 'Categoría', 
      sortable: true,
      render: (value) => (
        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
          {value}
        </span>
      )
    },
    { 
      key: 'price', 
      label: 'Precio', 
      sortable: true,
      render: (value) => `$${value.toFixed(2)}`
    },
    { 
      key: 'status', 
      label: 'Estado', 
      sortable: true,
      render: (value) => {
        const colors = {
          active: 'bg-green-100 text-green-800',
          inactive: 'bg-gray-100 text-gray-800',
          pending: 'bg-yellow-100 text-yellow-800'
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs ${colors[value] || colors.inactive}`}>
            {value}
          </span>
        );
      }
    },
    {
      key: 'created_at',
      label: 'Fecha',
      sortable: true,
      render: (value) => new Date(value).toLocaleDateString('es-ES')
    }
  ];

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    applyFiltersAndSearch();
  }, [data, searchValue, filterValues, dateRange, sortColumn, sortDirection]);

  const loadData = async () => {
    try {
      setLoading(true);
      // In production, replace with actual API call
      // const response = await axiosInstance.get('/your-endpoint');
      // setData(response.data);
      
      // Mock data for demonstration
      const mockData = Array.from({ length: 100 }, (_, i) => ({
        id: i + 1,
        name: `Producto ${i + 1}`,
        category: ['electronics', 'clothing', 'food'][Math.floor(Math.random() * 3)],
        price: Math.random() * 1000,
        status: ['active', 'inactive', 'pending'][Math.floor(Math.random() * 3)],
        featured: Math.random() > 0.7,
        created_at: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString()
      }));
      
      setData(mockData);
      toast.success('Datos cargados correctamente');
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSearch = () => {
    let result = [...data];

    // Apply search
    if (searchValue) {
      result = result.filter(item =>
        item.name.toLowerCase().includes(searchValue.toLowerCase()) ||
        item.category.toLowerCase().includes(searchValue.toLowerCase())
      );
    }

    // Apply filters
    Object.keys(filterValues).forEach(key => {
      const value = filterValues[key];
      if (!value || (Array.isArray(value) && value.length === 0) || value === '') return;

      if (key === 'priceRange' && value.min !== undefined && value.max !== undefined) {
        if (value.min) result = result.filter(item => item.price >= Number(value.min));
        if (value.max) result = result.filter(item => item.price <= Number(value.max));
      } else if (key === 'featured' && value) {
        result = result.filter(item => item.featured === true);
      } else {
        result = result.filter(item => item[key] === value);
      }
    });

    // Apply date range
    if (dateRange.start && dateRange.end) {
      result = result.filter(item => {
        const itemDate = new Date(item.created_at);
        return itemDate >= new Date(dateRange.start) && itemDate <= new Date(dateRange.end);
      });
    }

    // Apply sorting
    if (sortColumn) {
      result.sort((a, b) => {
        const aVal = a[sortColumn];
        const bVal = b[sortColumn];
        
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    setFilteredData(result);
    setCurrentPage(1); // Reset to first page when filters change
  };

  const handleFilterChange = (key, value) => {
    setFilterValues(prev => ({ ...prev, [key]: value }));
  };

  const handleSort = (column, direction) => {
    setSortColumn(column);
    setSortDirection(direction);
  };

  const handleExportCSV = () => {
    exportToCSV(paginatedData, `productos_${new Date().toISOString().split('T')[0]}.csv`);
    toast.success('Exportado a CSV correctamente');
  };

  const handleExportExcel = () => {
    exportToExcel(paginatedData, `productos_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.success('Exportado a Excel correctamente');
  };

  // Paginate data
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedData = filteredData.slice(startIndex, startIndex + itemsPerPage);
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Lista de Productos
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Gestiona todos tus productos con búsqueda, filtros y exportación
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Actualizar
          </button>
          
          <button
            onClick={handleExportCSV}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Download className="w-4 h-4" />
            CSV
          </button>
          
          <button
            onClick={handleExportExcel}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Excel
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <SearchAndFilter
        searchValue={searchValue}
        onSearchChange={setSearchValue}
        filters={filters}
        onFilterChange={handleFilterChange}
        dateRange={dateRange}
        onDateRangeChange={setDateRange}
        placeholder="Buscar por nombre o categoría..."
      />

      {/* Results count */}
      <div className="text-sm text-gray-600 dark:text-gray-400">
        Mostrando {paginatedData.length} de {filteredData.length} resultados
        {filteredData.length !== data.length && ` (filtrados de ${data.length} totales)`}
      </div>

      {/* Table */}
      <SortableTable
        columns={columns}
        data={paginatedData}
        sortColumn={sortColumn}
        sortDirection={sortDirection}
        onSort={handleSort}
        loading={loading}
        emptyMessage={searchValue || Object.keys(filterValues).length > 0 
          ? "No se encontraron resultados con los filtros aplicados" 
          : "No hay productos disponibles"
        }
      />

      {/* Pagination */}
      {filteredData.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          totalItems={filteredData.length}
          itemsPerPage={itemsPerPage}
          onPageChange={setCurrentPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}
    </div>
  );
}

export default DataTableExample;
