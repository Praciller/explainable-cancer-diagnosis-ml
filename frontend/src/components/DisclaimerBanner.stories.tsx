import type { Meta, StoryObj } from "@storybook/react-vite";

import { DisclaimerBanner } from "./DisclaimerBanner";

const meta = { title: "Domain/DisclaimerBanner", component: DisclaimerBanner, tags: ["autodocs"] } satisfies Meta<typeof DisclaimerBanner>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
