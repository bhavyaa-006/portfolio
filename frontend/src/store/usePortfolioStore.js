import { create } from 'zustand';
import api from '../services/api';

const usePortfolioStore = create((set) => ({
  settings: null,
  projects: [],
  skills: [],
  experience: [],
  education: [],
  loading: false,
  error: null,

  fetchPublicData: async () => {
    set({ loading: true, error: null });
    try {
      const [settingsRes, projectsRes, skillsRes, expRes, eduRes] = await Promise.all([
        api.get('/portfolio/settings'),
        api.get('/portfolio/projects'),
        api.get('/portfolio/skills'),
        api.get('/portfolio/experience'),
        api.get('/portfolio/education'),
      ]);
      set({
        settings: settingsRes.data,
        projects: projectsRes.data,
        skills: skillsRes.data,
        experience: expRes.data,
        education: eduRes.data,
        loading: false,
      });
    } catch (err) {
      console.error('Failed to fetch public portfolio data', err);
      set({
        error: err?.response?.data?.detail || err?.message || 'Unable to load portfolio data',
        loading: false,
      });
    }
  },
}));

export default usePortfolioStore;
