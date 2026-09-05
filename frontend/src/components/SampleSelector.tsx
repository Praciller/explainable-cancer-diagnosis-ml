import { useState } from "react";

import type { SampleRecord } from "../types/api";
import { Button } from "./ui";

interface SampleSelectorProps {
  samples: SampleRecord[];
  onSelect: (sample: SampleRecord) => void;
}

export function SampleSelector({ samples, onSelect }: SampleSelectorProps) {
  const [selectedId, setSelectedId] = useState(samples[0]?.dataset_row_id.toString() ?? "");
  const effectiveSelectedId = selectedId || samples[0]?.dataset_row_id.toString() || "";

  const loadSample = () => {
    const selected = samples.find(
      (sample) => sample.dataset_row_id.toString() === effectiveSelectedId,
    );
    if (selected) onSelect(selected);
  };

  return (
    <div className="sample-selector">
      <div>
        <label htmlFor="sample-record">Sample record</label>
        <select
          id="sample-record"
          value={effectiveSelectedId}
          onChange={(event) => setSelectedId(event.target.value)}
        >
          {samples.map((sample) => (
            <option key={sample.dataset_row_id} value={sample.dataset_row_id}>
              Dataset row {sample.dataset_row_id}, reference label: {sample.known_label}
            </option>
          ))}
        </select>
      </div>
      <Button variant="secondary" type="button" onClick={loadSample}>
        Load sample
      </Button>
    </div>
  );
}
