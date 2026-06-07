interface RuntimeConfig {
  apiUrl: string;
  hostedShowcase: boolean;
}

export function resolveRuntimeConfig(
  configuredApiUrl: string | undefined,
  isProduction: boolean,
): RuntimeConfig {
  const apiUrl = configuredApiUrl?.trim();

  return {
    apiUrl: apiUrl || "http://localhost:8000",
    hostedShowcase: isProduction && !apiUrl,
  };
}

export const RUNTIME_CONFIG = resolveRuntimeConfig(
  import.meta.env.VITE_API_URL,
  import.meta.env.PROD,
);
