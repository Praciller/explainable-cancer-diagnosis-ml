/* global URL, console, process */

import { readdir, stat } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const assetsDirectory = fileURLToPath(new URL("../dist/assets/", import.meta.url));
const budgets = { js: 600_000, css: 30_000 };
const files = (await readdir(assetsDirectory)).filter((file) => /\.(js|css)$/.test(file));
const sizes = await Promise.all(
  files.map(async (file) => ({ file, bytes: (await stat(join(assetsDirectory, file))).size })),
);
const totals = {
  js: sizes.filter(({ file }) => file.endsWith(".js")).reduce((total, { bytes }) => total + bytes, 0),
  css: sizes.filter(({ file }) => file.endsWith(".css")).reduce((total, { bytes }) => total + bytes, 0),
};

for (const kind of ["js", "css"]) {
  console.log(`bundle ${kind}: ${totals[kind]} bytes (budget ${budgets[kind]} bytes)`);
}
for (const { file, bytes } of sizes.sort((a, b) => b.bytes - a.bytes)) {
  console.log(`  ${file}: ${bytes} bytes`);
}

const failures = Object.entries(budgets).filter(([kind, budget]) => totals[kind] > budget);
if (failures.length > 0) {
  console.error(`Bundle budget exceeded: ${failures.map(([kind]) => kind).join(", ")}`);
  process.exitCode = 1;
}
