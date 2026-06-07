import type { EvaluationReport, ModelInfo } from "../types/api";

export const SHOWCASE_MODEL_INFO: ModelInfo = {
  model_name: "logistic_regression",
  problem_type: "binary_classification",
  features: 30,
  classes: ["malignant", "benign"],
  dataset_version: "8d2142da4abeaaaa",
};

export const SHOWCASE_EVALUATION: EvaluationReport = {
  best_test_model: "logistic_regression",
  models: {
    logistic_regression: {
      accuracy: 0.9883720930232558,
      precision: 1,
      recall: 0.96875,
      f1: 0.9841269841269841,
      macro_f1: 0.9874763361001893,
      roc_auc: 0.9953703703703703,
      sensitivity: 0.96875,
      specificity: 1,
    },
    random_forest: {
      accuracy: 0.8953488372093024,
      precision: 0.896551724137931,
      recall: 0.8125,
      f1: 0.8524590163934426,
      macro_f1: 0.8856889676561808,
      roc_auc: 0.9797453703703703,
      sensitivity: 0.8125,
      specificity: 0.9444444444444444,
    },
    gradient_boosting: {
      accuracy: 0.9186046511627907,
      precision: 0.9310344827586207,
      recall: 0.84375,
      f1: 0.8852459016393442,
      macro_f1: 0.9110914192881405,
      roc_auc: 0.9756944444444445,
      sensitivity: 0.84375,
      specificity: 0.9629629629629629,
    },
    pytorch_mlp: {
      accuracy: 0.9534883720930233,
      precision: 0.9375,
      recall: 0.9375,
      f1: 0.9375,
      macro_f1: 0.9502314814814814,
      roc_auc: 0.9936342592592593,
      sensitivity: 0.9375,
      specificity: 0.9629629629629629,
    },
  },
};
