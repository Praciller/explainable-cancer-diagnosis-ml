# Frontend

The frontend is a React 19 and Vite 8 product dashboard styled with Tailwind CSS 4 and project CSS tokens.

## Start

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL` when the API is not at `http://localhost:8000`.

## Vercel

The frontend-only production deployment is available at:

https://explainable-cancer-diagnosis-ml.vercel.app

Production builds without `VITE_API_URL` use hosted showcase mode. They load a fixed snapshot of
measured model metrics and generated report figures, while clearly disabling live inference.

Local Vite and Docker builds remain API-connected. The Docker frontend sets
`VITE_API_URL=http://localhost:8000`.

## Pages

- Overview: dataset, selected model, measured evidence, disclaimer.
- Prediction: sample selector, optional 30-feature form, output probabilities, top contributions.
- Evaluation: comparison table and generated evaluation figures.
- Explainability: feature importance, SHAP, and threshold figures.

## UX Decisions

- Sample selection is primary because the 30 measurements are not user-friendly manual inputs.
- The full form is progressively disclosed and generated from `/features`.
- Malignant and benign colors remain consistent across charts and outputs.
- Loading, empty, request error, disabled, hover, focus, and success states are represented.
- Navigation collapses to icon controls on smaller screens.

## Verification

```bash
npm test
npm run build
```
