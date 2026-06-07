import { reportUrl } from "../services/api";
import { ReportFigure } from "./ReportFigure";

export function ConfusionMatrixViewer() {
  return (
    <ReportFigure
      src={reportUrl("confusion_matrix.png")}
      alt="Confusion matrix for the selected model"
      caption="Errors are split by malignant and benign class."
    />
  );
}
