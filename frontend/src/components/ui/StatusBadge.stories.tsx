import type { Meta, StoryObj } from "@storybook/react-vite";

import { StatusBadge } from "./StatusBadge";

const meta = {
  title: "UI/StatusBadge",
  component: StatusBadge,
  tags: ["autodocs"],
  args: { children: "Model output" },
} satisfies Meta<typeof StatusBadge>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Neutral: Story = {};
export const Malignant: Story = { args: { status: "malignant", children: "Malignant class" } };
export const Benign: Story = { args: { status: "benign", children: "Benign class" } };
export const Warning: Story = { args: { status: "warning", children: "Input warning" } };
