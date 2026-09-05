import type { Meta, StoryObj } from "@storybook/react-vite";

import contract from "../data/showcase_contract.json";
import type { EvaluationReport } from "../types/api";
import { ModelComparisonTable } from "./ModelComparisonTable";

const report = contract.evaluation as EvaluationReport;

const meta = {
  title: "Domain/ModelComparisonTable",
  component: ModelComparisonTable,
  tags: ["autodocs"],
  args: { report },
} satisfies Meta<typeof ModelComparisonTable>;

export default meta;
type Story = StoryObj<typeof meta>;

export const ValidationEvidence: Story = {};
export const Empty: Story = { args: { report: null } };
