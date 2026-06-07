import { ArrowRight, Database, GitCompareArrows, ScanSearch } from "lucide-react";

import { DisclaimerBanner } from "../components/DisclaimerBanner";
import { MetricCard } from "../components/MetricCard";
import type { EvaluationReport, ModelInfo } from "../types/api";

interface OverviewPageProps {
  modelInfo: ModelInfo;
  evaluation: EvaluationReport | null;
  onStart: () => void;
}

export function OverviewPage({ modelInfo, evaluation, onStart }: OverviewPageProps) {
  const best = evaluation?.models[evaluation.best_test_model];

  return (
    <div className="page">
      <header className="page-heading overview-heading">
        <div>
          <span className="section-label">Explainable tabular ML</span>
          <h1>Evidence before confidence.</h1>
          <p>
            Compare four classification approaches, inspect held-out performance, and trace what
            shaped each model output.
          </p>
        </div>
        <button className="button button-primary" type="button" onClick={onStart}>
          Explore a prediction <ArrowRight aria-hidden="true" size={18} />
        </button>
      </header>

      <DisclaimerBanner />

      <section className="metric-row" aria-label="Project summary">
        <MetricCard label="Dataset" value="569" detail="Rows, 30 numeric features" />
        <MetricCard label="Selected model" value={modelInfo.model_name} detail="Validation ROC-AUC" />
        <MetricCard
          label="Test ROC-AUC"
          value={best ? best.roc_auc.toFixed(3) : "Run evaluation"}
          detail="Shared held-out test set"
        />
      </section>

      <section className="workflow">
        <div className="section-heading">
          <span className="section-label">Review path</span>
          <h2>From offline dataset to explainable API</h2>
        </div>
        <ol>
          <li>
            <Database aria-hidden="true" />
            <div>
              <strong>Validate the dataset</strong>
              <p>Verify class mapping, ranges, missing values, duplicates, and imbalance.</p>
            </div>
          </li>
          <li>
            <GitCompareArrows aria-hidden="true" />
            <div>
              <strong>Compare model families</strong>
              <p>Use one stratified split for linear, ensemble, boosting, and neural models.</p>
            </div>
          </li>
          <li>
            <ScanSearch aria-hidden="true" />
            <div>
              <strong>Inspect model behavior</strong>
              <p>Review global importance, SHAP values, errors, and threshold trade-offs.</p>
            </div>
          </li>
        </ol>
      </section>
    </div>
  );
}
