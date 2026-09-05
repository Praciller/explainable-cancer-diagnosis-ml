type SkeletonVariant = "line" | "short" | "title";

interface SkeletonProps {
  label: string;
  variant?: SkeletonVariant;
}

export function Skeleton({ label, variant = "line" }: SkeletonProps) {
  return (
    <div className={["skeleton", `skeleton-${variant}`].join(" ")} role="status">
      <span className="sr-only">{label}</span>
    </div>
  );
}
