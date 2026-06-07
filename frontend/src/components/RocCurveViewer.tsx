import { reportUrl } from "../services/api";
import { ReportFigure } from "./ReportFigure";

export function RocCurveViewer() {
  return (
    <ReportFigure
      src={reportUrl("roc_curve.png")}
      alt="ROC curves comparing all trained models"
      caption="All curves use the same held-out test rows."
    />
  );
}
