import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';
import type { UserData, LoginRequest, RegisterRequest } from '../types/api';

interface AuthContextType {
  user: UserData | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<{ user: UserData }>;
  register: (data: RegisterRequest) => Promise<{ user: UserData }>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<UserData>) => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          // Cache-first: mostra dados do localStorage imediatamente
          const cachedUser = authService.getUser();
          if (cachedUser) {
            setUser(cachedUser);
            setIsLoading(false); // Libera UI imediatamente com dados em cache

            // Atualiza em background (silencioso)
            authService.getCurrentUser()
              .then(freshUser => setUser(freshUser))
              .catch(() => {}); // Ignora erros na atualização em background
          } else {
            // Sem cache, precisa esperar a API
            const freshUser = await authService.getCurrentUser();
            setUser(freshUser);
            setIsLoading(false);
          }
        } else {
          setIsLoading(false);
        }
      } catch (error) {
        console.error('Auth init error:', error);
        await authService.logout();
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (data: LoginRequest) => {
    const response = await authService.login(data);
    setUser(response.user);
    return { user: response.user };
  };

  const register = async (data: RegisterRequest) => {
    const response = await authService.register(data);
    setUser(response.user);
    return { user: response.user };
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  const updateUser = async (data: Partial<UserData>) => {
    const updatedUser = await authService.updateProfile(data as any);
    setUser(updatedUser);
  };

  const refreshUser = async () => {
    const freshUser = await authService.getCurrentUser();
    setUser(freshUser);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateUser,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
