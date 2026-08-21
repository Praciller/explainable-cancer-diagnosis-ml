# Project Requirements: Explainable Breast Cancer Diagnostic ML

## 1. Project Summary

### Recommended Repository Name

`explainable-cancer-diagnosis-ml`

Alternative names:

```txt
breast-cancer-risk-explainability
diagnostic-ml-explainability
tabular-ml-risk-classifier
```

### Project Type

Data Science / Tabular Machine Learning / Explainable AI / ML API portfolio project.

### Main Goal

Build an end-to-end machine learning system that predicts whether a tumor sample is malignant or benign using the built-in Breast Cancer Wisconsin Diagnostic dataset from scikit-learn, then explains predictions using model interpretation techniques.

This project should demonstrate practical Data Scientist and Machine Learning Engineer skills beyond notebooks:

```txt
EDA → preprocessing → baseline ML → advanced ML → PyTorch MLP → evaluation → explainability → FastAPI inference → React dashboard → Docker → MLflow
```

### Important Disclaimer

This project is for educational and portfolio purposes only. It must not be presented as a real medical diagnosis tool.

The README and UI must clearly state:

```txt
This system is a machine learning portfolio demo and is not intended for medical diagnosis or clinical decision-making.
```

---

## 2. Why This Project

This project fills a useful gap in the existing portfolio by focusing on:

- Tabular machine learning
- Binary classification
- Classification metrics beyond accuracy
- Model comparison
- Feature importance
- SHAP explainability
- MLflow experiment tracking
- Production-style inference API
- React dashboard for model interpretation

It is different from NLP projects, procurement analytics, POS systems, and general AI app projects.

---

## 3. Dataset

### Primary Dataset

Use the Breast Cancer Wisconsin Diagnostic dataset from scikit-learn.

### Why This Dataset

This dataset is recommended because:

- It is included with scikit-learn.
- It does not require Kaggle.
- It does not require login.
- It does not require scraping.
- It does not depend on an unstable external URL.
- It works offline after installing scikit-learn.
- It is suitable for binary classification and explainable AI.

### Access Method

Install scikit-learn:

```bash
pip install scikit-learn
```

Load dataset:

```python
from sklearn.datasets import load_breast_cancer

dataset = load_breast_cancer(as_frame=True)
X = dataset.data
y = dataset.target
```

### Dataset Target

The target is binary:

```txt
0 = malignant
1 = benign
```

The project must verify this mapping from `dataset.target_names`.

### Dataset Features

The dataset contains numeric features computed from digitized images of breast mass cell nuclei.

Example feature groups:

```txt
mean radius
mean texture
mean perimeter
mean area
mean smoothness
mean compactness
mean concavity
mean concave points
mean symmetry
mean fractal dimension
```

The dataset has 30 numeric features.

### Data Storage

The project should save a local copy after loading:

```txt
data/raw/breast_cancer_raw.csv
data/processed/breast_cancer_processed.csv
```

---

## 4. Tech Stack

### Required

```txt
Python 3.10+
pandas
numpy
scikit-learn
PyTorch
FastAPI
Uvicorn
Pydantic
React
Vite
TypeScript
Tailwind CSS
Recharts
matplotlib
joblib
```

### Strongly Recommended Optional

These are worth using in this project:

```txt
SHAP
MLflow local tracking
Docker
```

### Not Required for Version 1

```txt
TensorFlow
Database
Authentication
Paid cloud services
Kubernetes
Airflow
External API
Large model storage
```

### Optional Decision

| Tool | Use? | Reason |
|---|---:|---|
| React + Vite | Yes | Lightweight dashboard frontend |
| PyTorch | Yes | Useful for building a neural network on tabular data |
| SHAP | Yes | Very suitable for tabular model explainability |
| MLflow | Yes, local only | Good for tracking experiments and metrics |
| Docker | Yes | Good for reproducible portfolio demo |
| TensorFlow | No for v1 | Avoid duplicating deep learning framework complexity |
| PostgreSQL | No | Dataset is small and local CSV is enough |
| Airflow/Prefect | No | Too heavy for this project |
| Paid GPU | No | Dataset is small; CPU is enough |

---

## 5. Functional Requirements

## 5.1 Data Loading

The system must load the dataset from scikit-learn.

### Required Script

```txt
src/data/load_dataset.py
```

### Requirements

- Load dataset with `load_breast_cancer(as_frame=True)`.
- Convert features and target into a pandas DataFrame.
- Add a human-readable label column.
- Save raw data to CSV.
- Save dataset metadata to markdown.

### Output

```txt
data/raw/breast_cancer_raw.csv
reports/dataset_metadata.md
```

### Acceptance Criteria

- The dataset can be loaded without internet access after dependencies are installed.
- The script creates `data/raw/breast_cancer_raw.csv`.
- The metadata report includes feature names, target names, row count, and column count.

---

## 5.2 Data Validation

The system must validate the dataset before training.

### Required Checks

- Missing values
- Duplicate rows
- Target distribution
- Feature data types
- Numeric feature ranges
- Outlier summary
- Class imbalance summary

### Required Script

```txt
src/data/validate_dataset.py
```

### Output

```txt
reports/data_validation_report.md
```

### Acceptance Criteria

- The validation report is generated in markdown.
- The report includes class distribution and missing values.
- The report explains whether class imbalance is a major issue.

---

## 5.3 Exploratory Data Analysis

The project must include EDA.

### Required Notebook

```txt
notebooks/01_eda.ipynb
```

### Required EDA

- Dataset shape
- Target distribution
- Summary statistics
- Feature correlation heatmap
- Top correlated features with target
- Distribution of important features by class
- Pairwise comparison for selected features
- Notes on possible data leakage or overfitting risks

### Output

```txt
reports/eda_summary.md
reports/figures/target_distribution.png
reports/figures/correlation_heatmap.png
reports/figures/top_feature_distributions.png
```

### Acceptance Criteria

- EDA notebook can run from top to bottom.
- At least 3 figures are saved.
- EDA summary explains important findings in plain English.

---

## 5.4 Preprocessing and Feature Engineering

The project must implement reusable preprocessing.

### Required Processing

- Train/validation/test split
- Stratified split
- Standard scaling for linear models and PyTorch MLP
- No scaling required for tree-based models
- Pipeline-based preprocessing using scikit-learn
- Save fitted preprocessors when needed

### Required Script

```txt
src/features/preprocess.py
```

### Acceptance Criteria

- Preprocessing is not hardcoded in notebooks only.
- The same split is used across all models.
- Random seed is configurable.
- Data leakage is avoided by fitting scaler only on training data.

---

## 5.5 Baseline Machine Learning Models

Train baseline models using scikit-learn.

### Required Models

```txt
Logistic Regression
Random Forest Classifier
Gradient Boosting Classifier
```

### Optional Model

```txt
XGBoost Classifier
```

Only add XGBoost if dependency setup is simple. The project must still work without XGBoost.

### Required Script

```txt
src/models/train_baseline.py
```

### Requirements

- Train multiple models.
- Use the same train/validation/test split.
- Save model artifacts.
- Save metrics.
- Select the best model based on validation ROC-AUC or macro F1.
- Save the best model as `models/best_model.joblib`.

### Output

```txt
models/logistic_regression.joblib
models/random_forest.joblib
models/gradient_boosting.joblib
models/best_model.joblib
reports/baseline_metrics.json
reports/model_comparison.md
```

### Acceptance Criteria

- Training runs from CLI.
- Model metrics are saved.
- Best model is clearly identified.
- Model comparison table exists.

---

## 5.6 PyTorch MLP Model

Build a neural network model for tabular classification using PyTorch.

### Required Model

A simple Multi-Layer Perceptron.

Example architecture:

```txt
Input layer: 30 features
Hidden layer 1: 64 units + ReLU + Dropout
Hidden layer 2: 32 units + ReLU + Dropout
Output layer: 1 unit or 2 classes
```

### Required Script

```txt
src/models/train_pytorch_mlp.py
```

### Requirements

- Use PyTorch Dataset and DataLoader.
- Use standard-scaled numeric features.
- Track train and validation loss.
- Support configurable epochs, learning rate, batch size, and seed.
- Save model checkpoint.
- Save metrics.
- Include early stopping if practical.

### Output

```txt
models/pytorch_mlp.pt
reports/pytorch_mlp_metrics.json
reports/figures/training_curve.png
```

### Acceptance Criteria

- PyTorch training runs on CPU.
- Training curve is saved.
- Test metrics are saved.
- README compares PyTorch MLP with scikit-learn models.

---

## 5.7 Model Evaluation

Evaluate all models on the same test set.

### Required Metrics

```txt
accuracy
precision
recall
f1
macro_f1
roc_auc
confusion_matrix
sensitivity
specificity
```

### Why Sensitivity and Specificity

Because the dataset is diagnostic in nature, the project should show that the model is evaluated beyond accuracy.

### Required Script

```txt
src/evaluation/evaluate_models.py
```

### Output

```txt
reports/model_comparison.md
reports/evaluation_metrics.json
reports/figures/confusion_matrix.png
reports/figures/roc_curve.png
reports/figures/precision_recall_curve.png
```

### Acceptance Criteria

- Evaluation metrics are generated for all trained models.
- ROC curve is saved.
- Confusion matrix is saved.
- README includes model comparison table.

---

## 5.8 Explainability

The project must include explainability for the best model.

### Required Methods

```txt
Feature importance
SHAP summary plot
SHAP force or waterfall plot for a single prediction
```

### Required Script

```txt
src/explainability/explain_model.py
```

### Output

```txt
reports/figures/feature_importance.png
reports/figures/shap_summary.png
reports/figures/shap_example_prediction.png
reports/explainability_summary.md
```

### Requirements

- Explain global feature importance.
- Explain one individual prediction.
- Explain limitations of interpretability.
- Use plain language for business/recruiter readability.

### Acceptance Criteria

- SHAP plots are generated.
- Explainability report exists.
- Dashboard can show top contributing features for a prediction, if practical.

---

## 5.9 Error Analysis

The project must include error analysis.

### Required Analysis

- False positives
- False negatives
- Low-confidence predictions
- Feature patterns in wrong predictions
- Threshold trade-off analysis

### Required Script

```txt
src/evaluation/error_analysis.py
```

### Output

```txt
reports/error_analysis.csv
reports/error_analysis.md
reports/figures/threshold_analysis.png
```

### Acceptance Criteria

- Error examples are saved.
- Error analysis explains which mistakes are more concerning.
- README includes a short limitation section.

---

## 5.10 MLflow Experiment Tracking

Use MLflow locally.

### Required Tracking

Track:

```txt
model_name
parameters
metrics
artifact_paths
training_date
dataset_version
random_seed
```

### Requirements

- MLflow must be optional.
- Training must still work if MLflow is disabled.
- MLflow data should not be committed to GitHub.

### Command

```bash
mlflow ui
```

MLflow UI:

```txt
http://localhost:5000
```

### Acceptance Criteria

- Baseline models log metrics to MLflow.
- PyTorch MLP logs metrics to MLflow.
- README explains how to open MLflow UI.

---

## 5.11 Prediction API

Build a FastAPI inference API.

### Required Endpoints

#### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

#### Model Info

```http
GET /model-info
```

Response:

```json
{
  "model_name": "random_forest",
  "problem_type": "binary_classification",
  "features": 30,
  "classes": ["malignant", "benign"]
}
```

#### Single Prediction

```http
POST /predict
```

Request:

```json
{
  "features": {
    "mean radius": 17.99,
    "mean texture": 10.38,
    "mean perimeter": 122.8,
    "mean area": 1001.0
  }
}
```

Important:

The actual API should require all 30 features unless the frontend uses sample rows from the dataset.

Response:

```json
{
  "predicted_class": "malignant",
  "predicted_class_id": 0,
  "confidence": 0.93,
  "probabilities": {
    "malignant": 0.93,
    "benign": 0.07
  },
  "top_features": [
    {
      "feature": "worst concave points",
      "importance": 0.18
    }
  ],
  "disclaimer": "This is a portfolio ML demo and not medical advice."
}
```

#### Batch Prediction

```http
POST /predict-batch
```

Response:

```json
{
  "results": [
    {
      "predicted_class": "malignant",
      "confidence": 0.93
    }
  ]
}
```

### API Requirements

- Load model once at startup.
- Validate input features.
- Return clear validation errors.
- Include CORS for React frontend.
- Do not expose internal stack traces.
- Include medical disclaimer in prediction response.

### Acceptance Criteria

- API runs with Uvicorn.
- Swagger UI works.
- `/health`, `/model-info`, `/predict`, and `/predict-batch` work.
- Invalid input returns a clear error.

---

## 5.12 React Frontend

Build a React + Vite dashboard.

### Required Pages

#### 1. Overview Page

Show:

- Project summary
- Dataset summary
- Model performance summary
- Medical disclaimer

#### 2. Prediction Page

Show:

- Input form for 30 numeric features
- Option to load sample patient records from CSV
- Predict button
- Predicted class
- Confidence score
- Probability chart
- Top feature contributions
- Disclaimer

#### 3. Model Evaluation Page

Show:

- Model comparison table
- Confusion matrix
- ROC curve
- Precision-recall curve
- Training curve for PyTorch model

#### 4. Explainability Page

Show:

- Feature importance chart
- SHAP summary plot
- Example explanation
- Explanation notes in plain English

### Required Components

```txt
FeatureInputForm
SampleSelector
PredictionResult
ProbabilityChart
ModelComparisonTable
MetricCard
ConfusionMatrixViewer
RocCurveViewer
FeatureImportanceChart
DisclaimerBanner
LoadingState
ErrorMessage
```

### Frontend Tech

```txt
React
Vite
TypeScript
Tailwind CSS
Recharts
Axios or Fetch API
```

### Acceptance Criteria

- Frontend can call FastAPI backend.
- User can choose a sample row and run prediction.
- User can view model metrics and plots.
- UI is responsive enough for desktop and mobile.
- README includes screenshots.

---

## 6. Non-Functional Requirements

## 6.1 Cost

The project must be free.

### Requirements

- Must run locally without paid services.
- Must not require paid GPU.
- Must not require paid database.
- Must not require paid cloud hosting.
- Must not depend on Kaggle login.
- Must not depend on external data download.

---

## 6.2 Performance

### API

- Single prediction should respond in less than 1 second after model load.
- Batch prediction should support at least 100 rows.
- Model must not reload on every request.

### Frontend

- UI must show loading states.
- UI must handle API errors.
- Charts must render without freezing on normal data sizes.

---

## 6.3 Reproducibility

The project must include:

```txt
requirements.txt
.env.example
README.md
random seed configuration
sample input CSV
clear CLI commands
```

Training commands must support a seed value:

```bash
python -m src.models.train_baseline --seed 42
python -m src.models.train_pytorch_mlp --seed 42
```

---

## 6.4 Maintainability

The project must use modular code.

### Required Backend Structure

```txt
src/
├── data/
├── features/
├── models/
├── evaluation/
├── explainability/
├── api/
└── utils/
```

### Required Frontend Structure

```txt
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── types/
│   └── utils/
```

### Requirements

- Do not put all logic in notebooks.
- Training logic must not be inside API code.
- API prediction logic must be reusable.
- Frontend API calls must be separated into service files.

---

## 6.5 Security and Safety

The API must:

- Validate all numeric input.
- Reject missing required features.
- Reject non-numeric values.
- Avoid exposing stack traces.
- Include a medical disclaimer.

The frontend must:

- Show disclaimer clearly.
- Avoid presenting the output as a real diagnosis.
- Use "prediction" or "model output", not "diagnosis".

---

## 6.6 Testing

The project must include tests.

### Required Tests

```txt
tests/test_data_loading.py
tests/test_preprocess.py
tests/test_api.py
tests/test_prediction_schema.py
```

### Test Cases

- Dataset loads successfully.
- Preprocessing returns expected shape.
- API health endpoint works.
- Predict endpoint rejects missing features.
- Predict endpoint returns expected response fields.

---

## 6.7 Documentation

The project must include:

```txt
README.md
docs/data_source.md
docs/modeling_approach.md
docs/evaluation.md
docs/explainability.md
docs/api.md
docs/frontend.md
docs/limitations.md
```

README must include:

```txt
Project overview
Problem statement
Dataset source
Tech stack
Architecture
Project structure
Setup instructions
Training commands
API usage
Frontend usage
Model results
Explainability results
Screenshots
Limitations
Future improvements
Medical disclaimer
```

---

## 7. Recommended Repository Structure

```txt
explainable-cancer-diagnosis-ml/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile.api
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│       └── sample_features.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_model_experiments.ipynb
│   └── 03_explainability.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   ├── explainability/
│   ├── api/
│   └── utils/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── types/
│       └── utils/
├── reports/
│   ├── figures/
│   ├── baseline_metrics.json
│   ├── pytorch_mlp_metrics.json
│   ├── evaluation_metrics.json
│   ├── model_comparison.md
│   ├── error_analysis.csv
│   ├── error_analysis.md
│   └── explainability_summary.md
├── models/
│   └── .gitkeep
├── docs/
└── tests/
```

---

## 8. CLI Commands

### Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Load Dataset

```bash
python -m src.data.load_dataset
```

### Validate Dataset

```bash
python -m src.data.validate_dataset
```

### Train Baseline Models

```bash
python -m src.models.train_baseline --seed 42
```

### Train PyTorch MLP

```bash
python -m src.models.train_pytorch_mlp --seed 42 --epochs 100 --batch-size 32
```

### Evaluate Models

```bash
python -m src.evaluation.evaluate_models
```

### Generate Explainability Reports

```bash
python -m src.explainability.explain_model
```

### Run API

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 9. Docker Requirements

Docker is recommended but should not block local setup.

### Required Services

```txt
api
frontend
```

### Docker Command

```bash
docker compose up --build
```

Expected URLs:

```txt
Frontend: http://localhost:5173
API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

---

## 10. GitHub Actions CI

Add basic CI.

### Required Workflow

```txt
.github/workflows/ci.yml
```

### CI Jobs

```txt
Backend:
- install Python dependencies
- run tests
- run basic lint or import check

Frontend:
- npm install
- npm run build
```

### Acceptance Criteria

- CI runs on push and pull request.
- CI does not require secrets.
- CI does not require deployment.
- CI does not require paid services.

---

## 11. README Model Result Template

The README must include a model comparison table.

```md
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Notes |
|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | TBD | TBD | TBD | TBD | TBD | Strong baseline |
| Random Forest | TBD | TBD | TBD | TBD | TBD | Tree-based model |
| Gradient Boosting | TBD | TBD | TBD | TBD | TBD | Boosting model |
| PyTorch MLP | TBD | TBD | TBD | TBD | TBD | Neural network |
```

---

## 12. Architecture

```txt
scikit-learn Breast Cancer Dataset
        ↓
Data Loading
        ↓
Data Validation
        ↓
EDA
        ↓
Preprocessing and Split
        ↓
Baseline ML Models + PyTorch MLP
        ↓
Model Evaluation
        ↓
Explainability with SHAP
        ↓
FastAPI Inference API
        ↓
React Dashboard
```

---

## 13. Business / Portfolio Value

The project should communicate these skills:

```txt
- Ability to work with tabular ML datasets
- Ability to compare multiple models fairly
- Understanding of classification metrics
- Understanding of sensitivity, specificity, ROC-AUC, and threshold tradeoffs
- Ability to explain model predictions with SHAP
- Ability to serve ML models with FastAPI
- Ability to build a frontend dashboard for model interpretation
- Ability to make a reproducible and documented ML project
```

Resume bullet example:

```txt
Built an explainable tabular machine learning system using scikit-learn, PyTorch, SHAP, FastAPI, and React to classify Breast Cancer Wisconsin Diagnostic samples, compare multiple models, analyze classification errors, and explain predictions through an interactive dashboard.
```

---

## 14. Limitations

The project must document limitations:

```txt
- The dataset is small and clean compared with real-world clinical data.
- The model is trained on a public educational dataset.
- The system is not suitable for real medical diagnosis.
- Feature values are not easy for general users to input manually.
- External validation on independent datasets is not included in version 1.
```

---

## 15. Future Improvements

```txt
- Add threshold tuning UI
- Add calibration curve
- Add model confidence monitoring
- Add LIME as an additional local explanation method
- Add ONNX export
- Add batch CSV upload in frontend
- Add Hugging Face Spaces demo
- Add comparison with TensorFlow/Keras MLP
- Add automated model card generation
```

---

## 16. Definition of Done

The project is complete when:

- Dataset loads from scikit-learn.
- Data validation report is generated.
- EDA notebook and summary exist.
- Baseline models are trained.
- PyTorch MLP is trained.
- All models are evaluated on the same test set.
- Model comparison report exists.
- SHAP explainability outputs exist.
- Error analysis exists.
- FastAPI backend works.
- React frontend works.
- Docker Compose works or local setup is clearly documented.
- GitHub Actions CI works.
- README is complete and recruiter-friendly.
- Screenshots are added.
- Medical disclaimer is visible in README, API response, and frontend.

---

# Project Implementation Notes

Use these notes after creating and cloning the new repository.

```txt
You are working inside my new GitHub repository.

Repository name:
explainable-cancer-diagnosis-ml

Goal:
Build an end-to-end Data Science / Machine Learning portfolio project using the scikit-learn Breast Cancer Wisconsin Diagnostic dataset. The project must demonstrate tabular ML, PyTorch, explainable AI, model evaluation, FastAPI serving, and React dashboard development.

Important:
- This is a portfolio ML demo, not a real medical diagnosis tool.
- Add medical disclaimer in README, API response, and frontend.
- The project must be free-tier friendly.
- The dataset must come from scikit-learn using load_breast_cancer(as_frame=True).
- Do not require Kaggle, login, scraping, paid cloud, paid GPU, or external dataset downloads.
- Use React + Vite for frontend.
- Use FastAPI for backend.
- Use PyTorch for a tabular MLP model.
- Use SHAP for explainability.
- Use MLflow local tracking if practical.
- Use Docker if practical.
- Do not commit large model artifacts.
- Keep the code modular and recruiter-friendly.

Functional Requirements:
1. Create the recommended project structure.
2. Add data loading from sklearn.datasets.load_breast_cancer.
3. Save raw and processed CSV files locally.
4. Add data validation and markdown report.
5. Add EDA notebook and EDA summary.
6. Add preprocessing utilities with stratified train/validation/test split.
7. Train Logistic Regression, Random Forest, and Gradient Boosting models.
8. Train a PyTorch MLP model on standardized features.
9. Evaluate all models on the same test set.
10. Report accuracy, precision, recall, F1, macro F1, ROC-AUC, sensitivity, and specificity.
11. Generate confusion matrix, ROC curve, precision-recall curve, and training curve.
12. Add SHAP explainability for the best model.
13. Add error analysis for false positives, false negatives, low-confidence predictions, and threshold tradeoffs.
14. Add FastAPI endpoints: /health, /model-info, /predict, /predict-batch.
15. Add React + Vite frontend pages: Overview, Prediction, Model Evaluation, Explainability.
16. Add Docker support if practical.
17. Add GitHub Actions CI for backend tests and frontend build.
18. Add tests for data loading, preprocessing, API, and prediction schema.
19. Add complete README and docs.
20. Create PORTFOLIO_REVIEW.md explaining what this project demonstrates.

Non-Functional Requirements:
1. Must run locally without paid services.
2. Must not require internet for dataset download after dependencies are installed.
3. Must run on CPU.
4. API must load model once at startup.
5. API must validate all numeric inputs.
6. Frontend must show loading and error states.
7. Code must be modular.
8. README must be clear enough for recruiters.
9. CI must not require secrets.
10. Large generated artifacts must be ignored by Git.

Recommended README Sections:
- Project Overview
- Medical Disclaimer
- Problem Statement
- Dataset Source
- Tech Stack
- Architecture
- Project Structure
- Setup Instructions
- Training
- Evaluation
- Explainability
- API Usage
- Frontend Usage
- Screenshots
- Model Results
- Error Analysis
- Limitations
- Future Improvements
- Resume Bullet

After implementation:
Create a file named PORTFOLIO_REVIEW.md with:
- Implemented features
- Data science skills demonstrated
- ML engineering skills demonstrated
- Explainability skills demonstrated
- Remaining gaps
- How to present this project in resume and LinkedIn
```
