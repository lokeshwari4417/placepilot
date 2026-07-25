import { useAuth } from "../app/AuthContext";

export function Topbar() {
  const { user, logout } = useAuth();
  return (
    <header className="h-16 border-b border-slate-200 bg-white flex items-center justify-between px-4 md:px-8">
      <div className="text-sm text-muted">Welcome back{user ? `, ${user.email}` : ""}</div>
      <button
        onClick={logout}
        className="text-sm text-muted hover:text-ink transition-colors"
      >
        Log out
      </button>
    </header>
  );
}
