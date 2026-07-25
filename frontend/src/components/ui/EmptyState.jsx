export function EmptyState({ title, description, action }) {
  return (
    <div className="text-center py-12">
      <h3 className="text-sm font-medium text-ink">{title}</h3>
      {description && <p className="text-sm text-muted mt-1">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
