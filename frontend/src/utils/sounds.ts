/**
 * Subtle sound effects using Web Audio API — no external files needed.
 * Each sound is a short synthesized tone.
 * Respects user's sound preference stored in localStorage.
 */

let audioCtx: AudioContext | null = null;

const SOUND_KEY = 'mastercs_sounds_enabled';

function isSoundEnabled(): boolean {
  try {
    return localStorage.getItem(SOUND_KEY) !== 'false';
  } catch {
    return true;
  }
}

export function setSoundEnabled(enabled: boolean): void {
  try {
    localStorage.setItem(SOUND_KEY, String(enabled));
  } catch { /* ignore */ }
}

export function getSoundEnabled(): boolean {
  return isSoundEnabled();
}

function getCtx(): AudioContext {
  if (!audioCtx) audioCtx = new AudioContext();
  return audioCtx;
}

function playTone(freq: number, duration: number, type: OscillatorType = 'sine', volume = 0.12) {
  if (!isSoundEnabled()) return;
  try {
    const ctx = getCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + duration);
  } catch {
    // Audio not available — silent fail
  }
}

export const sounds = {
  correct() {
    playTone(523, 0.1, 'sine', 0.1);
    setTimeout(() => playTone(659, 0.1, 'sine', 0.1), 80);
    setTimeout(() => playTone(784, 0.15, 'sine', 0.12), 160);
  },

  wrong() {
    playTone(300, 0.15, 'square', 0.06);
    setTimeout(() => playTone(250, 0.2, 'square', 0.05), 120);
  },

  select() {
    playTone(440, 0.05, 'sine', 0.04);
  },

  levelUp() {
    const notes = [523, 659, 784, 1047];
    notes.forEach((f, i) => {
      setTimeout(() => playTone(f, 0.15, 'sine', 0.1), i * 100);
    });
  },

  streak() {
    playTone(880, 0.08, 'sine', 0.08);
    setTimeout(() => playTone(1100, 0.12, 'sine', 0.1), 60);
  },

  badge() {
    const notes = [659, 784, 988, 1175];
    notes.forEach((f, i) => {
      setTimeout(() => playTone(f, 0.18, 'triangle', 0.1), i * 120);
    });
  },

  complete() {
    const notes = [523, 659, 784, 1047, 784, 1047];
    notes.forEach((f, i) => {
      setTimeout(() => playTone(f, 0.2, 'sine', 0.08), i * 100);
    });
  },
};
