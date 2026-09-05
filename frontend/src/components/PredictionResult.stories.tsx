import type { Meta, StoryObj } from "@storybook/react-vite";

import type { PredictionResponse } from "../types/api";
import { PredictionResult } from "./PredictionResult";

const fixture: PredictionResponse = {
  model_classification: "malignant",
  raw_target: 0,
  malignant_class_score: 0.72,
  decision_threshold: 0.5,
  calibration_status: "uncalibrated",
  score_interpretation: "This is an uncalibrated malignant-class model score.",
  warning_flags: [],
  model_version: "storybook-fixture",
  explanation_available: true,
  top_feature_contributions: [
    { feature: "mean radius", contribution: 0.4, direction: "toward_malignant" },
    { feature: "mean texture", contribution: -0.18, direction: "toward_benign" },
  ],
  educational_limitation:
    "This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.",
};

const meta = {
  title: "Domain/PredictionResult",
  component: PredictionResult,
  tags: ["autodocs"],
  args: { result: fixture },
} satisfies Meta<typeof PredictionResult>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Malignant: Story = {};
export const Benign: Story = {
  args: { result: { ...fixture, model_classification: "benign", raw_target: 1, malignant_class_score: 0.21 } },
};
export const WithInputWarning: Story = {
  args: { result: { ...fixture, warning_flags: ["outside_observed_training_range:mean radius"] } },
};
