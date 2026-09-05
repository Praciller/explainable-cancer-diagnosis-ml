import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test.describe("Evaluation table scroll accessibility", () => {
  test.beforeEach(() => {
    test.skip(
      !["hosted", "local"].includes(process.env.E2E_MODE ?? ""),
      "Evaluation table accessibility coverage",
    );
  });

  for (const viewport of [
    { width: 390, height: 844 },
    { width: 332, height: 720 },
  ]) {
    test(`keeps the horizontal table scroll region keyboard accessible at ${viewport.width}px`, async ({ page }) => {
      await page.setViewportSize(viewport);
      await page.goto("/");
      await page.getByRole("button", { name: "Evaluation" }).click();
      await expect(page.getByRole("heading", { name: "Keep model choice outside the test result." })).toBeVisible();

      const scrollRegion = page.locator(".table-scroll");
      await expect(scrollRegion).toHaveAttribute("role", "region");
      await expect(scrollRegion).toHaveAttribute("aria-label", "Validation-only candidate comparison table");
      await expect(scrollRegion).toHaveAttribute("tabindex", "0");
      await expect(scrollRegion.locator("caption")).toContainText("Validation-only candidate comparison");
      await expect(scrollRegion.locator("tbody th[scope='row']")).not.toHaveCount(0);

      const overflow = await scrollRegion.evaluate((element) => element.scrollWidth > element.clientWidth);
      expect(overflow).toBe(true);

      await page.locator("body").focus();
      for (let tabCount = 0; tabCount < 30; tabCount += 1) {
        await page.keyboard.press("Tab");
        if (await scrollRegion.evaluate((element) => element === document.activeElement)) break;
      }
      await expect(scrollRegion).toBeFocused();
      await expect(scrollRegion).toHaveCSS("outline-width", "3px");

      const initialScrollLeft = await scrollRegion.evaluate((element) => element.scrollLeft);
      await page.keyboard.press("ArrowRight");
      await expect.poll(() => scrollRegion.evaluate((element) => element.scrollLeft)).toBeGreaterThan(initialScrollLeft);

      const results = await new AxeBuilder({ page }).analyze();
      const severe = results.violations.filter((violation) =>
        ["serious", "critical"].includes(violation.impact ?? ""),
      );
      expect(severe, `${viewport.width}px: ${JSON.stringify(severe)}`).toEqual([]);
    });
  }
});
