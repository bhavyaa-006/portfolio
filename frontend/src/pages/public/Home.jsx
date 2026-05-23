import { useEffect } from 'react';
import usePortfolioStore from '../../store/usePortfolioStore';
import Hero from '../../components/sections/Hero';
import Projects from '../../components/sections/Projects';
import Startup from '../../components/sections/Startup';

export default function Home() {
  const { fetchPublicData, loading, error } = usePortfolioStore();

  useEffect(() => {
    fetchPublicData();
  }, [fetchPublicData]);

  if (loading) {
    return <Startup />;
  }

  return (
    <div className="space-y-0">
      {error && (
        <div className="mx-auto mt-4 max-w-5xl px-4">
          <div className="rounded-2xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-900 dark:text-amber-100">
            {error}
          </div>
        </div>
      )}
      <Hero />
      <Projects />
      {/* Other sections will go here */}
    </div>
  );
}
