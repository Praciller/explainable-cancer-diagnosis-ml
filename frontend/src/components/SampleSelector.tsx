import { useEffect, useState } from "react";

import type { SampleRecord } from "../types/api";

interface SampleSelectorProps {
  samples: SampleRecord[];
  onSelect: (sample: SampleRecord) => void;
}

export function SampleSelector({ samples, onSelect }: SampleSelectorProps) {
  const [selectedId, setSelectedId] = useState(samples[0]?.id.toString() ?? "");

  useEffect(() => {
    if (!selectedId && samples[0]) {
      setSelectedId(samples[0].id.toString());
    }
  }, [samples, selectedId]);

  const loadSample = () => {
    const selected = samples.find((sample) => sample.id.toString() === selectedId);
    if (selected) onSelect(selected);
  };

  return (
    <div className="sample-selector">
      <div>
        <label htmlFor="sample-record">Sample record</label>
        <select
          id="sample-record"
          value={selectedId}
          onChange={(event) => setSelectedId(event.target.value)}
        >
          {samples.map((sample) => (
            <option key={sample.id} value={sample.id}>
              Sample {sample.id + 1}, known label: {sample.known_label}
            </option>
          ))}
        </select>
      </div>
      <button className="button button-secondary" type="button" onClick={loadSample}>
        Load sample
      </button>
    </div>
  );
}
