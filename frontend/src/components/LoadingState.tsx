import { Skeleton } from "./ui";

export function LoadingState({ label = "Loading model evidence" }: { label?: string }) {
  return (
    <div className="loading-state" role="status">
      <Skeleton label={label} variant="title" />
      <Skeleton label={label} />
      <Skeleton label={label} variant="short" />
      <span className="sr-only">{label}</span>
    </div>
  );
}
