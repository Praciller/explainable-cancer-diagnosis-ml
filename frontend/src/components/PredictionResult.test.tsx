import { render, screen } from "@testing-library/react";

import { PredictionResult } from "./PredictionResult";

test("describes uncalibrated model score and educational boundary", () => {
  render(
    <PredictionResult
      result={{
        model_classification: "malignant",
        raw_target: 0,
        malignant_class_score: 0.72,
        decision_threshold: 0.5,
        calibration_status: "uncalibrated",
        score_interpretation:
          "This is an uncalibrated malignant-class model score. It is not an individual clinical probability.",
        warning_flags: [],
        model_version: "test-version",
        explanation_available: true,
        top_feature_contributions: [
          {
            feature: "mean radius",
            contribution: 0.4,
            direction: "toward_malignant",
          },
        ],
        educational_limitation:
          "This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.",
      }}
    />,
  );

  expect(screen.getByText(/malignant-class model score/i)).toBeVisible();
  expect(screen.getByText(/calibration status:/i)).toBeVisible();
  expect(screen.getByText(/not intended for diagnosis, screening, treatment/i)).toBeVisible();
  expect(screen.queryByText(/model confidence/i)).not.toBeInTheDocument();
});
