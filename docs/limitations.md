# Scope and limitations

- The 569-row WDBC dataset is small, clean, historical, and educational.
- Features come from digitized fine-needle aspirate images, not user-entered symptoms.
- Physical units are not supplied by the bundled dataset documentation.
- The governed test rows were exposed during earlier portfolio development and are not a pristine scientific holdout.
- Results come from one deterministic split and have material sample uncertainty.
- No external, prospective, demographic-representativeness, fairness, or clinical validation is included.
- Model scores are uncalibrated and are not individual clinical probabilities or risk estimates.
- Observed value ranges are descriptive warning references, not clinical validity bounds.
- SHAP and coefficients describe model behavior, not biology or causality.
- The local API has no authentication because it exposes only public educational dataset rows.
- `joblib` and PyTorch artifacts are trusted-code formats; only repository-generated artifacts may be loaded.
- The project makes no claim of clinical validity, regulatory compliance, production readiness, or medical-device security.

> This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
