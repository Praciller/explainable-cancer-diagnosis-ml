import { Bar, BarChart, Cell, ReferenceLine, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function ModelScoreChart({
  malignantScore,
  threshold,
}: {
  malignantScore: number;
  threshold: number;
}) {
  const data = [{ name: "Malignant-class score", value: malignantScore }];

  return (
    <div
      className="chart"
      role="img"
      aria-label={`Malignant-class model score ${malignantScore.toFixed(3)}. Fixed classification threshold ${threshold.toFixed(2)}.`}
    >
      <ResponsiveContainer width="100%" height={150}>
        <BarChart data={data} layout="vertical" margin={{ left: 24, right: 24 }}>
          <XAxis
            type="number"
            domain={[0, 1]}
            tickFormatter={(value: number) => value.toFixed(1)}
          />
          <YAxis dataKey="name" type="category" width={136} />
          <ReferenceLine
            x={threshold}
            stroke="oklch(0.24 0.025 310)"
            strokeDasharray="4 4"
            label="Threshold"
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]} isAnimationActive={false}>
            <Cell fill="oklch(0.58 0.16 32)" />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="score-caption">
        Score {malignantScore.toFixed(3)}. Fixed threshold {threshold.toFixed(2)}.
      </p>
    </div>
  );
}
