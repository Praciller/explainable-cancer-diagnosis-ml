import { describe, expect, it } from "vitest";

import { resolveRuntimeConfig } from "./runtime";

describe("resolveRuntimeConfig", () => {
  it("uses hosted showcase mode for production builds without an API URL", () => {
    expect(resolveRuntimeConfig(undefined, true)).toEqual({
      apiUrl: "http://localhost:8000",
      hostedShowcase: true,
    });
  });

  it("keeps configured production builds connected to the supplied API", () => {
    expect(resolveRuntimeConfig("http://localhost:8000", true)).toEqual({
      apiUrl: "http://localhost:8000",
      hostedShowcase: false,
    });
  });
});
