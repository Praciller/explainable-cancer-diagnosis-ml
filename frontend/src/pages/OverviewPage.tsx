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
  const locked = evaluation?.locked_test.metrics;

  return (
    <div className="page">
      <header className="page-heading overview-heading">
        <div>
          <span className="section-label">Governed educational tabular ML</span>
          <h1>Evidence with an explicit boundary.</h1>
          <p>
            Compare validation evidence, inspect malignant-case errors on a governed regression
            set, and trace the selected model without claiming clinical meaning.
          </p>
        </div>
        <button className="button button-primary" type="button" onClick={onStart}>
          Review the workflow <ArrowRight aria-hidden="true" size={18} />
        </button>
      </header>

      <DisclaimerBanner />

      <section className="metric-row" aria-label="Governance summary">
        <MetricCard label="Dataset" value="569 × 30" detail="WDBC rows and image measurements" />
        <MetricCard label="Split" value="398 / 85 / 86" detail="Train / validation / governed test" />
        <MetricCard label="Positive class" value="Malignant" detail="Raw target 0, explicit contract" />
        <MetricCard
          label="Score status"
          value={modelInfo.calibration_status}
          detail={`Fixed threshold ${modelInfo.decision_threshold.toFixed(2)}`}
        />
      </section>

      <section className="evidence-summary" aria-label="Selected-model evidence">
        <div>
          <span className="section-label">Selected on validation</span>
          <h2>{modelInfo.model_name}</h2>
          <p>
            Selection metric: validation ROC-AUC. The 86-row test artifact has been exposed during
            portfolio development and is retained as a governed regression set.
          </p>
        </div>
        <dl>
          <div>
            <dt>Governed-test ROC-AUC</dt>
            <dd>{locked ? locked.roc_auc.toFixed(3) : "Unavailable"}</dd>
          </div>
          <div>
            <dt>Malignant-to-benign errors</dt>
            <dd>{locked?.false_negative_count ?? "Unavailable"}</dd>
          </div>
          <div>
            <dt>Benign-to-malignant errors</dt>
            <dd>{locked?.false_positive_count ?? "Unavailable"}</dd>
          </div>
        </dl>
      </section>

      <section className="workflow">
        <div className="section-heading">
          <span className="section-label">Review path</span>
          <h2>From packaged data to validated artifacts</h2>
        </div>
        <ol>
          <li>
            <Database aria-hidden="true" />
            <div>
              <strong>Validate the dataset contract</strong>
              <p>Fingerprint 569 rows, 30 ordered features, target mapping, and split lineage.</p>
            </div>
          </li>
          <li>
            <GitCompareArrows aria-hidden="true" />
            <div>
              <strong>Select on validation only</strong>
              <p>Compare a majority baseline and four candidates without test-set selection.</p>
            </div>
          </li>
          <li>
            <ScanSearch aria-hidden="true" />
            <div>
              <strong>Verify model behavior</strong>
              <p>Check malignant-oriented scores, SHAP signs, errors, and artifact checksums.</p>
            </div>
          </li>
        </ol>
      </section>
    </div>
  );
}
