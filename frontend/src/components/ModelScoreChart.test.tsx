import { render, screen } from "@testing-library/react";

import { ModelScoreChart } from "./ModelScoreChart";

test("exposes a visible score and threshold alternative beside the chart", () => {
  render(<ModelScoreChart malignantScore={0.72} threshold={0.5} />);

  expect(screen.getByRole("heading", { name: "Malignant-class score" })).toBeVisible();
  expect(screen.getByText("Malignant-class score: 0.720")).toBeVisible();
  expect(screen.getByText("Fixed threshold: 0.50")).toBeVisible();
});
