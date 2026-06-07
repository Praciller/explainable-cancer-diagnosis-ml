# Model Comparison

| Model | Accuracy | Precision | Recall | F1 | Macro F1 | ROC-AUC | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| logistic_regression | 0.9884 | 1.0000 | 0.9688 | 0.9841 | 0.9875 | 0.9954 | 0.9688 | 1.0000 |
| random_forest | 0.8953 | 0.8966 | 0.8125 | 0.8525 | 0.8857 | 0.9797 | 0.8125 | 0.9444 |
| gradient_boosting | 0.9186 | 0.9310 | 0.8438 | 0.8852 | 0.9111 | 0.9757 | 0.8438 | 0.9630 |
| pytorch_mlp | 0.9535 | 0.9375 | 0.9375 | 0.9375 | 0.9502 | 0.9936 | 0.9375 | 0.9630 |
