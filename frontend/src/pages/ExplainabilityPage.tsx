import caseArtifact from "../data/explainability_case.json";
import { ExplainabilityCaseStudy } from "../components/ExplainabilityCaseStudy";
import { FeatureImportanceChart } from "../components/FeatureImportanceChart";
import { ReportFigure } from "../components/ReportFigure";
import { reportUrl } from "../services/api";
import type { CaseStudyArtifact } from "../types/explainability";

const typedCaseArtifact = caseArtifact as unknown as CaseStudyArtifact;

export function ExplainabilityPage() {
  return (
    <div className="page">
      <header className="page-heading">
        <div>
          <span className="section-label">Model interpretation</span>
          <h1>Explain behavior without claiming causality.</h1>
          <p>
            Global importance summarizes recurring signals. SHAP values reconstruct the selected
            model's malignant-class log-odds relative to a training-background expectation.
          </p>
        </div>
      </header>

      <section className="explanation-note">
        <h2>Read these charts carefully</h2>
        <p>
          Correlated measurements can share or redistribute importance. These explanations
          describe how the model used supplied measurements. They do not prove biological
          causality, medical importance, or why cancer develops.
        </p>
      </section>

      <ExplainabilityCaseStudy artifact={typedCaseArtifact} />

      <section className="figure-grid">
        <FeatureImportanceChart />
        <ReportFigure
          src={reportUrl("shap_summary.png")}
          alt="SHAP summary plot for malignant-class log-odds across governed test rows"
          caption="Positive SHAP values move the model toward its malignant-class output."
        />
        <ReportFigure
          src={reportUrl("shap_example_prediction.png")}
          alt="Malignant-class SHAP waterfall for one educational dataset row"
          caption="Dataset row 102, reconstructed relative to the training background."
        />
        <ReportFigure
          src={reportUrl("threshold_analysis.png")}
          alt="Validation sensitivity and specificity across model-score thresholds"
          caption="A validation-only trade-off view, not a clinical threshold recommendation."
        />
      </section>
    </div>
  );
}
