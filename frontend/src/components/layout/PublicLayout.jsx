import { Outlet } from 'react-router-dom';

export default function PublicLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary selection:text-primary-foreground">
      {/* Navigation will go here */}
      <main>
        <Outlet />
      </main>
      {/* Footer will go here */}
    </div>
  );
}
