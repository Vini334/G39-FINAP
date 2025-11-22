import React from 'react';
import { Home, PieChart, GraduationCap, Users, MessageCircle } from 'lucide-react';
import { ViewState } from '../types';

interface BottomNavProps {
  currentView: ViewState;
  onNavigate: (view: ViewState) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({ currentView, onNavigate }) => {
  const navItems = [
    { id: ViewState.OVERVIEW, icon: Home, label: 'Início' },
    { id: ViewState.EXTRACT, icon: PieChart, label: 'Extrato' },
    { id: ViewState.LEARN, icon: GraduationCap, label: 'Aprender' },
    { id: ViewState.SOCIAL, icon: Users, label: 'Social' },
    { id: ViewState.ASSISTANT, icon: MessageCircle, label: 'FIM' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 pb-6 pt-3 flex justify-around items-center z-50 shadow-[0_-5px_20px_rgba(0,0,0,0.03)]">
      {navItems.map((item) => {
        const isActive = currentView === item.id;
        const Icon = item.icon;
        return (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`flex flex-col items-center gap-1 transition-colors duration-200 ${isActive ? 'text-finap-primary' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <div className={`p-2 rounded-xl transition-all duration-300 ${isActive ? 'bg-purple-50 -translate-y-1' : ''}`}>
              <Icon size={24} strokeWidth={isActive ? 2.5 : 2} />
            </div>
            <span className={`text-[10px] font-semibold transition-opacity ${isActive ? 'opacity-100' : 'opacity-70'}`}>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};