# Evaluation

Metrics treat malignant (`0`) as the safety-relevant positive class.

- Accuracy: all correct classifications.
- Precision: share of malignant predictions that are malignant.
- Recall and sensitivity: share of malignant rows detected.
- Specificity: share of benign rows identified as benign.
- F1: harmonic mean of malignant precision and recall.
- Macro F1: equal class weighting.
- ROC-AUC: malignant ranking quality across thresholds.

All models use the same 86-row held-out test set.

## Result Interpretation

Logistic Regression achieved 0.9954 ROC-AUC, 0.9688 sensitivity, and 1.0 specificity. It missed one malignant sample. The PyTorch MLP was close in ranking quality at 0.9936 ROC-AUC but made four class errors.

The small test set means individual rows materially affect metrics. Results must not be interpreted as clinical validation.
