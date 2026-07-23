import type { PredictionResponse } from "../types/api";
import { ModelScoreChart } from "./ModelScoreChart";

export function PredictionResult({ result }: { result: PredictionResponse }) {
  return (
    <section className="result" aria-live="polite">
      <header>
        <span>Model classification for a dataset-style feature vector</span>
        <h2 className={`class-${result.model_classification}`}>
          {result.model_classification}
        </h2>
        <p>
          Malignant is the safety-relevant positive class. This output uses the fixed{" "}
          {result.decision_threshold.toFixed(2)} model threshold.
        </p>
      </header>
      <ModelScoreChart
        malignantScore={result.malignant_class_score}
        threshold={result.decision_threshold}
      />
      <p className="score-interpretation">
        {result.score_interpretation} Calibration status:{" "}
        <strong>{result.calibration_status}</strong>.
      </p>
      {result.warning_flags.length ? (
        <div className="warning-list" role="status">
          <strong>Input warnings</strong>
          <ul>
            {result.warning_flags.map((warning) => (
              <li key={warning}>{warning.replace("outside_observed_training_range:", "")}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="range-status">All values are within the observed dataset ranges.</p>
      )}
      <div>
        <h3>Top malignant-class feature contributions</h3>
        <ol className="contribution-list">
          {result.top_feature_contributions.map((item) => (
            <li key={item.feature}>
              <span>
                {item.feature}
                <small>{item.direction.replaceAll("_", " ")}</small>
              </span>
              <strong>{item.contribution.toFixed(3)}</strong>
            </li>
          ))}
        </ol>
      </div>
      <p className="result-disclaimer">{result.educational_limitation}</p>
      <small className="model-version">Artifact version {result.model_version}</small>
    </section>
  );
}
