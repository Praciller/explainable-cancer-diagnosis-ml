import { ConfusionMatrixViewer } from "../components/ConfusionMatrixViewer";
import { ModelComparisonTable } from "../components/ModelComparisonTable";
import { ReportFigure } from "../components/ReportFigure";
import { RocCurveViewer } from "../components/RocCurveViewer";
import { reportUrl } from "../services/api";
import type { EvaluationReport } from "../types/api";

export function EvaluationPage({ report }: { report: EvaluationReport | null }) {
  const locked = report?.locked_test.metrics;

  return (
    <div className="page">
      <header className="page-heading">
        <div>
          <span className="section-label">Validation selection, governed test evidence</span>
          <h1>Keep model choice outside the test result.</h1>
          <p>
            Candidates are compared on 85 validation rows. Only the frozen selected model is
            reported on the 86-row governed regression set.
          </p>
        </div>
      </header>

      <section>
        <div className="section-heading">
          <h2>Validation-only candidate comparison</h2>
          <p>
            Malignant is the positive class. ROC-AUC and PR-AUC measure ranking, not clinical
            utility.
          </p>
        </div>
        <ModelComparisonTable report={report} />
      </section>

      <section className="locked-summary">
        <div>
          <span className="section-label">Frozen selected model</span>
          <h2>{report?.selected_model ?? "Run the pipeline"}</h2>
          <p>
            Threshold {report?.threshold.value.toFixed(2) ?? "unavailable"}, calibration status{" "}
            {report?.calibration_status ?? "unavailable"}. This test artifact is already exposed
            and serves as a portfolio regression set.
          </p>
        </div>
        <dl>
          <div>
            <dt>Confusion matrix</dt>
            <dd>{locked ? JSON.stringify(locked.confusion_matrix) : "Unavailable"}</dd>
          </div>
          <div>
            <dt>Malignant recall</dt>
            <dd>{locked ? locked.malignant_recall.toFixed(3) : "Unavailable"}</dd>
          </div>
          <div>
            <dt>PR-AUC</dt>
            <dd>{locked ? locked.pr_auc.toFixed(3) : "Unavailable"}</dd>
          </div>
        </dl>
      </section>

      <section className="figure-grid">
        <ConfusionMatrixViewer />
        <RocCurveViewer />
        <ReportFigure
          src={reportUrl("precision_recall_curve.png")}
          alt="Precision-recall curve for the frozen selected model"
          caption="Malignant-class ranking on the governed regression set."
        />
        <ReportFigure
          src={reportUrl("training_curve.png")}
          alt="PyTorch MLP training and validation loss"
          caption="The MLP is a validation challenger, not the deployed model."
        />
      </section>
    </div>
  );
}
