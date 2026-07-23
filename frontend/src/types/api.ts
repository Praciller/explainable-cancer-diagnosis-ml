export type NormalizedLabel = "malignant" | "benign";

export interface FeatureDefinition {
  name: string;
  minimum: number;
  maximum: number;
  mean: number;
  measurement_context: string;
}

export interface SampleRecord {
  dataset_row_id: number;
  known_label: NormalizedLabel;
  features: Record<string, number>;
}

export interface FeatureContribution {
  feature: string;
  contribution: number;
  direction: "toward_malignant" | "toward_benign" | "magnitude_only";
}

export interface PredictionResponse {
  model_classification: NormalizedLabel;
  raw_target: 0 | 1;
  malignant_class_score: number;
  decision_threshold: number;
  calibration_status: "uncalibrated";
  score_interpretation: string;
  warning_flags: string[];
  model_version: string;
  explanation_available: boolean;
  top_feature_contributions: FeatureContribution[];
  educational_limitation: string;
}

export interface ModelInfo {
  model_name: string;
  problem_type: "binary_classification";
  features: number;
  classes: string[];
  positive_class: "malignant";
  dataset_fingerprint: string;
  model_version: string;
  decision_threshold: number;
  calibration_status: "uncalibrated";
  educational_limitation: string;
}

export interface ModelMetrics {
  sample_count: number;
  threshold: number;
  accuracy: number;
  balanced_accuracy: number;
  malignant_precision: number;
  malignant_recall: number;
  malignant_f1: number;
  macro_f1: number;
  roc_auc: number;
  pr_auc: number;
  sensitivity: number;
  specificity: number;
  false_negative_count: number;
  false_positive_count: number;
  confusion_matrix: number[][];
}

export interface EvaluationReport {
  selected_model: string;
  selection: {
    metric: string;
    value: number;
  };
  split?: {
    seed: number;
    row_counts: {
      train: number;
      validation: number;
      locked_test: number;
    };
    assignment_sha256: string;
  };
  threshold: {
    value: number;
    source: string;
  };
  calibration_status: "uncalibrated";
  validation_models: Record<string, ModelMetrics>;
  locked_test: {
    status: string;
    evaluated_at: string;
    metrics: ModelMetrics;
  };
}
