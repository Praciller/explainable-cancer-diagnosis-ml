import type { Meta, StoryObj } from "@storybook/react-vite";

import caseArtifactJson from "../data/explainability_case.json";
import type { CaseStudyArtifact } from "../types/explainability";
import { ExplainabilityCaseStudy } from "./ExplainabilityCaseStudy";

const caseArtifact = caseArtifactJson as unknown as CaseStudyArtifact;

const meta = {
  title: "Domain/ExplainabilityCaseStudy",
  component: ExplainabilityCaseStudy,
  tags: ["autodocs"],
  args: { artifact: caseArtifact },
} satisfies Meta<typeof ExplainabilityCaseStudy>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const FeatureSelected: Story = {
  play: async ({ canvasElement }) => {
    canvasElement
      .querySelector<HTMLButtonElement>('button[aria-label^="mean compactness feature contribution"]')
      ?.click();
  },
};

export const AllContributions: Story = {
  play: async ({ canvasElement }) => {
    canvasElement.querySelector<HTMLButtonElement>('button[aria-expanded="false"]')?.click();
  },
};

export const Mobile: Story = {
  parameters: {
    viewport: { defaultViewport: "mobile1" },
  },
};
