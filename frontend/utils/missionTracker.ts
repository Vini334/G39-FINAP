/**
 * Mission Tracker Utility
 * Controls daily mission triggers using localStorage to avoid duplicate API calls.
 */

export type MissionType = 'daily_login' | 'add_transaction' | 'complete_quiz' | 'view_report' | 'chat_fim';

export const missionTracker = {
  /**
   * Get the localStorage key for a mission type for today
   */
  getTodayKey: (missionType: MissionType): string => {
    const today = new Date().toISOString().split('T')[0];
    return `finap_mission_${missionType}_${today}`;
  },

  /**
   * Check if a mission has already been triggered today
   */
  hasTriggeredToday: (missionType: MissionType): boolean => {
    // For add_transaction, we track count instead of boolean
    if (missionType === 'add_transaction') {
      return false; // Always allow, we track count separately
    }
    return localStorage.getItem(missionTracker.getTodayKey(missionType)) === 'true';
  },

  /**
   * Mark a mission as triggered for today
   */
  markAsTriggered: (missionType: MissionType): void => {
    localStorage.setItem(missionTracker.getTodayKey(missionType), 'true');
  },

  /**
   * Get the count of transactions added today (for add_transaction mission)
   */
  getTransactionCount: (): number => {
    const key = missionTracker.getTodayKey('add_transaction') + '_count';
    const count = localStorage.getItem(key);
    return count ? parseInt(count, 10) : 0;
  },

  /**
   * Increment transaction count for today
   */
  incrementTransactionCount: (): number => {
    const key = missionTracker.getTodayKey('add_transaction') + '_count';
    const currentCount = missionTracker.getTransactionCount();
    const newCount = currentCount + 1;
    localStorage.setItem(key, newCount.toString());
    return newCount;
  },

  /**
   * Check if should call API for add_transaction (only up to target of 3)
   */
  shouldTriggerTransaction: (): boolean => {
    return missionTracker.getTransactionCount() < 3;
  },

  /**
   * Clean old mission flags from previous days
   */
  cleanOldFlags: (): void => {
    const today = new Date().toISOString().split('T')[0];
    const keysToRemove: string[] = [];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('finap_mission_') && !key.includes(today)) {
        keysToRemove.push(key);
      }
    }

    keysToRemove.forEach(key => localStorage.removeItem(key));
  }
};

export default missionTracker;
