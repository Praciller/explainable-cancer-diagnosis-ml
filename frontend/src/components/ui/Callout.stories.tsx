import type { Meta, StoryObj } from "@storybook/react-vite";

import { Callout } from "./Callout";

const meta = {
  title: "UI/Callout",
  component: Callout,
  tags: ["autodocs"],
  args: { title: "Educational model evidence only", children: <p>Review the limitations before interpreting the output.</p> },
} satisfies Meta<typeof Callout>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Disclaimer: Story = {};
export const Warning: Story = { args: { tone: "warning", title: "Input warnings" } };
export const Error: Story = { args: { tone: "error", title: "Request could not be completed" } };
