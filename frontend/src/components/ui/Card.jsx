export function Card({ className = "", children }) {
  return (
    <div className={`bg-white border border-slate-200 rounded-xl p-5 shadow-sm ${className}`}>
      {children}
    </div>
  );
}
