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

  test("interacts with the static row-102 explainability case study", async ({ page }) => {
    const consoleErrors: string[] = [];
    const requestUrls: string[] = [];
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("request", (request) => requestUrls.push(request.url()));

    for (const viewport of [
      { width: 1440, height: 1000 },
      { width: 1024, height: 900 },
      { width: 640, height: 900 },
      { width: 390, height: 844 },
      { width: 332, height: 800 },
    ]) {
      await page.setViewportSize(viewport);
      await page.goto("/");
      const navigation = page.getByRole("navigation", { name: "Primary" });
      const explainability = navigation.getByRole("button", { name: "Explainability" });
      await explainability.click();
      await expect(explainability).toHaveAttribute("aria-current", "page");
      await expect(
        page.getByRole("heading", { name: "Row 102 explainability case study" }),
      ).toBeVisible();
      await expect(page.getByText("logistic_regression")).toBeVisible();
      await expect(page.getByText("0.008", { exact: true })).toBeVisible();
      await expect(
        page.getByText(/Base value \+ local contributions = malignant-class log-odds/i),
      ).toBeVisible();

      expect(await page.locator("html").evaluate((element) => element.scrollWidth)).toBeLessThanOrEqual(
        viewport.width,
      );
      expect(await page.locator("body").evaluate((element) => element.scrollWidth)).toBeLessThanOrEqual(
        viewport.width,
      );
      expect(requestUrls.some((url) => url.includes("127.0.0.1:8000"))).toBe(false);

      await expect(
        page.getByRole("button", { name: /show all 30 contributions/i }),
      ).toBeVisible();
      await page.getByRole("button", { name: /show all 30 contributions/i }).click();
      await expect(page.getByRole("button", { name: /feature contribution/i })).toHaveCount(30);
      const feature = page.getByRole("button", { name: /worst texture feature contribution/i });
      await feature.press("Enter");
      await expect(
        page.getByRole("region", { name: "Selected feature detail" }),
      ).toContainText("worst texture");
    }

    expect(consoleErrors).toEqual([]);
  });
});
