import { reportUrl } from "../services/api";
import { ReportFigure } from "./ReportFigure";

export function RocCurveViewer() {
  return (
    <ReportFigure
      src={reportUrl("roc_curve.png")}
      alt="ROC curve for the frozen selected model"
      caption="The governed regression set is used only for the frozen selected model."
    />
  );
}
