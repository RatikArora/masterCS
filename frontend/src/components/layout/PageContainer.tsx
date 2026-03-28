import type { ReactNode } from 'react';

export default function PageContainer({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <div className="bg-slate-50 min-h-screen">
      <div className={`max-w-lg mx-auto px-4 pt-6 pb-28 md:pt-8 md:pb-12 ${className}`}>
        {children}
      </div>
    </div>
  );
}
