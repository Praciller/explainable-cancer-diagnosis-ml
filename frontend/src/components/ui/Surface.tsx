import type { HTMLAttributes, ReactNode } from "react";

type SurfaceElement = "article" | "div" | "section";

interface SurfaceProps extends HTMLAttributes<HTMLElement> {
  as?: SurfaceElement;
  children: ReactNode;
}

export function Surface({ as = "div", className = "", children, ...props }: SurfaceProps) {
  const Element = as;
  return (
    <Element {...props} className={["surface", className].filter(Boolean).join(" ")}>
      {children}
    </Element>
  );
}
