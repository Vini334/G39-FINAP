/**
 * Transaction Service
 * Handles transaction operations (CRUD)
 */

import api, { APIResponse, getErrorMessage } from './api';
import type {
  Transaction,
  TransactionCreate,
  TransactionUpdate,
  TransactionListResponse,
  Category,
} from '../types/api';

class TransactionService {
  /**
   * Get list of transactions
   */
  async getTransactions(params?: {
    limit?: number;
    offset?: number;
    type?: 'income' | 'expense';
    category?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<TransactionListResponse> {
    try {
      const response = await api.get<APIResponse<TransactionListResponse>>('/transactions', {
        params,
      });

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get a single transaction by ID
   */
  async getTransaction(id: string): Promise<Transaction> {
    try {
      const response = await api.get<APIResponse<{ transaction: Transaction }>>(
        `/transactions/${id}`
      );

      return response.data.data.transaction;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Create a new transaction
   */
  async createTransaction(data: TransactionCreate): Promise<Transaction> {
    try {
      const response = await api.post<APIResponse<{ transaction: Transaction; message: string }>>(
        '/transactions',
        data
      );

      return response.data.data.transaction;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Update a transaction
   */
  async updateTransaction(id: string, data: TransactionUpdate): Promise<Transaction> {
    try {
      const response = await api.put<APIResponse<{ transaction: Transaction }>>(
        `/transactions/${id}`,
        data
      );

      return response.data.data.transaction;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Delete a transaction
   */
  async deleteTransaction(id: string): Promise<void> {
    try {
      await api.delete(`/transactions/${id}`);
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get available categories
   */
  async getCategories(): Promise<Category[]> {
    try {
      const response = await api.get<APIResponse<{ categories: Category[] }>>(
        '/transactions/categories/list'
      );

      return response.data.data.categories;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }
}

// Export singleton instance
export const transactionService = new TransactionService();
export default transactionService;
