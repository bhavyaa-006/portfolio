import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';

function getInitials(name) {
  if (!name) {
    return 'P';
  }

  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('');
}

export default function AvatarRotator({ name, src }) {
  const [activeFace, setActiveFace] = useState(0);
  const [hasImageError, setHasImageError] = useState(false);

  const trimmedSrc = typeof src === 'string' ? src.trim() : '';
  const canShowPhoto = Boolean(trimmedSrc) && !hasImageError;
  const initials = getInitials(name);
  const faces = canShowPhoto ? ['photo', 'badge'] : ['badge'];

  useEffect(() => {
    if (!canShowPhoto) {
      setActiveFace(0);
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      setActiveFace((current) => (current + 1) % 2);
    }, 4500);

    return () => window.clearInterval(intervalId);
  }, [canShowPhoto]);

  useEffect(() => {
    setActiveFace(0);
    setHasImageError(false);
  }, [src, name]);

  return (
    <motion.div
      initial={{ scale: 0.92, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.55, ease: 'easeOut' }}
      className="relative h-36 w-36 overflow-hidden rounded-full border border-white/20 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 shadow-[0_30px_80px_rgba(15,23,42,0.35)] md:h-44 md:w-44"
    >
      <div className="absolute inset-0 rounded-full bg-gradient-to-br from-primary/30 via-transparent to-secondary/30 blur-2xl" />
      <AnimatePresence mode="wait">
        {faces[activeFace] === 'photo' ? (
          <motion.img
            key="photo"
            src={trimmedSrc}
            alt={name}
            onError={() => setHasImageError(true)}
            initial={{ opacity: 0, scale: 1.05 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.35 }}
            className="relative z-10 h-full w-full object-cover"
          />
        ) : (
          <motion.div
            key="badge"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.96 }}
            transition={{ duration: 0.35 }}
            className="relative z-10 flex h-full w-full items-center justify-center bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.18),_rgba(15,23,42,0.95)_55%)]"
          >
            <span className="text-4xl font-semibold tracking-[0.25em] text-white md:text-5xl">
              {initials}
            </span>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}