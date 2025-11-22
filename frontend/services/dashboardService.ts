/**
 * Dashboard Service
 * Handles dashboard and overview data
 */

import api, { APIResponse, getErrorMessage } from './api';
import type { DashboardOverview } from '../types/api';

class DashboardService {
  /**
   * Get dashboard overview for a user
   */
  async getOverview(userId: string): Promise<DashboardOverview> {
    try {
      const response = await api.get<APIResponse<DashboardOverview>>(
        `/dashboard/overview/${userId}`
      );

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get dashboard summary
   */
  async getSummary(params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<any> {
    try {
      const response = await api.get<APIResponse<any>>('/dashboard/summary', {
        params,
      });

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get additional statistics
   */
  async getStats(): Promise<any> {
    try {
      const response = await api.get<APIResponse<any>>('/dashboard/stats');

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }
}

// Export singleton instance
export const dashboardService = new DashboardService();
export default dashboardService;
