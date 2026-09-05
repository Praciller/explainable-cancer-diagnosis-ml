import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "./Button";

const meta = {
  title: "UI/Button",
  component: Button,
  tags: ["autodocs"],
  args: { children: "Run model prediction" },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
export const Secondary: Story = { args: { variant: "secondary", children: "Load sample" } };
export const Text: Story = { args: { variant: "text", children: "Review all inputs" } };
export const Disabled: Story = { args: { disabled: true } };
export const Focus: Story = { args: { autoFocus: true } };
