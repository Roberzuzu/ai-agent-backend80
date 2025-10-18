import { Download, FileSpreadsheet } from 'lucide-react';

// Export to CSV
export const exportToCSV = (data, filename = 'export.csv', columns = null) => {
  if (!data || data.length === 0) {
    alert('No hay datos para exportar');
    return;
  }

  // If columns not specified, use all keys from first object
  const headers = columns || Object.keys(data[0]);
  
  // Create CSV content
  let csv = headers.join(',') + '\n';
  
  data.forEach(row => {
    const values = headers.map(header => {
      const value = row[header];
      // Handle values with commas, quotes, and newlines
      if (value === null || value === undefined) return '';
      const stringValue = String(value);
      if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
        return `"${stringValue.replace(/"/g, '""')}"`;
      }
      return stringValue;
    });
    csv += values.join(',') + '\n';
  });

  // Create blob and download
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Export to Excel (actually XLSX format)
export const exportToExcel = (data, filename = 'export.xlsx', sheetName = 'Sheet1', columns = null) => {
  if (!data || data.length === 0) {
    alert('No hay datos para exportar');
    return;
  }

  // If columns not specified, use all keys from first object
  const headers = columns || Object.keys(data[0]);
  
  // Create table HTML
  let html = '<table>';
  
  // Headers
  html += '<thead><tr>';
  headers.forEach(header => {
    html += `<th>${header}</th>`;
  });
  html += '</tr></thead>';
  
  // Body
  html += '<tbody>';
  data.forEach(row => {
    html += '<tr>';
    headers.forEach(header => {
      const value = row[header];
      html += `<td>${value !== null && value !== undefined ? value : ''}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody></table>';

  // Create blob with Excel MIME type
  const blob = new Blob([html], { 
    type: 'application/vnd.ms-excel' 
  });
  
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Export button component
export const ExportButton = ({ 
  data, 
  filename = 'export', 
  format = 'csv',
  columns = null,
  label = 'Exportar',
  className = ''
}) => {
  const handleExport = () => {
    const timestamp = new Date().toISOString().split('T')[0];
    const fullFilename = `${filename}_${timestamp}.${format}`;
    
    if (format === 'csv') {
      exportToCSV(data, fullFilename, columns);
    } else if (format === 'excel' || format === 'xlsx') {
      exportToExcel(data, fullFilename.replace(format, 'xlsx'), 'Data', columns);
    }
  };

  return (
    <button
      onClick={handleExport}
      className={`flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors ${className}`}
    >
      {format === 'excel' || format === 'xlsx' ? (
        <FileSpreadsheet className="w-4 h-4" />
      ) : (
        <Download className="w-4 h-4" />
      )}
      {label}
    </button>
  );
};

export default {
  exportToCSV,
  exportToExcel,
  ExportButton
};
