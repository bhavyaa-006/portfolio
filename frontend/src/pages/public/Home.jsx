import { useEffect } from 'react';
import usePortfolioStore from '../../store/usePortfolioStore';
import Hero from '../../components/sections/Hero';
import Projects from '../../components/sections/Projects';

export default function Home() {
  const { fetchPublicData, loading } = usePortfolioStore();

  useEffect(() => {
    fetchPublicData();
  }, [fetchPublicData]);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div>
      <Hero />
      <Projects />
      {/* Other sections will go here */}
    </div>
  );
}
