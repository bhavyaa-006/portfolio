import axios from 'axios';

const explicitApiUrl = (import.meta.env.VITE_API_URL || '').trim().replace(/\/+$/, '');
const isBrowser = typeof window !== 'undefined';
const isLocalHost = isBrowser && ['localhost', '127.0.0.1'].includes(window.location.hostname);
const normalizedExplicitApiUrl = explicitApiUrl
  ? explicitApiUrl.endsWith('/api/v1')
    ? explicitApiUrl
    : `${explicitApiUrl}/api/v1`
  : '';

const baseURL = normalizedExplicitApiUrl || (isLocalHost ? '/api/v1' : '/api/v1');

if (import.meta.env.PROD && !normalizedExplicitApiUrl) {
  console.warn('VITE_API_URL is not set. Production requests will fall back to the current origin and likely fail.');
}

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API request failed', {
      url: error?.config?.url,
      status: error?.response?.status,
      message: error?.message,
    });
    return Promise.reject(error);
  }
);

export default api;
