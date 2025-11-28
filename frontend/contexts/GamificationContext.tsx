import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { dashboardService } from '../services/dashboardService';
import { useAuth } from './AuthContext';

export interface GamificationStats {
  level: number;
  xp: number;
  xp_percentage: number;
  next_level_xp: number;
  coins: number;
  lives: number;
  max_lives: number;
  streak: number;
}

interface GamificationContextType {
  stats: GamificationStats;
  isLoading: boolean;
  refreshStats: () => Promise<void>;
  addXP: (amount: number) => void;
  addCoins: (amount: number) => void;
  removeLife: () => void;
}

const defaultStats: GamificationStats = {
  level: 1,
  xp: 0,
  xp_percentage: 0,
  next_level_xp: 100,
  coins: 100,
  lives: 5,
  max_lives: 5,
  streak: 0,
};

const GamificationContext = createContext<GamificationContextType | undefined>(undefined);

export const GamificationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [stats, setStats] = useState<GamificationStats>(defaultStats);
  const [isLoading, setIsLoading] = useState(false);

  const refreshStats = useCallback(async () => {
    if (!user?.uid) return;

    setIsLoading(true);
    try {
      const overview = await dashboardService.getOverview(user.uid);
      if (overview?.stats) {
        setStats({
          level: overview.stats.level,
          xp: overview.stats.current_xp,
          xp_percentage: overview.stats.xp_percentage,
          next_level_xp: overview.stats.next_level_xp,
          coins: overview.stats.coins,
          lives: overview.stats.lives,
          max_lives: overview.stats.max_lives,
          streak: overview.stats.streak,
        });
      }
    } catch (error) {
      console.error('Error refreshing stats:', error);
    } finally {
      setIsLoading(false);
    }
  }, [user?.uid]);

  useEffect(() => {
    if (user?.uid) {
      refreshStats();
    }
  }, [user?.uid, refreshStats]);

  const addXP = (amount: number) => {
    setStats(prev => {
      const newXP = prev.xp + amount;
      const newLevel = Math.floor(newXP / 100) + 1;
      return {
        ...prev,
        xp: newXP % 100,
        level: newLevel,
        xp_percentage: (newXP % 100),
      };
    });
  };

  const addCoins = (amount: number) => {
    setStats(prev => ({
      ...prev,
      coins: prev.coins + amount,
    }));
  };

  const removeLife = () => {
    setStats(prev => ({
      ...prev,
      lives: Math.max(0, prev.lives - 1),
    }));
  };

  return (
    <GamificationContext.Provider
      value={{
        stats,
        isLoading,
        refreshStats,
        addXP,
        addCoins,
        removeLife,
      }}
    >
      {children}
    </GamificationContext.Provider>
  );
};

export const useGamification = (): GamificationContextType => {
  const context = useContext(GamificationContext);
  if (context === undefined) {
    throw new Error('useGamification must be used within a GamificationProvider');
  }
  return context;
};
