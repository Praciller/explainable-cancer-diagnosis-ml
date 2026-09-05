import type { ReactNode } from "react";

type Status = "benign" | "malignant" | "neutral" | "warning";

interface StatusBadgeProps {
  status?: Status;
  children: ReactNode;
}

export function StatusBadge({ status = "neutral", children }: StatusBadgeProps) {
  return <span className={["status-badge", `status-badge-${status}`].join(" ")}>{children}</span>;
}
