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
  timeout: 30000, // 30 seconds - increased for slower connections
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

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
          // No refresh token, redirect to login
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
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');

        // Redirect to login page
        window.location.href = '/login';

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
        return apiError.detail;
      } else if (Array.isArray(apiError.detail)) {
        return apiError.detail[0]?.msg || 'Erro desconhecido';
      }
    }

    return error.message || 'Erro de conexão';
  }

  return 'Erro desconhecido';
};

export default api;
