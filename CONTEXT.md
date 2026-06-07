# Explainable Cancer Diagnosis ML

This context defines the educational model workflow and prevents clinical terminology from overstating what the system does.

## Language

**Model output**:
The class probabilities and predicted class produced by a trained portfolio model.
_Avoid_: Diagnosis, medical result

**Sample**:
One dataset row containing all 30 numeric features derived from a digitized breast-mass image.
_Avoid_: Patient, case

**Malignant class**:
Dataset target `0`, verified from scikit-learn's target names.
_Avoid_: Positive diagnosis

**Benign class**:
Dataset target `1`, verified from scikit-learn's target names.
_Avoid_: Negative diagnosis

**Top feature contribution**:
A model-specific directional or global importance value used to explain a model output.
_Avoid_: Cause, clinical factor

## Example Dialogue

Developer: "Which sample should the dashboard load?"

Data scientist: "Load a complete 30-feature sample, then display its model output and top feature contributions."

Developer: "Should the result say diagnosis?"

Data scientist: "No. It is a model prediction from an educational dataset, not a clinical diagnosis."
