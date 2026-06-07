import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

import type { SampleRecord } from "../types/api";
import { SampleSelector } from "./SampleSelector";

const samples: SampleRecord[] = [
  { id: 0, known_label: "malignant", features: { "mean radius": 17.99 } },
  { id: 1, known_label: "benign", features: { "mean radius": 12.45 } },
];

test("loads a selected complete sample into the prediction workflow", async () => {
  const onSelect = vi.fn();
  render(<SampleSelector samples={samples} onSelect={onSelect} />);

  await userEvent.selectOptions(screen.getByLabelText(/sample record/i), "1");
  await userEvent.click(screen.getByRole("button", { name: /load sample/i }));

  expect(onSelect).toHaveBeenCalledWith(samples[1]);
});
