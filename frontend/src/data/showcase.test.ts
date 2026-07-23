import contract from "./showcase_contract.json";

test("generated showcase contract reconciles governed evidence", () => {
  const locked = contract.evaluation.locked_test.metrics;

  expect(contract.model_info.model_name).toBe(contract.evaluation.selected_model);
  expect(contract.model_info.positive_class).toBe("malignant");
  expect(contract.model_info.calibration_status).toBe("uncalibrated");
  expect(contract.model_info.decision_threshold).toBe(contract.evaluation.threshold.value);
  expect(contract.evaluation.split.row_counts).toEqual({
    train: 398,
    validation: 85,
    locked_test: 86,
  });
  expect(locked.sample_count).toBe(86);
  expect(locked.confusion_matrix).toEqual([
    [locked.true_malignant_count, locked.false_negative_count],
    [locked.false_positive_count, locked.true_benign_count],
  ]);
});
