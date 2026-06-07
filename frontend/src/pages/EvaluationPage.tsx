import { ConfusionMatrixViewer } from "../components/ConfusionMatrixViewer";
import { ModelComparisonTable } from "../components/ModelComparisonTable";
import { ReportFigure } from "../components/ReportFigure";
import { RocCurveViewer } from "../components/RocCurveViewer";
import { reportUrl } from "../services/api";
import type { EvaluationReport } from "../types/api";

export function EvaluationPage({ report }: { report: EvaluationReport | null }) {
  return (
    <div className="page">
      <header className="page-heading">
        <div>
          <span className="section-label">Held-out evidence</span>
          <h1>One test set, multiple model families.</h1>
          <p>
            Accuracy is not enough. The comparison includes malignant-class sensitivity,
            specificity, macro F1, ROC-AUC, and precision-recall behavior.
          </p>
        </div>
      </header>

      <section>
        <div className="section-heading">
          <h2>Model comparison</h2>
        </div>
        <ModelComparisonTable report={report} />
      </section>

      <section className="figure-grid">
        <ConfusionMatrixViewer />
        <RocCurveViewer />
        <ReportFigure
          src={reportUrl("precision_recall_curve.png")}
          alt="Precision-recall curves for all models"
          caption="Precision-recall focuses on malignant-class retrieval quality."
        />
        <ReportFigure
          src={reportUrl("training_curve.png")}
          alt="PyTorch MLP training and validation loss"
          caption="Validation loss supports early stopping."
        />
      </section>
    </div>
  );
}
