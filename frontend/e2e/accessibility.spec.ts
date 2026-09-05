import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test.describe("automated accessibility checks", () => {
  test.beforeEach(() => {
    test.skip(process.env.E2E_MODE !== "hosted", "Hosted showcase accessibility coverage");
  });

  test("major hosted routes have no serious or critical axe findings", async ({ page }) => {
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

      for (const label of ["Overview", "Evaluation", "Explainability", "Prediction"]) {
        await navigation.getByRole("button", { name: label }).click();
        const results = await new AxeBuilder({ page }).analyze();
        const severe = results.violations.filter((violation) =>
          ["serious", "critical"].includes(violation.impact ?? ""),
        );
        expect(severe, `${label} at ${viewport.width}px: ${JSON.stringify(severe)}`).toEqual([]);
      }
    }
  });
});
