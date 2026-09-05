import { test, expect } from "@playwright/test";

test.describe("hosted read-only showcase", () => {
  test.beforeEach(() => {
    test.skip(process.env.E2E_MODE !== "hosted", "Hosted-only coverage");
  });

  test("loads evidence and navigates every public page", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Evidence with an explicit boundary." })).toBeVisible();
    await expect(page.getByText("Read-only evidence. Live dataset-row inference remains local.")).toBeVisible();
    await expect(page.getByRole("link", { name: "Skip to main content" })).toBeAttached();

    const navigation = page.getByRole("navigation", { name: "Primary" });
    for (const [label, heading] of [
      ["Evaluation", "Keep model choice outside the test result."],
      ["Explainability", "Explain behavior without claiming causality."],
      ["Prediction", "Live inference stays local for v1."],
    ]) {
      await navigation.getByRole("button", { name: label }).click();
      await expect(page.getByRole("heading", { name: heading })).toBeVisible();
    }

    await expect(page.getByText(/not intended for diagnosis, screening, treatment/i)).toBeVisible();
    await expect(page.locator("body")).not.toContainText("model confidence");
    await page.screenshot({ path: "test-results/hosted-showcase.png", fullPage: true });
  });

  test("supports keyboard skip navigation and mobile reflow", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Tab");
    await expect(page.getByRole("link", { name: "Skip to main content" })).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page.locator("main")).toBeFocused();
    await expect(page.locator("body")).toHaveCSS("overflow-x", "visible");
  });
});
