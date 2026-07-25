const NAV_ITEMS = [
  { label: "Dashboard", href: "/" },
  { label: "Roadmap", href: "/roadmap" },
  { label: "Coding Practice", href: "/coding" },
  { label: "Aptitude & Interviews", href: "/aptitude" },
  { label: "Resume", href: "/resume" },
  { label: "Skill Gap", href: "/skills" },
  { label: "Portfolio", href: "/portfolio" },
];

export function Sidebar() {
  return (
    <aside className="hidden md:flex md:w-60 flex-col border-r border-slate-200 bg-white">
      <div className="h-16 flex items-center px-6 font-semibold text-ink">PlacePilot</div>
      <nav className="flex-1 px-3 space-y-1">
        {NAV_ITEMS.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="block rounded-lg px-3 py-2 text-sm text-muted hover:bg-accent-50 hover:text-accent-700 transition-colors"
          >
            {item.label}
          </a>
        ))}
      </nav>
    </aside>
  );
}
