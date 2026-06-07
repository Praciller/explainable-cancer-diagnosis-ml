import { FeatureImportanceChart } from "../components/FeatureImportanceChart";
import { ReportFigure } from "../components/ReportFigure";
import { reportUrl } from "../services/api";

export function ExplainabilityPage() {
  return (
    <div className="page">
      <header className="page-heading">
        <div>
          <span className="section-label">Model interpretation</span>
          <h1>Explain behavior without claiming causality.</h1>
          <p>
            Global importance summarizes recurring signals. SHAP shows how feature values move
            individual outputs relative to a background expectation.
          </p>
        </div>
      </header>

      <section className="explanation-note">
        <h2>Read these charts carefully</h2>
        <p>
          Correlated measurements can share or redistribute importance. These explanations
          describe the trained model, not biological mechanisms or clinical relevance.
        </p>
      </section>

      <section className="figure-grid">
        <FeatureImportanceChart />
        <ReportFigure
          src={reportUrl("shap_summary.png")}
          alt="SHAP summary plot across held-out samples"
          caption="Feature impact magnitude and direction across multiple outputs."
        />
        <ReportFigure
          src={reportUrl("shap_example_prediction.png")}
          alt="SHAP waterfall for one example prediction"
          caption="One local explanation relative to the model background."
        />
        <ReportFigure
          src={reportUrl("threshold_analysis.png")}
          alt="Sensitivity and specificity across decision thresholds"
          caption="Threshold choice changes the model's error trade-off."
        />
      </section>
    </div>
  );
}
