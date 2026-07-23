import { reportUrl } from "../services/api";
import { ReportFigure } from "./ReportFigure";

export function ConfusionMatrixViewer() {
  return (
    <ReportFigure
      src={reportUrl("confusion_matrix.png")}
      alt="Governed test confusion matrix for the selected model, ordered malignant then benign"
      caption="Rows are actual labels and columns are model classifications, ordered malignant then benign."
    />
  );
}
