import type { Meta, StoryObj } from "@storybook/react-vite";

import { ErrorMessage } from "./ErrorMessage";

const meta = { title: "Domain/ErrorMessage", component: ErrorMessage, tags: ["autodocs"] } satisfies Meta<typeof ErrorMessage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Error: Story = { args: { message: "The local API is unavailable." } };
