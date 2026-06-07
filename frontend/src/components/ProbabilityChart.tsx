import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function ProbabilityChart({
  probabilities,
}: {
  probabilities: Record<"malignant" | "benign", number>;
}) {
  const data = [
    { name: "Malignant", value: probabilities.malignant, color: "#d36d5f" },
    { name: "Benign", value: probabilities.benign, color: "#6c9b76" },
  ];

  return (
    <div className="chart" aria-label="Prediction probability chart">
      <ResponsiveContainer width="100%" height={190}>
        <BarChart data={data} layout="vertical" margin={{ left: 16, right: 24 }}>
          <XAxis
            type="number"
            domain={[0, 1]}
            tickFormatter={(value: number) => `${Math.round(value * 100)}%`}
          />
          <YAxis dataKey="name" type="category" width={82} />
          <Tooltip formatter={(value) => `${(Number(value) * 100).toFixed(1)}%`} />
          <Bar dataKey="value" radius={[0, 4, 4, 0]} isAnimationActive={false}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
