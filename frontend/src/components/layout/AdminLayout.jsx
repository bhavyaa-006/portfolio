import { Outlet, Navigate } from 'react-router-dom';
import useAuthStore from '../../store/useAuthStore';

export default function AdminLayout() {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-muted/40">
      {/* Admin Sidebar will go here */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}
