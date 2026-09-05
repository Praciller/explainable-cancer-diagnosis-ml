import { Metric } from "./ui";

interface MetricCardProps {
  label: string;
  value: string;
  detail: string;
}

export function MetricCard({ label, value, detail }: MetricCardProps) {
  return <Metric label={label} value={value} detail={detail} />;
}
