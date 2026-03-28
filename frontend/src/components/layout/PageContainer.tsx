import type { ReactNode } from 'react';

export default function PageContainer({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <div className={`bg-slate-50 min-h-screen`}>
      <div className={`max-w-lg mx-auto px-4 py-6 pb-24 md:pb-8 ${className}`}>
        {children}
      </div>
    </div>
  );
}
