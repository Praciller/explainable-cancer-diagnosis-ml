export type ContributionDirection =
  | "toward_malignant"
  | "away_from_malignant"
  | "neutral";

export interface CaseContribution {
  rank: number;
  feature: string;
  value: number;
  contribution: number;
  absolute_contribution: number;
  direction: ContributionDirection;
}

export interface CaseStudyArtifact {
  schema_version: number;
  dataset_row_id: number;
  raw_target: number;
  known_label: string;
  model_name: string;
  model_version: string;
  positive_class: string;
  output_space: string;
  threshold: number;
  calibration_status: string;
  feature_order: string[];
  feature_count: number;
  base_value: number;
  contribution_sum: number;
  reconstructed_log_odds: number;
  model_score: number;
  reconstruction_error: number;
  reconstruction_tolerance: number;
  contributions: CaseContribution[];
  global_explanation: string;
  local_explanation: string;
  educational_limitation: string;
}
