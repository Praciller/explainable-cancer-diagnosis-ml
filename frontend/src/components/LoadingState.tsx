export function LoadingState({ label = "Loading model evidence" }: { label?: string }) {
  return (
    <div className="loading-state" role="status">
      <div className="skeleton skeleton-title" />
      <div className="skeleton" />
      <div className="skeleton skeleton-short" />
      <span className="sr-only">{label}</span>
    </div>
  );
}
