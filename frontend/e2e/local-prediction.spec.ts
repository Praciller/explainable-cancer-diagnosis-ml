import { test, expect } from "@playwright/test";

test.describe("local prediction integration", () => {
  test.beforeEach(() => {
    test.skip(process.env.E2E_MODE !== "local", "Local FastAPI coverage");
  });

  test("runs a dataset sample through the real FastAPI service", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Evidence with an explicit boundary." })).toBeVisible();

    await page.getByRole("navigation", { name: "Primary" }).getByRole("button", { name: "Prediction" }).click();
    await expect(page.getByRole("heading", { name: "Start with a governed dataset row." })).toBeVisible();
    await page.getByRole("button", { name: "Load sample" }).click();
    await page.getByRole("button", { name: "Run model prediction" }).click();

    await expect(page.getByText(/malignant-class model score/i)).toBeVisible();
    await expect(page.getByText(/calibration status: uncalibrated/i)).toBeVisible();
    await expect(page.locator(".result-disclaimer")).toContainText(
      /educational machine-learning portfolio demonstration/i,
    );
    await page.screenshot({ path: "test-results/local-prediction.png", fullPage: true });
  });
});
