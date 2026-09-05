import type { Meta, StoryObj } from "@storybook/react-vite";

import { MetricCard } from "./MetricCard";

const meta = { title: "Domain/MetricCard", component: MetricCard, tags: ["autodocs"] } satisfies Meta<typeof MetricCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Dataset: Story = { args: { label: "Dataset", value: "569 × 30", detail: "Rows and features" } };
export const ScoreStatus: Story = { args: { label: "Score status", value: "uncalibrated", detail: "Fixed threshold 0.50" } };
