# Error Analysis

Best baseline model: `logistic_regression`.

- False negatives (malignant predicted benign): 1
- False positives (benign predicted malignant): 0
- Other low-confidence predictions: 4

False negatives are the more concerning error in this educational diagnostic framing. Threshold changes trade sensitivity against specificity and cannot establish clinical suitability on this small public dataset.
