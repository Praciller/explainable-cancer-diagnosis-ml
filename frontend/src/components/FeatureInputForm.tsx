import type { FormEvent } from "react";

import type { FeatureDefinition } from "../types/api";

interface FeatureInputFormProps {
  definitions: FeatureDefinition[];
  values: Record<string, number>;
  onChange: (name: string, value: number) => void;
  onSubmit: () => void;
  pending: boolean;
}

export function FeatureInputForm({
  definitions,
  values,
  onChange,
  onSubmit,
  pending,
}: FeatureInputFormProps) {
  const submit = (event: FormEvent) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={submit}>
      <div className="feature-grid">
        {definitions.map((feature) => (
          <div className="field" key={feature.name}>
            <label htmlFor={`feature-${feature.name}`}>{feature.name}</label>
            <input
              id={`feature-${feature.name}`}
              type="number"
              min={feature.minimum}
              max={feature.maximum}
              step="any"
              required
              value={values[feature.name] ?? feature.mean}
              onChange={(event) => onChange(feature.name, Number(event.target.value))}
            />
            <small>
              Observed {feature.minimum.toFixed(2)} to {feature.maximum.toFixed(2)}
            </small>
          </div>
        ))}
      </div>
      <button className="button button-primary" type="submit" disabled={pending}>
        {pending ? "Running model..." : "Run model prediction"}
      </button>
    </form>
  );
}
