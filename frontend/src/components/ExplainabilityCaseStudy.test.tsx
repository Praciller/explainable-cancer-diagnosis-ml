import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import caseArtifact from "../data/explainability_case.json";
import type { CaseStudyArtifact } from "../types/explainability";
import { ExplainabilityCaseStudy } from "./ExplainabilityCaseStudy";

const typedCaseArtifact = caseArtifact as unknown as CaseStudyArtifact;

describe("ExplainabilityCaseStudy", () => {
  it("shows the governed summary and score reconstruction", () => {
    render(<ExplainabilityCaseStudy artifact={typedCaseArtifact} />);

    expect(
      screen.getByRole("heading", { name: /row 102 explainability case study/i }),
    ).toBeVisible();
    expect(screen.getByText("logistic_regression")).toBeVisible();
    expect(screen.getByText("0.008")).toBeVisible();
    expect(screen.getByText(/base value.*local contributions.*malignant-class log-odds/i)).toBeVisible();
    expect(screen.getByText(/Calibration status: uncalibrated/i)).toBeVisible();
    expect(screen.getByText(typedCaseArtifact.educational_limitation)).toBeVisible();
  });

  it("expands from the top eight to all thirty contributions", async () => {
    const user = userEvent.setup();
    render(<ExplainabilityCaseStudy artifact={typedCaseArtifact} />);

    expect(screen.getAllByRole("button", { name: /feature contribution/i })).toHaveLength(8);
    const expandButton = screen.getByRole("button", { name: /show all 30 contributions/i });
    expect(expandButton).toHaveAttribute("aria-expanded", "false");
    await user.click(expandButton);

    expect(screen.getAllByRole("button", { name: /feature contribution/i })).toHaveLength(30);
    expect(expandButton).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByRole("button", { name: /show top 8 contributions/i })).toBeVisible();
  });

  it("selects a feature with the keyboard and shows signed detail", async () => {
    const user = userEvent.setup();
    render(<ExplainabilityCaseStudy artifact={typedCaseArtifact} />);

    const feature = screen.getByRole("button", { name: /worst texture feature contribution/i });
    feature.focus();
    await user.keyboard("{Enter}");

    const detail = screen.getByRole("region", { name: /selected feature detail/i });
    expect(detail).toHaveTextContent("worst texture");
    expect(detail).toHaveTextContent("32.840");
    expect(detail).toHaveTextContent("+1.470");
    expect(detail).toHaveTextContent("Toward malignant");
    expect(detail).toHaveTextContent(/model behavior.*rather than causality/i);
    expect(feature).toHaveAttribute("aria-pressed", "true");
  });

  it("explains global versus local meaning without clinical claims", () => {
    render(<ExplainabilityCaseStudy artifact={typedCaseArtifact} />);
    const section = screen.getByRole("region", { name: /interactive explainability case study/i });

    expect(section).toHaveTextContent(/global importance summarizes recurring model behavior/i);
    expect(section).toHaveTextContent(/local contributions describe how this supplied dataset row/i);
    expect(section).toHaveTextContent(/correlated measurements can share or redistribute importance/i);
    expect(section).toHaveTextContent(/do not prove biological causality/i);
    expect(section).not.toHaveTextContent(/patient|risk score|model confidence/i);
  });

  it("supports pointer selection as well as keyboard selection", () => {
    render(<ExplainabilityCaseStudy artifact={typedCaseArtifact} />);
    const feature = screen.getByRole("button", { name: /mean compactness feature contribution/i });

    fireEvent.click(feature);

    expect(feature).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("region", { name: /selected feature detail/i })).toHaveTextContent(
      "mean compactness",
    );
  });
});
