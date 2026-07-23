# Evaluation contract

Malignant (`0`) is the safety-relevant positive class. Metrics are recomputed from `reports/locked_test_predictions.csv`, never averaged from rounded values.

- balanced accuracy gives equal weight to malignant and benign recall;
- malignant precision describes the share of malignant classifications that are malignant rows;
- malignant recall or sensitivity describes malignant rows classified as malignant;
- specificity describes benign rows classified as benign;
- malignant F1 combines malignant precision and recall;
- ROC-AUC measures malignant-score ranking across thresholds;
- PR-AUC emphasizes malignant-class retrieval under class imbalance.

The selected Logistic Regression uses threshold `0.50` and is uncalibrated. On 86 governed regression rows:

- matrix `[[31, 1], [0, 54]]`, rows actual and columns model classification in malignant/benign order;
- 1 malignant-to-benign error and 0 benign-to-malignant errors;
- sensitivity `0.9688`, specificity `1.0000`;
- balanced accuracy `0.9844`, malignant F1 `0.9841`;
- ROC-AUC `0.9954`, PR-AUC `0.9938`.

The small test set and prior exposure mean each row materially affects the metrics. These values do not encode clinical utility or establish safety.
