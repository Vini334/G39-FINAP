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
import { INITIAL_USER_STATS, DAILY_MISSIONS, MOCK_TRANSACTIONS } from './constants';
import { authService } from './services';

const App: React.FC = () => {
  // Verificar autenticação ao iniciar e ao mudar de view
  const [currentView, setCurrentView] = useState<ViewState>(() => {
    const isAuthenticated = authService.isAuthenticated();
    return isAuthenticated ? ViewState.OVERVIEW : ViewState.ONBOARDING;
  });

  // Reavaliar autenticação quando a view mudar
  useEffect(() => {
    const isAuthenticated = authService.isAuthenticated();

    // Se o usuário não está autenticado e está tentando acessar uma view protegida
    if (!isAuthenticated &&
        currentView !== ViewState.ONBOARDING &&
        currentView !== ViewState.LOGIN &&
        currentView !== ViewState.REGISTER) {
      setCurrentView(ViewState.ONBOARDING);
    }
  }, [currentView]);
  
  const renderView = () => {
    switch (currentView) {
      case ViewState.LOGIN:
        return <Login onNavigate={setCurrentView} />;
      case ViewState.REGISTER:
        return <Register onNavigate={setCurrentView} />;
      case ViewState.ONBOARDING:
        // When onboarding finishes, go to Overview
        return <Onboarding onComplete={() => setCurrentView(ViewState.OVERVIEW)} />;
      case ViewState.OVERVIEW:
        return <Overview onNavigate={setCurrentView} />;
      case ViewState.EXTRACT:
        return <Extract />;
      case ViewState.LEARN:
        // Passed stats to Learn for the Lives system
        return <Learn stats={INITIAL_USER_STATS} />;
      case ViewState.SOCIAL:
        return <Social />;
      case ViewState.ASSISTANT:
        return <Assistant />;
      case ViewState.PROFILE:
        return <Profile stats={INITIAL_USER_STATS} onBack={() => setCurrentView(ViewState.OVERVIEW)} onNavigate={setCurrentView} />;
      default:
        return <Overview stats={INITIAL_USER_STATS} missions={DAILY_MISSIONS} onNavigate={setCurrentView} />;
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

export default App;