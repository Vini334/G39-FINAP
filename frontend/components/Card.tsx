import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  title?: string;
  action?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ children, className = '', onClick, title, action }) => {
  return (
    <div 
      onClick={onClick}
      // Added border-slate-100 to separate from the light gray background
      className={`bg-white rounded-xl shadow-sm border border-slate-100 p-5 mb-4 ${onClick ? 'cursor-pointer active:scale-[0.98] transition-transform hover:border-finap-primary/30' : ''} ${className}`}
    >
      {(title || action) && (
        <div className="flex justify-between items-center mb-3">
          {title && <h3 className="font-bold text-finap-dark text-lg tracking-tight">{title}</h3>}
          {action}
        </div>
      )}
      {children}
    </div>
  );
};