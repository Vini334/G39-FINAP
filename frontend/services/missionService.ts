/**
 * Mission Service
 * Handles mission progress updates and tracking
 */

import api, { APIResponse, getErrorMessage } from './api';
import { missionTracker, MissionType } from '../utils/missionTracker';

export interface MissionProgressResult {
  success: boolean;
  mission_id: string | null;
  mission_type: string;
  title?: string;
  progress?: number;
  target?: number;
  completed: boolean;
  xp_earned: number;
  coins_earned: number;
  total_xp?: number;
  total_coins?: number;
  level_up: boolean;
  new_level?: number;
  message: string;
}

class MissionService {
  /**
   * Update mission progress by type
   * This is a fire-and-forget operation that shouldn't block the main action
   */
  async updateProgress(
    userId: string,
    missionType: MissionType
  ): Promise<MissionProgressResult | null> {
    try {
      // For missions that should only trigger once per day, check localStorage first
      if (missionType !== 'add_transaction') {
        if (missionTracker.hasTriggeredToday(missionType)) {
          console.log(`Mission ${missionType} already triggered today, skipping API call`);
          return null;
        }
      } else {
        // For add_transaction, check if we've reached the target
        if (!missionTracker.shouldTriggerTransaction()) {
          console.log('Transaction mission target reached, skipping API call');
          return null;
        }
      }

      const response = await api.post<APIResponse<MissionProgressResult>>(
        '/gamification/missions/progress',
        {
          user_id: userId,
          mission_type: missionType,
        }
      );

      const result = response.data.data;

      // Mark as triggered in localStorage
      if (missionType === 'add_transaction') {
        missionTracker.incrementTransactionCount();
      } else {
        missionTracker.markAsTriggered(missionType);
      }

      return result;
    } catch (error) {
      // Log error but don't throw - mission updates shouldn't block main actions
      console.error(`Error updating mission progress for ${missionType}:`, getErrorMessage(error));
      return null;
    }
  }

  /**
   * Trigger daily login mission
   * Should be called after successful login
   */
  async triggerDailyLogin(userId: string): Promise<MissionProgressResult | null> {
    return this.updateProgress(userId, 'daily_login');
  }

  /**
   * Trigger add transaction mission
   * Should be called after successfully adding a transaction
   */
  async triggerAddTransaction(userId: string): Promise<MissionProgressResult | null> {
    return this.updateProgress(userId, 'add_transaction');
  }

  /**
   * Trigger complete quiz mission
   * Should be called after completing a quiz
   */
  async triggerCompleteQuiz(userId: string): Promise<MissionProgressResult | null> {
    return this.updateProgress(userId, 'complete_quiz');
  }

  /**
   * Trigger view report mission
   * Should be called when user opens the Extract/Analysis screen
   */
  async triggerViewReport(userId: string): Promise<MissionProgressResult | null> {
    return this.updateProgress(userId, 'view_report');
  }

  /**
   * Trigger chat with FIM mission
   * Should be called after sending a message to FIM
   */
  async triggerChatFim(userId: string): Promise<MissionProgressResult | null> {
    return this.updateProgress(userId, 'chat_fim');
  }
}

// Export singleton instance
export const missionService = new MissionService();
export default missionService;
