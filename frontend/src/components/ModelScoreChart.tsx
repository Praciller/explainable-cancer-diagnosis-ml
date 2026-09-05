import { Bar, BarChart, Cell, ReferenceLine, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function ModelScoreChart({
  malignantScore,
  threshold,
}: {
  malignantScore: number;
  threshold: number;
}) {
  const data = [{ name: "Malignant-class score", value: malignantScore }];
  const chartTitleId = "malignant-score-chart-title";
  const chartDescriptionId = "malignant-score-chart-description";

  return (
    <figure className="chart" aria-labelledby={chartTitleId}>
      <h3 id={chartTitleId}>Malignant-class score</h3>
      <div
        className="chart-visual"
        role="img"
        aria-label={`Malignant-class model score ${malignantScore.toFixed(3)}. Fixed classification threshold ${threshold.toFixed(2)}.`}
        aria-describedby={chartDescriptionId}
      >
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={data} layout="vertical" margin={{ left: 8, right: 32 }}>
            <XAxis
              type="number"
              domain={[0, 1]}
              tickFormatter={(value: number) => value.toFixed(1)}
            />
            <YAxis dataKey="name" type="category" hide />
            <ReferenceLine
              x={threshold}
              stroke="var(--text)"
              strokeDasharray="4 4"
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]} isAnimationActive={false}>
              <Cell fill="var(--malignant)" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <figcaption id={chartDescriptionId} className="score-caption">
        <span>Malignant-class score: {malignantScore.toFixed(3)}</span>
        <span>Fixed threshold: {threshold.toFixed(2)}</span>
      </figcaption>
    </figure>
  );
}
