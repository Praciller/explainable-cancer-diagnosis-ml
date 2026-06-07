# API

Start:

```bash
uvicorn src.api.main:app --reload --port 8000
```

## Endpoints

### `GET /health`

Returns `{"status":"ok"}`.

### `GET /model-info`

Returns model name, problem type, feature count, class names, and dataset version.

### `GET /features`

Returns the 30 canonical feature names with observed minimum, maximum, and mean values. The frontend uses this endpoint as its form schema.

### `GET /samples`

Returns complete dataset samples for the dashboard. Query parameter `limit` accepts 1 to 20.

### `POST /predict`

Requires exactly 30 finite numeric values:

```python
import pandas as pd
import requests

features = pd.read_csv("data/sample/sample_features.csv").iloc[0].to_dict()
response = requests.post(
    "http://localhost:8000/predict",
    json={"features": features},
    timeout=5,
)
print(response.json())
```

The response includes predicted class, probabilities, confidence, top feature contributions, and the medical disclaimer.

### `POST /predict-batch`

Accepts `{"items": [{"features": {...}}]}` with 1 to 100 rows.

## Validation

Pydantic rejects:

- missing or unknown feature names;
- numeric strings and booleans;
- `NaN`, infinity, and non-numeric values;
- batch sizes above 100.

The model is loaded once during FastAPI lifespan startup.
