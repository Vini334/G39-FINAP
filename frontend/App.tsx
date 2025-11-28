import React, { useState, useEffect } from 'react';
import { Overview } from './views/Overview';
import { Extract } from './views/Extract';
import { Learn } from './views/Learn';
import { Social } from './views/Social';
import { Assistant } from './views/Assistant';
import { Profile } from './views/Profile';
import { Onboarding } from './views/Onboarding';
import { Login } from './views/Login';
import { Register } from './views/Register';
import { BottomNav } from './components/BottomNav';
import { ViewState } from './types';
import { AuthProvider, useAuth, GamificationProvider, useGamification } from './contexts';

// Inner App component that uses the contexts
const AppContent: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const { stats } = useGamification();

  const [currentView, setCurrentView] = useState<ViewState>(() => {
    return isAuthenticated ? ViewState.OVERVIEW : ViewState.ONBOARDING;
  });

  // Update view when authentication status changes
  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated &&
          currentView !== ViewState.ONBOARDING &&
          currentView !== ViewState.LOGIN &&
          currentView !== ViewState.REGISTER) {
        setCurrentView(ViewState.ONBOARDING);
      }
    }
  }, [isAuthenticated, isLoading, currentView]);

  // Show loading while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-finap-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-finap-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  const renderView = () => {
    switch (currentView) {
      case ViewState.LOGIN:
        return <Login onNavigate={setCurrentView} />;
      case ViewState.REGISTER:
        return <Register onNavigate={setCurrentView} />;
      case ViewState.ONBOARDING:
        return <Onboarding onComplete={() => setCurrentView(ViewState.OVERVIEW)} />;
      case ViewState.OVERVIEW:
        return <Overview onNavigate={setCurrentView} />;
      case ViewState.EXTRACT:
        return <Extract />;
      case ViewState.LEARN:
        return <Learn stats={stats} />;
      case ViewState.SOCIAL:
        return <Social />;
      case ViewState.ASSISTANT:
        return <Assistant />;
      case ViewState.PROFILE:
        return <Profile stats={stats} onBack={() => setCurrentView(ViewState.OVERVIEW)} onNavigate={setCurrentView} />;
      default:
        return <Overview onNavigate={setCurrentView} />;
    }
  };

  return (
    <div className="min-h-screen bg-finap-bg font-sans text-gray-800 max-w-md mx-auto shadow-2xl relative overflow-hidden">
       {/* Main Content Area */}
       <main className="h-full overflow-y-auto no-scrollbar">
          {renderView()}
       </main>

       {/* Persistent Navigation - Hide on Profile, Onboarding, Login, and Register screens */}
       {currentView !== ViewState.PROFILE &&
        currentView !== ViewState.ONBOARDING &&
        currentView !== ViewState.LOGIN &&
        currentView !== ViewState.REGISTER && (
          <BottomNav currentView={currentView} onNavigate={setCurrentView} />
       )}
    </div>
  );
};

// Main App component with providers
const App: React.FC = () => {
  return (
    <AuthProvider>
      <GamificationProvider>
        <AppContent />
      </GamificationProvider>
    </AuthProvider>
  );
};

export default App;