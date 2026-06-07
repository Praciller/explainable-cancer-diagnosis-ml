# EDA Summary

The dataset contains 569 samples and 30 numeric features. Benign samples are more common, but the class ratio is mild and stratified splitting preserves both classes.

## Strongest Relationships

- `worst concave points`: target correlation 0.794
- `worst perimeter`: target correlation 0.783
- `mean concave points`: target correlation 0.777
- `worst radius`: target correlation 0.776
- `mean perimeter`: target correlation 0.743
- `worst area`: target correlation 0.734
- `mean radius`: target correlation 0.730
- `mean area`: target correlation 0.709

## Leakage and Overfitting Risks

Features are measurements from the same digitized image and several are strongly correlated. Splitting must happen by row before fitting scalers. The small, clean dataset can overstate real-world performance and does not provide external clinical validation.
