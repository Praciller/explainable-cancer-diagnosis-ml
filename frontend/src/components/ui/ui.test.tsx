import { render, screen } from "@testing-library/react";

import { Button, Callout, Metric, Skeleton, StatusBadge, Surface } from "./index";

describe("UI primitives", () => {
  it("renders button variants and native disabled behavior", () => {
    render(
      <Button variant="secondary" disabled>
        Load sample
      </Button>,
    );

    expect(screen.getByRole("button", { name: "Load sample" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Load sample" })).toHaveClass(
      "button-secondary",
    );
  });

  it("renders a metric with its value and detail", () => {
    render(<Metric label="Rows" value="569" detail="30 features" />);

    expect(screen.getByText("Rows")).toBeVisible();
    expect(screen.getByText("569")).toBeVisible();
    expect(screen.getByText("30 features")).toBeVisible();
  });

  it("gives status labels text beyond their semantic color", () => {
    render(<StatusBadge status="malignant">Malignant class</StatusBadge>);

    expect(screen.getByText("Malignant class")).toHaveClass("status-badge-malignant");
  });

  it("uses alert semantics for error callouts", () => {
    render(
      <Callout tone="error" title="Request failed">
        Try again.
      </Callout>,
    );

    expect(screen.getByRole("alert")).toHaveTextContent("Request failedTry again.");
  });

  it("keeps surfaces structural and skeletons announced", () => {
    render(
      <Surface as="section" aria-label="Evidence panel">
        <Skeleton label="Loading evidence" variant="title" />
      </Surface>,
    );

    expect(screen.getByRole("region", { name: "Evidence panel" })).toHaveClass("surface");
    expect(screen.getByRole("status")).toHaveTextContent("Loading evidence");
  });
});
