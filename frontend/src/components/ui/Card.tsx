import { type ReactNode } from 'react';
import { motion, type HTMLMotionProps } from 'framer-motion';

interface CardProps extends HTMLMotionProps<'div'> {
  children: ReactNode;
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}

const paddings = { sm: 'p-3', md: 'p-4', lg: 'p-5' };

export default function Card({ children, hover = false, padding = 'md', className = '', ...props }: CardProps) {
  return (
    <motion.div
      whileHover={hover ? { y: -1, transition: { duration: 0.2 } } : undefined}
      className={`bg-white rounded-2xl shadow-sm border border-slate-200/60 ${
        hover ? 'hover:shadow-md hover:border-slate-300/60 transition-all duration-200' : ''
      } ${paddings[padding]} ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}
