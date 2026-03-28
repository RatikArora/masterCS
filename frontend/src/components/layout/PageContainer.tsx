import type { ReactNode } from 'react';

export default function PageContainer({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <div className={`max-w-2xl mx-auto px-4 py-6 pb-24 md:pb-8 ${className}`}>
      {children}
    </div>
  );
}
