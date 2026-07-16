import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Products API
export const productsAPI = {
  list: (params?: any) => api.get('/products', { params }),
  get: (id: number) => api.get(`/products/${id}`),
  create: (data: any) => api.post('/products', data),
  search: (query: string) => api.get(`/products/search/${query}`),
  getByBarcode: (barcode: string) => api.get(`/products/barcode/${barcode}`),
  scan: (formData: FormData) => api.post('/products/scan', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

// Recommendations API
export const recommendationsAPI = {
  analyze: (data: any) => api.post('/recommendations/analyze', data),
  compare: (data: any) => api.post('/recommendations/compare', data),
  fuzzyEvaluate: (data: any) => api.post('/recommendations/fuzzy-evaluate', data),
};

// Ingredients API
export const ingredientsAPI = {
  list: (params?: any) => api.get('/ingredients', { params }),
  get: (id: number) => api.get(`/ingredients/${id}`),
  analyze: (data: any) => api.post('/ingredients/analyze', data),
  search: (name: string) => api.get(`/ingredients/search/${name}`),
};

// Claims API
export const claimsAPI = {
  analyze: (data: any) => api.post('/claims/analyze', data),
  batchAnalyze: (data: any) => api.post('/claims/batch-analyze', data),
};
