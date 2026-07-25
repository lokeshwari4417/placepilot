import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-semibold text-ink">PlacePilot</h1>
          <p className="text-sm text-muted mt-1">Learn. Practice. Build. Get Hired.</p>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
