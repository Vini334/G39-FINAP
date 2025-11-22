/**
 * API Configuration
 * Axios instance configured for FINAP backend
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// API Base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1';

// Create axios instance
export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

/**
 * Request interceptor
 * Adds authentication token to requests
 */
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor
 * Handles token refresh and error responses
 */
api.interceptors.response.use(
  (response) => {
    // Return successful responses
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Don't try to refresh token for login/register endpoints
      const isAuthEndpoint = originalRequest.url?.includes('/auth/login') ||
                            originalRequest.url?.includes('/auth/register');

      if (isAuthEndpoint) {
        // For login/register failures, just return the error
        return Promise.reject(error);
      }

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
          // No refresh token, clear data but don't redirect
          // Let the calling component handle the navigation
          throw new Error('No refresh token available');
        }

        // Call refresh endpoint
        const response = await axios.post(`${API_BASE_URL}/api/${API_VERSION}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data.data;

        // Save new access token
        localStorage.setItem('access_token', access_token);

        // Retry original request with new token
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }

        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear tokens but don't redirect
        // Let the calling component handle the navigation
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');

        return Promise.reject(refreshError);
      }
    }

    // Return other errors
    return Promise.reject(error);
  }
);

/**
 * Standard API response type
 */
export interface APIResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  errors?: any[];
}

/**
 * Error response type
 */
export interface APIError {
  detail: string | Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

/**
 * Helper function to extract error message
 */
export const getErrorMessage = (error: any): string => {
  if (axios.isAxiosError(error)) {
    const apiError = error.response?.data as APIError;

    if (apiError?.detail) {
      if (typeof apiError.detail === 'string') {
        const detail = apiError.detail;

        // Customize error messages for better user experience
        if (detail.toLowerCase().includes('invalid credentials') ||
            detail.toLowerCase().includes('incorrect') ||
            detail.toLowerCase().includes('wrong')) {
          return 'Email ou senha incorretos';
        }

        if (detail.toLowerCase().includes('user not found') ||
            detail.toLowerCase().includes('não encontrado') ||
            detail.toLowerCase().includes('cadastre-se')) {
          return 'Email não cadastrado. Por favor, cadastre-se primeiro.';
        }

        if (detail.toLowerCase().includes('already exists') ||
            detail.toLowerCase().includes('already registered') ||
            detail.toLowerCase().includes('já está cadastrado')) {
          return 'Este email já está cadastrado. Tente fazer login.';
        }

        if (detail.toLowerCase().includes('desativada')) {
          return 'Sua conta está desativada. Entre em contato com o suporte.';
        }

        return detail;
      } else if (Array.isArray(apiError.detail)) {
        return apiError.detail[0]?.msg || 'Erro de validação';
      }
    }

    // Network errors
    if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
      return 'Erro de conexão. Verifique sua internet e tente novamente.';
    }

    // Timeout errors
    if (error.code === 'ECONNABORTED') {
      return 'A requisição demorou muito. Tente novamente.';
    }

    return error.message || 'Erro de conexão';
  }

  return 'Erro inesperado. Tente novamente.';
};

export default api;
