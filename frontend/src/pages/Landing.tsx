import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Brain, RefreshCw, TrendingUp, GraduationCap } from 'lucide-react';
import Button from '../components/ui/Button';

const features = [
  {
    title: 'Concept-First',
    desc: 'Learn the idea before the problems. Build real understanding.',
    icon: <Brain size={22} strokeWidth={1.5} className="text-indigo-600" />,
  },
  {
    title: 'Adaptive Difficulty',
    desc: 'Questions get harder as you improve. Stay in the zone.',
    icon: <Zap size={22} strokeWidth={1.5} className="text-indigo-600" />,
  },
  {
    title: 'Spaced Repetition',
    desc: 'Never forget. Our SM-2 algorithm schedules perfect review timing.',
    icon: <RefreshCw size={22} strokeWidth={1.5} className="text-indigo-600" />,
  },
  {
    title: 'Weakness Targeting',
    desc: 'We push harder on your weak areas so you grow faster.',
    icon: <TrendingUp size={22} strokeWidth={1.5} className="text-indigo-600" />,
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Hero */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-5">
            <GraduationCap size={28} strokeWidth={1.5} className="text-indigo-600" />
          </div>
          <h1 className="text-4xl md:text-5xl font-semibold text-slate-900 mb-4 tracking-tight">
            Master<span className="text-indigo-600">CS</span>
          </h1>
          <p className="text-base text-slate-500 max-w-sm mx-auto mb-10 leading-relaxed">
            Learn Computer Science like a language. Adaptive questions, spaced repetition, 
            and smart tracking — from basics to interview-ready.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link to="/register">
              <Button size="lg" className="px-8">Get Started Free</Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="secondary" className="px-8">Sign In</Button>
            </Link>
          </div>
        </motion.div>
      </div>

      {/* Features */}
      <div className="max-w-2xl mx-auto px-4 pb-20">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.08 }}
              className="bg-slate-50 rounded-2xl p-5 border border-slate-100"
            >
              <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center mb-3">
                {f.icon}
              </div>
              <h3 className="font-semibold text-slate-900 text-sm mb-1">{f.title}</h3>
              <p className="text-sm text-slate-500 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
