import type {
  EvaluationReport,
  FeatureDefinition,
  ModelInfo,
  PredictionResponse,
  SampleRecord,
} from "../types/api";
import { SHOWCASE_EVALUATION, SHOWCASE_MODEL_INFO } from "../data/showcase";
import { RUNTIME_CONFIG } from "./runtime";

export const API_URL = RUNTIME_CONFIG.apiUrl;
export const HOSTED_SHOWCASE = RUNTIME_CONFIG.hostedShowcase;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : "The API could not complete this request. Check that trained model artifacts exist.";
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export async function getModelInfo(): Promise<ModelInfo> {
  if (HOSTED_SHOWCASE) {
    return SHOWCASE_MODEL_INFO;
  }
  return request<ModelInfo>("/model-info");
}

export async function getFeatures(): Promise<FeatureDefinition[]> {
  if (HOSTED_SHOWCASE) {
    return [];
  }
  const response = await request<{ features: FeatureDefinition[] }>("/features");
  return response.features;
}

export async function getSamples(): Promise<SampleRecord[]> {
  if (HOSTED_SHOWCASE) {
    return [];
  }
  const response = await request<{ samples: SampleRecord[] }>("/samples?limit=8");
  return response.samples;
}

export async function getEvaluationReport(): Promise<EvaluationReport | null> {
  if (HOSTED_SHOWCASE) {
    return SHOWCASE_EVALUATION;
  }
  const response = await fetch(`${API_URL}/reports/evaluation_metrics.json`);
  return response.ok ? ((await response.json()) as EvaluationReport) : null;
}

export async function predict(features: Record<string, number>): Promise<PredictionResponse> {
  if (HOSTED_SHOWCASE) {
    throw new Error("Live inference requires the local Docker API.");
  }
  return request<PredictionResponse>("/predict", {
    method: "POST",
    body: JSON.stringify({ features }),
  });
}

export function reportUrl(filename: string): string {
  if (HOSTED_SHOWCASE) {
    return `/reports/figures/${filename}`;
  }
  return `${API_URL}/reports/figures/${filename}`;
}
