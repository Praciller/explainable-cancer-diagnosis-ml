import { useState } from "react";

import { ErrorMessage } from "../components/ErrorMessage";
import { DisclaimerBanner } from "../components/DisclaimerBanner";
import { FeatureInputForm } from "../components/FeatureInputForm";
import { PredictionResult } from "../components/PredictionResult";
import { SampleSelector } from "../components/SampleSelector";
import { Button } from "../components/ui";
import { predict } from "../services/api";
import type { FeatureDefinition, PredictionResponse, SampleRecord } from "../types/api";

interface PredictionPageProps {
  features: FeatureDefinition[];
  samples: SampleRecord[];
  hostedShowcase?: boolean;
}

export function PredictionPage({
  features,
  samples,
  hostedShowcase = false,
}: PredictionPageProps) {
  const [values, setValues] = useState<Record<string, number>>(
    () => samples[0]?.features ?? Object.fromEntries(features.map((item) => [item.name, item.mean])),
  );
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);

  if (hostedShowcase) {
    return (
      <div className="page">
        <header className="page-heading">
          <div>
            <span className="section-label">Prediction workspace</span>
          <h1>Live inference stays local for v1.</h1>
            <p>
              The hosted frontend presents measured model evidence without deploying the model
              inference API to a general-purpose frontend platform.
            </p>
          </div>
        </header>

        <DisclaimerBanner />

        <section className="deployment-notice">
          <h2>Run the complete sample-based workflow locally</h2>
          <p>
            Start the FastAPI model service and React dashboard together. The local dashboard will
            load the 30-feature schema and balanced samples from the API.
          </p>
          <code>docker compose up --build</code>
          <p>
            Open <strong>http://localhost:5173</strong>. The API remains at{" "}
            <strong>http://localhost:8000</strong>.
          </p>
        </section>
      </div>
    );
  }

  const runPrediction = async () => {
    setPending(true);
    setError("");
    try {
      setResult(await predict(values));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Prediction failed.");
    } finally {
      setPending(false);
    }
  };

  return (
    <div className="page">
      <header className="page-heading">
        <div>
          <span className="section-label">Prediction workspace</span>
          <h1>Start with a governed dataset row.</h1>
          <p>
            These are educational dataset records containing measurements from digitized
            fine-needle aspirate images, not real-time patients or user-entered symptoms.
          </p>
        </div>
      </header>

      <DisclaimerBanner />

      <div className="prediction-layout">
        <section className="prediction-input">
          <h2>Choose input values</h2>
          <SampleSelector
            samples={samples}
            onSelect={(sample) => {
              setValues(sample.features);
              setResult(null);
            }}
          />
          <Button
            variant="text"
            type="button"
            aria-expanded={showForm}
            onClick={() => setShowForm((current) => !current)}
          >
            {showForm ? "Hide all 30 feature inputs" : "Review all 30 feature inputs"}
          </Button>
          {showForm ? (
            <FeatureInputForm
              definitions={features}
              values={values}
              onChange={(name, value) =>
                setValues((current) => ({ ...current, [name]: value }))
              }
              onSubmit={runPrediction}
              pending={pending}
            />
          ) : (
            <Button
              type="button"
              onClick={runPrediction}
              disabled={pending}
            >
              {pending ? "Running model..." : "Run model prediction"}
            </Button>
          )}
          {error ? <ErrorMessage message={error} /> : null}
        </section>

        <div className="prediction-output">
          {result ? (
            <PredictionResult result={result} />
          ) : (
            <div className="empty-result">
              <strong>No model output yet</strong>
              <p>
                Load a dataset row and run the model to see its malignant-class score and bounded
                feature contributions.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
