# Data Validation Report

## Summary

- Rows: 569
- Numeric features: 30
- Duplicate feature rows: 0
- Missing values: 0
- Class ratio: 1.68
- Assessment: Class imbalance is mild and is handled with stratified splits.

## Target Distribution

| label     |   count |
|:----------|--------:|
| benign    |     357 |
| malignant |     212 |

## Missing Values

|                         |   count |
|:------------------------|--------:|
| mean radius             |       0 |
| mean texture            |       0 |
| mean perimeter          |       0 |
| mean area               |       0 |
| mean smoothness         |       0 |
| mean compactness        |       0 |
| mean concavity          |       0 |
| mean concave points     |       0 |
| mean symmetry           |       0 |
| mean fractal dimension  |       0 |
| radius error            |       0 |
| texture error           |       0 |
| perimeter error         |       0 |
| area error              |       0 |
| smoothness error        |       0 |
| compactness error       |       0 |
| concavity error         |       0 |
| concave points error    |       0 |
| symmetry error          |       0 |
| fractal dimension error |       0 |
| worst radius            |       0 |
| worst texture           |       0 |
| worst perimeter         |       0 |
| worst area              |       0 |
| worst smoothness        |       0 |
| worst compactness       |       0 |
| worst concavity         |       0 |
| worst concave points    |       0 |
| worst symmetry          |       0 |
| worst fractal dimension |       0 |
| target                  |       0 |
| label                   |       0 |

## Feature Data Types

|                         | dtype   |
|:------------------------|:--------|
| mean radius             | float64 |
| mean texture            | float64 |
| mean perimeter          | float64 |
| mean area               | float64 |
| mean smoothness         | float64 |
| mean compactness        | float64 |
| mean concavity          | float64 |
| mean concave points     | float64 |
| mean symmetry           | float64 |
| mean fractal dimension  | float64 |
| radius error            | float64 |
| texture error           | float64 |
| perimeter error         | float64 |
| area error              | float64 |
| smoothness error        | float64 |
| compactness error       | float64 |
| concavity error         | float64 |
| concave points error    | float64 |
| symmetry error          | float64 |
| fractal dimension error | float64 |
| worst radius            | float64 |
| worst texture           | float64 |
| worst perimeter         | float64 |
| worst area              | float64 |
| worst smoothness        | float64 |
| worst compactness       | float64 |
| worst concavity         | float64 |
| worst concave points    | float64 |
| worst symmetry          | float64 |
| worst fractal dimension | float64 |

## Numeric Feature Ranges

|                         |      min |       max |
|:------------------------|---------:|----------:|
| mean radius             |   6.9810 |   28.1100 |
| mean texture            |   9.7100 |   39.2800 |
| mean perimeter          |  43.7900 |  188.5000 |
| mean area               | 143.5000 | 2501.0000 |
| mean smoothness         |   0.0526 |    0.1634 |
| mean compactness        |   0.0194 |    0.3454 |
| mean concavity          |   0.0000 |    0.4268 |
| mean concave points     |   0.0000 |    0.2012 |
| mean symmetry           |   0.1060 |    0.3040 |
| mean fractal dimension  |   0.0500 |    0.0974 |
| radius error            |   0.1115 |    2.8730 |
| texture error           |   0.3602 |    4.8850 |
| perimeter error         |   0.7570 |   21.9800 |
| area error              |   6.8020 |  542.2000 |
| smoothness error        |   0.0017 |    0.0311 |
| compactness error       |   0.0023 |    0.1354 |
| concavity error         |   0.0000 |    0.3960 |
| concave points error    |   0.0000 |    0.0528 |
| symmetry error          |   0.0079 |    0.0790 |
| fractal dimension error |   0.0009 |    0.0298 |
| worst radius            |   7.9300 |   36.0400 |
| worst texture           |  12.0200 |   49.5400 |
| worst perimeter         |  50.4100 |  251.2000 |
| worst area              | 185.2000 | 4254.0000 |
| worst smoothness        |   0.0712 |    0.2226 |
| worst compactness       |   0.0273 |    1.0580 |
| worst concavity         |   0.0000 |    1.2520 |
| worst concave points    |   0.0000 |    0.2910 |
| worst symmetry          |   0.1565 |    0.6638 |
| worst fractal dimension |   0.0550 |    0.2075 |

## Outlier Summary

Counts use a simple three-standard-deviation screen and are descriptive, not grounds for automatic removal.

|                         |   count |
|:------------------------|--------:|
| mean radius             |       5 |
| mean texture            |       4 |
| mean perimeter          |       7 |
| mean area               |       8 |
| mean smoothness         |       5 |
| mean compactness        |       9 |
| mean concavity          |       9 |
| mean concave points     |       6 |
| mean symmetry           |       5 |
| mean fractal dimension  |       7 |
| radius error            |       7 |
| texture error           |       9 |
| perimeter error         |       8 |
| area error              |       6 |
| smoothness error        |       7 |
| compactness error       |      12 |
| concavity error         |       6 |
| concave points error    |       6 |
| symmetry error          |      11 |
| fractal dimension error |      10 |
| worst radius            |       6 |
| worst texture           |       4 |
| worst perimeter         |       6 |
| worst area              |      10 |
| worst smoothness        |       3 |
| worst compactness       |      10 |
| worst concavity         |       7 |
| worst concave points    |       0 |
| worst symmetry          |       9 |
| worst fractal dimension |       9 |
