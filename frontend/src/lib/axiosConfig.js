import axios from 'axios';
import { toast } from 'sonner';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001/api';

// Create axios instance
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor with retry logic
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Don't retry if we've already retried 3 times
    if (!originalRequest._retry) {
      originalRequest._retry = 0;
    }

    // Retry logic for network errors or 5xx errors
    if (
      originalRequest._retry < 3 &&
      (error.code === 'ECONNABORTED' ||
        error.code === 'ERR_NETWORK' ||
        (error.response && error.response.status >= 500))
    ) {
      originalRequest._retry += 1;
      
      // Exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, originalRequest._retry - 1) * 1000;
      
      console.log(`Retry attempt ${originalRequest._retry} after ${delay}ms`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
      
      return axiosInstance(originalRequest);
    }

    // Handle specific error cases with user-friendly messages
    if (error.response) {
      const status = error.response.status;
      const message = error.response.data?.detail || error.response.data?.message || 'Error desconocido';

      switch (status) {
        case 400:
          toast.error(`Error de validación: ${message}`);
          break;
        case 401:
          toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setTimeout(() => {
            window.location.href = '/login';
          }, 2000);
          break;
        case 403:
          toast.error('No tienes permiso para realizar esta acción.');
          break;
        case 404:
          toast.error('Recurso no encontrado.');
          break;
        case 422:
          toast.error(`Datos inválidos: ${message}`);
          break;
        case 429:
          toast.error('Demasiadas solicitudes. Por favor, espera un momento.');
          break;
        case 500:
          toast.error('Error del servidor. Estamos trabajando en solucionarlo.');
          break;
        case 503:
          toast.error('Servicio temporalmente no disponible. Intenta de nuevo más tarde.');
          break;
        default:
          toast.error(`Error: ${message}`);
      }
    } else if (error.code === 'ECONNABORTED') {
      toast.error('La solicitud tardó demasiado. Intenta de nuevo.');
    } else if (error.code === 'ERR_NETWORK') {
      toast.error('Error de conexión. Verifica tu internet.');
    } else {
      toast.error('Ocurrió un error inesperado. Intenta de nuevo.');
    }

    return Promise.reject(error);
  }
);

// Helper function for making requests with loading state
export const apiRequest = async (requestFn, options = {}) => {
  const { 
    showSuccessToast = false, 
    successMessage = 'Operación exitosa',
    showErrorToast = true 
  } = options;

  try {
    const response = await requestFn();
    
    if (showSuccessToast) {
      toast.success(successMessage);
    }
    
    return { data: response.data, error: null };
  } catch (error) {
    // Error already handled by interceptor
    return { data: null, error };
  }
};

export default axiosInstance;
