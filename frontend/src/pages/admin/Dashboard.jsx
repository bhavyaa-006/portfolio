import useAuthStore from '../../store/useAuthStore';

export default function Dashboard() {
  const { logout } = useAuthStore();

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <button
          onClick={logout}
          className="bg-destructive text-destructive-foreground px-4 py-2 rounded-md hover:opacity-90 transition-opacity"
        >
          Sign Out
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-card p-6 rounded-xl border shadow-sm">
          <h3 className="text-lg font-medium text-muted-foreground mb-2">Projects</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-card p-6 rounded-xl border shadow-sm">
          <h3 className="text-lg font-medium text-muted-foreground mb-2">Skills</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-card p-6 rounded-xl border shadow-sm">
          <h3 className="text-lg font-medium text-muted-foreground mb-2">Messages</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
      </div>
    </div>
  );
}
