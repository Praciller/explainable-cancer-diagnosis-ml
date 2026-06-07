export interface FeatureDefinition {
  name: string;
  minimum: number;
  maximum: number;
  mean: number;
}

export interface SampleRecord {
  id: number;
  known_label: "malignant" | "benign";
  features: Record<string, number>;
}

export interface FeatureContribution {
  feature: string;
  importance: number;
}

export interface PredictionResponse {
  predicted_class: "malignant" | "benign";
  predicted_class_id: number;
  confidence: number;
  probabilities: Record<"malignant" | "benign", number>;
  top_features: FeatureContribution[];
  disclaimer: string;
}

export interface ModelInfo {
  model_name: string;
  problem_type: string;
  features: number;
  classes: string[];
  dataset_version: string;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  macro_f1: number;
  roc_auc: number;
  sensitivity: number;
  specificity: number;
}

export interface EvaluationReport {
  best_test_model: string;
  models: Record<string, ModelMetrics>;
}
