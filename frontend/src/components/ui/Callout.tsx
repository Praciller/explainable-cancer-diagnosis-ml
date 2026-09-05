import type { ReactNode } from "react";

type CalloutTone = "disclaimer" | "error" | "info" | "warning";

interface CalloutProps {
  tone?: CalloutTone;
  title: string;
  children: ReactNode;
  icon?: ReactNode;
}

const calloutRole: Record<CalloutTone, "alert" | "status" | undefined> = {
  disclaimer: undefined,
  error: "alert",
  info: "status",
  warning: "status",
};

export function Callout({ tone = "info", title, children, icon }: CalloutProps) {
  return (
    <aside
      className={["callout", `callout-${tone}`].join(" ")}
      role={calloutRole[tone]}
      aria-label={title}
    >
      {icon}
      <div>
        <strong>{title}</strong>
        {children}
      </div>
    </aside>
  );
}
