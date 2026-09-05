import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  test: {
    exclude: [
      "e2e/**",
      "**/node_modules/**",
      "**/dist/**",
      "**/storybook-static/**",
      "**/playwright-report/**",
      "**/test-results/**",
    ],
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/test/setup.ts",
  },
});
