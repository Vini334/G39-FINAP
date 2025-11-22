/**
 * FIM Service
 * Handles communication with FIM AI Assistant
 */

import api, { APIResponse, getErrorMessage } from './api';
import type { ChatRequest, ChatResponse, ConversationMessage } from '../types/api';

class FIMService {
  /**
   * Send a message to FIM
   */
  async chat(message: string, includeContext: boolean = true): Promise<ChatResponse> {
    try {
      const request: ChatRequest = {
        message,
        include_context: includeContext,
      };

      const response = await api.post<APIResponse<ChatResponse>>('/fim/chat', request);

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get conversation history
   */
  async getHistory(limit: number = 20): Promise<ConversationMessage[]> {
    try {
      const response = await api.get<APIResponse<{ messages: ConversationMessage[]; total: number }>>(
        '/fim/history',
        { params: { limit } }
      );

      return response.data.data.messages;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Clear conversation history
   */
  async clearHistory(): Promise<void> {
    try {
      await api.delete('/fim/history');
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get suggested questions
   */
  async getSuggestions(): Promise<Record<string, string[]>> {
    try {
      const response = await api.get<APIResponse<{ categories: Record<string, string[]> }>>(
        '/fim/suggestions'
      );

      return response.data.data.categories;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }

  /**
   * Get spending analysis from FIM
   */
  async analyzeSpending(): Promise<{analysis: string; suggestions: string[]}> {
    try {
      const response = await api.post<APIResponse<{analysis: string; suggestions: string[]}>>(
        '/fim/analyze'
      );

      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }
}

// Export singleton instance
export const fimService = new FIMService();
export default fimService;
