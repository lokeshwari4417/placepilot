export function Input({ label, error, className = "", ...props }) {
  return (
    <label className="block">
      {label && <span className="block text-sm font-medium text-ink mb-1">{label}</span>}
      <input
        className={`w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent-500 focus:border-transparent ${className}`}
        {...props}
      />
      {error && <span className="block text-xs text-red-600 mt-1">{error}</span>}
    </label>
  );
}
