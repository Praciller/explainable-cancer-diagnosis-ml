import type { PredictionResponse } from "../types/api";
import { ProbabilityChart } from "./ProbabilityChart";

export function PredictionResult({ result }: { result: PredictionResponse }) {
  return (
    <section className="result" aria-live="polite">
      <header>
        <span>Model prediction</span>
        <h2 className={`class-${result.predicted_class}`}>{result.predicted_class}</h2>
        <p>{(result.confidence * 100).toFixed(1)}% model confidence</p>
      </header>
      <ProbabilityChart probabilities={result.probabilities} />
      <div>
        <h3>Top feature contributions</h3>
        <ol className="contribution-list">
          {result.top_features.map((item) => (
            <li key={item.feature}>
              <span>{item.feature}</span>
              <strong>{item.importance.toFixed(3)}</strong>
            </li>
          ))}
        </ol>
      </div>
      <p className="result-disclaimer">{result.disclaimer}</p>
    </section>
  );
}
