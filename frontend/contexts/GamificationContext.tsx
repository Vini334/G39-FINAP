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

const STATS_CACHE_KEY = 'gamification_stats';
const STATS_CACHE_TTL = 60000; // 1 minuto

const GamificationContext = createContext<GamificationContextType | undefined>(undefined);

// Helper para cache de stats
const getCachedStats = (): { stats: GamificationStats; timestamp: number } | null => {
  try {
    const cached = localStorage.getItem(STATS_CACHE_KEY);
    if (cached) {
      return JSON.parse(cached);
    }
  } catch {}
  return null;
};

const setCachedStats = (stats: GamificationStats) => {
  try {
    localStorage.setItem(STATS_CACHE_KEY, JSON.stringify({ stats, timestamp: Date.now() }));
  } catch {}
};

export const GamificationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [stats, setStats] = useState<GamificationStats>(() => {
    // Inicializa com cache se disponível
    const cached = getCachedStats();
    return cached?.stats || defaultStats;
  });
  const [isLoading, setIsLoading] = useState(false);
  const lastFetchRef = React.useRef<number>(0);

  const refreshStats = useCallback(async (force = false) => {
    if (!user?.uid) return;

    // Evita chamadas duplicadas dentro de 2 segundos (debounce)
    const now = Date.now();
    if (!force && now - lastFetchRef.current < 2000) {
      return;
    }
    lastFetchRef.current = now;

    // Verifica cache válido (menos de 1 minuto)
    const cached = getCachedStats();
    if (!force && cached && (now - cached.timestamp) < STATS_CACHE_TTL) {
      setStats(cached.stats);
      return;
    }

    setIsLoading(true);
    try {
      const overview = await dashboardService.getOverview(user.uid);
      if (overview?.stats) {
        const newStats = {
          level: overview.stats.level,
          xp: overview.stats.current_xp,
          xp_percentage: overview.stats.xp_percentage,
          next_level_xp: overview.stats.next_level_xp,
          coins: overview.stats.coins,
          lives: overview.stats.lives,
          max_lives: overview.stats.max_lives,
          streak: overview.stats.streak,
        };
        setStats(newStats);
        setCachedStats(newStats);
      }
    } catch (error) {
      console.error('Error refreshing stats:', error);
    } finally {
      setIsLoading(false);
    }
  }, [user?.uid]);

  useEffect(() => {
    if (user?.uid) {
      // Usa cache primeiro, depois atualiza em background se necessário
      const cached = getCachedStats();
      if (cached) {
        setStats(cached.stats);
        // Se cache tem mais de 1 minuto, atualiza em background
        if (Date.now() - cached.timestamp > STATS_CACHE_TTL) {
          refreshStats(true);
        }
      } else {
        refreshStats(true);
      }
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
