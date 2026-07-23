import { render, screen } from "@testing-library/react";

import { DisclaimerBanner } from "./DisclaimerBanner";

test("shows the complete medical safety disclaimer", () => {
  render(<DisclaimerBanner />);

  expect(
    screen.getByText(
      /not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making/i,
    ),
  ).toBeVisible();
});
