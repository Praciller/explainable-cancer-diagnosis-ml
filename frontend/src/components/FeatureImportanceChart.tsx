import { reportUrl } from "../services/api";
import { ReportFigure } from "./ReportFigure";

export function FeatureImportanceChart() {
  return (
    <ReportFigure
      src={reportUrl("feature_importance.png")}
      alt="Global model feature importance"
      caption="Importance describes model behavior, not biological causality."
    />
  );
}
