import { test, expect } from "@playwright/test";

test.describe("deterministic API edge states", () => {
  test.beforeEach(() => {
    test.skip(process.env.E2E_MODE !== "local", "Local API edge-state coverage");
  });

  test("shows an accessible error when model metadata cannot load", async ({ page }) => {
    await page.route("**/model-info", (route) => route.abort());
    await page.goto("/");

    await expect(page.getByRole("alert")).toContainText("Request could not be completed");
    await expect(page.getByText(/educational model evidence only/i)).not.toBeVisible();
  });
});
