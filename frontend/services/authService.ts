/**
 * Authentication Service
 * Handles user authentication, registration, and token management
 */

import api, { APIResponse, getErrorMessage } from './api';
import type {
  RegisterRequest,
  LoginRequest,
  AuthResponse,
  UserData,
} from '../types/api';

class AuthService {
  /**
   * Register a new user
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await api.post<APIResponse<AuthResponse>>('/auth/register', data);

      const authData = response.data.data;

      // Save tokens and user data
      this.saveAuthData(authData);

      return authData;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Login user
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await api.post<APIResponse<AuthResponse>>('/auth/login', data);

      const authData = response.data.data;

      // Save tokens and user data
      this.saveAuthData(authData);

      return authData;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      // Call logout endpoint
      await api.post('/auth/logout');
    } catch (error) {
      // Log error but continue with local logout
      console.error('Logout error:', error);
    } finally {
      // Clear local data regardless of API call success
      this.clearAuthData();
    }
  }

  /**
   * Get current user data
   */
  async getCurrentUser(): Promise<UserData> {
    try {
      const response = await api.get<APIResponse<{ user: UserData }>>('/auth/me');
      return response.data.data.user;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(data: Partial<{
    name: string;
    phone: string;
    profile: any;
    preferences: any;
  }>): Promise<UserData> {
    try {
      const response = await api.put<APIResponse<{ user: UserData }>>('/auth/me', data);

      const userData = response.data.data.user;

      // Update stored user data
      this.saveUser(userData);

      return userData;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Update user avatar
   */
  async updateAvatar(avatarUrl: string): Promise<UserData> {
    return this.updateProfile({
      profile: { avatar_url: avatarUrl }
    });
  }

  /**
   * Delete user account
   */
  async deleteAccount(): Promise<void> {
    try {
      await api.delete('/auth/me');
      this.clearAuthData();
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    try {
      const refreshToken = this.getRefreshToken();

      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.post<APIResponse<{ access_token: string }>>(
        '/auth/refresh',
        { refresh_token: refreshToken }
      );

      const { access_token } = response.data.data;

      // Save new access token
      localStorage.setItem('access_token', access_token);

      return access_token;
    } catch (error) {
      // Clear auth data on refresh failure
      this.clearAuthData();
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    return !!token;
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Get stored user data
   */
  getUser(): UserData | null {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;

    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  /**
   * Save authentication data to localStorage
   */
  private saveAuthData(authData: AuthResponse): void {
    const { tokens, user } = authData;

    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
  }

  /**
   * Save user data to localStorage
   */
  private saveUser(user: UserData): void {
    localStorage.setItem('user', JSON.stringify(user));
  }

  /**
   * Clear all authentication data from localStorage
   */
  private clearAuthData(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService;
