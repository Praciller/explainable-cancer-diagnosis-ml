import {
  Activity,
  BarChart3,
  BrainCircuit,
  FlaskConical,
  Microscope,
} from "lucide-react";
import { lazy, Suspense, useEffect, useState } from "react";

import { ErrorMessage } from "./components/ErrorMessage";
import { LoadingState } from "./components/LoadingState";
import {
  getEvaluationReport,
  getFeatures,
  getModelInfo,
  getSamples,
  HOSTED_SHOWCASE,
} from "./services/api";
import type {
  EvaluationReport,
  FeatureDefinition,
  ModelInfo,
  SampleRecord,
} from "./types/api";

type Page = "overview" | "prediction" | "evaluation" | "explainability";

const OverviewPage = lazy(() =>
  import("./pages/OverviewPage").then((module) => ({ default: module.OverviewPage })),
);
const PredictionPage = lazy(() =>
  import("./pages/PredictionPage").then((module) => ({ default: module.PredictionPage })),
);
const EvaluationPage = lazy(() =>
  import("./pages/EvaluationPage").then((module) => ({ default: module.EvaluationPage })),
);
const ExplainabilityPage = lazy(() =>
  import("./pages/ExplainabilityPage").then((module) => ({
    default: module.ExplainabilityPage,
  })),
);

const navigation = [
  { id: "overview" as const, label: "Overview", icon: Activity },
  { id: "prediction" as const, label: "Prediction", icon: FlaskConical },
  { id: "evaluation" as const, label: "Evaluation", icon: BarChart3 },
  { id: "explainability" as const, label: "Explainability", icon: BrainCircuit },
];

export default function App() {
  const [page, setPage] = useState<Page>("overview");
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [features, setFeatures] = useState<FeatureDefinition[]>([]);
  const [samples, setSamples] = useState<SampleRecord[]>([]);
  const [evaluation, setEvaluation] = useState<EvaluationReport | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getModelInfo(), getFeatures(), getSamples(), getEvaluationReport()])
      .then(([info, featureList, sampleList, report]) => {
        setError("");
        setModelInfo(info);
        setFeatures(featureList);
        setSamples(sampleList);
        setEvaluation(report);
      })
      .catch((requestError: unknown) => {
        setError(
          requestError instanceof Error
            ? requestError.message
            : "The dashboard could not reach the API.",
        );
      });
  }, []);

  const navigate = (nextPage: Page) => {
    setPage(nextPage);
    window.history.replaceState(null, "", `#${nextPage}`);
    document.querySelector("main")?.focus();
  };

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <aside className="sidebar">
        <div className="brand">
          <Microscope aria-hidden="true" />
          <div>
            <strong>Model Evidence Lab</strong>
            <span>Breast cancer WDBC</span>
          </div>
        </div>
        <nav aria-label="Primary">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                className={page === item.id ? "active" : ""}
                aria-current={page === item.id ? "page" : undefined}
                onClick={() => navigate(item.id)}
              >
                <Icon aria-hidden="true" size={19} />
                {item.label}
              </button>
            );
          })}
        </nav>
        <p className="sidebar-note">Educational portfolio system. Not for clinical use.</p>
      </aside>

      <main id="main-content" tabIndex={-1}>
        {HOSTED_SHOWCASE ? (
          <div className="deployment-banner" role="status">
            <strong>Frontend showcase</strong>
            <span>Live inference remains local via Docker Compose for v1.</span>
          </div>
        ) : null}
        {error ? <ErrorMessage message={error} /> : null}
        {!modelInfo && !error ? <LoadingState /> : null}
        <Suspense fallback={<LoadingState label="Loading dashboard page" />}>
          {modelInfo && page === "overview" ? (
            <OverviewPage
              modelInfo={modelInfo}
              evaluation={evaluation}
              onStart={() => navigate("prediction")}
            />
          ) : null}
          {modelInfo && page === "prediction" ? (
            <PredictionPage
              features={features}
              samples={samples}
              hostedShowcase={HOSTED_SHOWCASE}
            />
          ) : null}
          {modelInfo && page === "evaluation" ? <EvaluationPage report={evaluation} /> : null}
          {modelInfo && page === "explainability" ? <ExplainabilityPage /> : null}
        </Suspense>
      </main>
    </div>
  );
}
