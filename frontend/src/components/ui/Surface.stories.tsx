import type { Meta, StoryObj } from "@storybook/react-vite";

import { Surface } from "./Surface";

const meta = {
  title: "UI/Surface",
  component: Surface,
  tags: ["autodocs"],
  args: { children: "A distinct evidence region", as: "section", "aria-label": "Evidence" },
} satisfies Meta<typeof Surface>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
export const Article: Story = { args: { as: "article", children: "An article surface" } };
