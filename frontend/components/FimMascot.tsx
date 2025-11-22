import React from 'react';

interface FimMascotProps {
  emotion?: 'happy' | 'worried' | 'neutral';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export const FimMascot: React.FC<FimMascotProps> = ({ emotion = 'happy', size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
    xl: 'w-32 h-32',
  };

  return (
    <div className={`relative ${sizeClasses[size]} ${className}`}>
      <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Body/Coin */}
        <circle cx="50" cy="50" r="40" fill="#FFD700" stroke="#E6C200" strokeWidth="4" />
        <circle cx="50" cy="50" r="32" stroke="#F4E695" strokeWidth="2" strokeDasharray="4 4" opacity="0.6" />
        
        {/* Shine */}
        <path d="M60 25 Q 75 25 75 40" stroke="white" strokeWidth="4" strokeLinecap="round" opacity="0.6" />

        {/* Eyes */}
        {emotion === 'worried' ? (
             <>
                <circle cx="35" cy="45" r="4" fill="black" />
                <circle cx="65" cy="45" r="4" fill="black" />
                <path d="M30 35 L40 40" stroke="black" strokeWidth="2" strokeLinecap="round"/>
                <path d="M70 35 L60 40" stroke="black" strokeWidth="2" strokeLinecap="round"/>
             </>
        ) : (
            <>
                <ellipse cx="35" cy="45" rx="4" ry="6" fill="black" />
                <ellipse cx="65" cy="45" rx="4" ry="6" fill="black" />
            </>
        )}

        {/* Mouth */}
        {emotion === 'happy' && (
           <path d="M35 60 Q 50 70 65 60" stroke="black" strokeWidth="3" strokeLinecap="round" fill="none" />
        )}
        {emotion === 'neutral' && (
           <path d="M40 65 L 60 65" stroke="black" strokeWidth="3" strokeLinecap="round" />
        )}
        {emotion === 'worried' && (
           <path d="M35 65 Q 50 55 65 65" stroke="black" strokeWidth="3" strokeLinecap="round" fill="none" />
        )}

        {/* Arms (Doodle Style) */}
        {emotion === 'worried' ? (
             <path d="M10 60 Q 20 40 30 30" stroke="black" strokeWidth="3" strokeLinecap="round" />
        ) : (
             <path d="M10 60 Q 5 40 20 45" stroke="black" strokeWidth="3" strokeLinecap="round" />
        )}
         <path d="M90 60 Q 95 40 80 45" stroke="black" strokeWidth="3" strokeLinecap="round" />

        {/* Legs */}
        <path d="M40 90 L 40 98" stroke="black" strokeWidth="3" strokeLinecap="round" />
        <path d="M60 90 L 60 98" stroke="black" strokeWidth="3" strokeLinecap="round" />
      </svg>
    </div>
  );
};