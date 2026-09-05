import type { Meta, StoryObj } from "@storybook/react-vite";

import { Metric } from "./Metric";

const meta = {
  title: "UI/Metric",
  component: Metric,
  tags: ["autodocs"],
  args: { label: "Dataset", value: "569 × 30", detail: "Rows and features" },
} satisfies Meta<typeof Metric>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
export const Unavailable: Story = { args: { value: "Unavailable", detail: "Run the pipeline" } };
