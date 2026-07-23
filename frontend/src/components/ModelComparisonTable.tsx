import type { EvaluationReport } from "../types/api";

export function ModelComparisonTable({ report }: { report: EvaluationReport | null }) {
  if (!report) {
    return <p className="muted">Run the governed pipeline to populate validation metrics.</p>;
  }

  return (
    <div className="table-scroll">
      <table>
        <caption className="sr-only">
          Validation-only candidate comparison. Malignant is the positive class.
        </caption>
        <thead>
          <tr>
            <th>Model</th>
            <th>Balanced accuracy</th>
            <th>Malignant recall</th>
            <th>ROC-AUC</th>
            <th>PR-AUC</th>
            <th>Specificity</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(report.validation_models).map(([name, metrics]) => (
            <tr key={name}>
              <th scope="row">
                {name}
                {name === report.selected_model ? <small>Selected on validation</small> : null}
              </th>
              <td>{metrics.balanced_accuracy.toFixed(3)}</td>
              <td>{metrics.malignant_recall.toFixed(3)}</td>
              <td>{metrics.roc_auc.toFixed(3)}</td>
              <td>{metrics.pr_auc.toFixed(3)}</td>
              <td>{metrics.specificity.toFixed(3)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
