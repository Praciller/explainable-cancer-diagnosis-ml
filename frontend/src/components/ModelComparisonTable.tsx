import type { EvaluationReport } from "../types/api";

export function ModelComparisonTable({ report }: { report: EvaluationReport | null }) {
  if (!report) {
    return <p className="muted">Run model evaluation to populate comparison metrics.</p>;
  }

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>Accuracy</th>
            <th>Recall</th>
            <th>Macro F1</th>
            <th>ROC-AUC</th>
            <th>Sensitivity</th>
            <th>Specificity</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(report.models).map(([name, metrics]) => (
            <tr key={name}>
              <th scope="row">
                {name}
                {name === report.best_test_model ? <small>Best test ROC-AUC</small> : null}
              </th>
              <td>{metrics.accuracy.toFixed(3)}</td>
              <td>{metrics.recall.toFixed(3)}</td>
              <td>{metrics.macro_f1.toFixed(3)}</td>
              <td>{metrics.roc_auc.toFixed(3)}</td>
              <td>{metrics.sensitivity.toFixed(3)}</td>
              <td>{metrics.specificity.toFixed(3)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
