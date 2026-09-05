import { useState } from "react";

import { Button, Callout, Metric, StatusBadge, Surface } from "./ui";
import type { CaseContribution, CaseStudyArtifact } from "../types/explainability";

interface ExplainabilityCaseStudyProps {
  artifact: CaseStudyArtifact;
}

function formatScore(value: number) {
  return value.toFixed(3);
}

function formatLogOdds(value: number) {
  return value.toFixed(4);
}

function formatContribution(value: number) {
  return `${value >= 0 ? "+" : ""}${value.toFixed(3)}`;
}

function directionLabel(direction: CaseContribution["direction"]) {
  if (direction === "toward_malignant") return "Toward malignant";
  if (direction === "away_from_malignant") return "Away from malignant";
  return "Neutral";
}

function statusForLabel(label: string) {
  return label === "malignant" ? "malignant" : label === "benign" ? "benign" : "neutral";
}

export function ExplainabilityCaseStudy({ artifact }: ExplainabilityCaseStudyProps) {
  const [expanded, setExpanded] = useState(false);
  const [selectedFeature, setSelectedFeature] = useState(artifact.contributions[0]?.feature ?? "");
  const visibleContributions = expanded ? artifact.contributions : artifact.contributions.slice(0, 8);
  const selected = artifact.contributions.find((item) => item.feature === selectedFeature) ?? artifact.contributions[0];
  const modelClassification = artifact.model_score >= artifact.threshold ? "malignant" : "benign";

  return (
    <Surface
      as="section"
      className="explainability-case-study"
      aria-label="Interactive explainability case study"
    >
      <header className="case-study-heading">
        <div>
          <span className="section-label">Local model explanation</span>
          <h2>Row {artifact.dataset_row_id} explainability case study</h2>
          <p>
            One governed locked-test dataset row shows how the selected model output is built from
            its local feature contributions.
          </p>
        </div>
        <StatusBadge status={statusForLabel(modelClassification)}>
          Model classification: {modelClassification}
        </StatusBadge>
      </header>

      <div className="case-study-metrics">
        <Metric label="Selected model" value={artifact.model_name} detail={`Artifact ${artifact.model_version}`} />
        <Metric label="Malignant-class score" value={formatScore(artifact.model_score)} detail="Uncalibrated model output" />
        <Metric label="Fixed threshold" value={artifact.threshold.toFixed(2)} detail="Governed default" />
        <Metric label="Dataset row" value={String(artifact.dataset_row_id)} detail={`Known label: ${artifact.known_label}`} />
      </div>

      <section className="case-study-reconstruction" aria-labelledby="case-study-reconstruction-title">
        <h3 id="case-study-reconstruction-title">Reconstruct the model score</h3>
        <p className="case-study-equation-label">
          Base value + local contributions = malignant-class log-odds
        </p>
        <p className="case-study-equation" aria-label="Malignant-class log-odds reconstruction">
          {formatLogOdds(artifact.base_value)} + ({formatLogOdds(artifact.contribution_sum)}) = {formatLogOdds(artifact.reconstructed_log_odds)}
        </p>
        <p>
          Sigmoid({formatLogOdds(artifact.reconstructed_log_odds)}) = {formatScore(artifact.model_score)}; this is below the fixed {artifact.threshold.toFixed(2)} threshold, so the model classification is {modelClassification}.
        </p>
        <p className="muted">Calibration status: {artifact.calibration_status}.</p>
      </section>

      <section className="case-study-contributions" aria-labelledby="case-study-contributions-title">
        <div className="case-study-section-heading">
          <div>
            <h3 id="case-study-contributions-title">Local feature contributions</h3>
            <p>
              Positive values move this model output toward the malignant class; negative values
              move it away. The signed values are in malignant-class log-odds space.
            </p>
          </div>
          <Button
            type="button"
            variant="secondary"
            aria-expanded={expanded}
            aria-controls="case-study-contribution-list"
            onClick={() => setExpanded((current) => !current)}
          >
            {expanded ? "Show top 8 contributions" : "Show all 30 contributions"}
          </Button>
        </div>

        <ol id="case-study-contribution-list" className="case-study-contribution-list">
          {visibleContributions.map((item) => {
            const selectedState = item.feature === selected?.feature;
            return (
              <li key={item.feature}>
                <button
                  type="button"
                  className={selectedState ? "case-study-contribution selected" : "case-study-contribution"}
                  aria-pressed={selectedState}
                  aria-label={`${item.feature} feature contribution: ${directionLabel(item.direction)} ${formatContribution(item.contribution)}`}
                  onClick={() => setSelectedFeature(item.feature)}
                >
                  <span className="case-study-contribution-copy">
                    <strong>{item.feature}</strong>
                    <small>
                      Rank {item.rank} · {directionLabel(item.direction)}
                    </small>
                  </span>
                  <strong className="case-study-contribution-value">
                    {formatContribution(item.contribution)}
                  </strong>
                </button>
              </li>
            );
          })}
        </ol>
      </section>

      {selected ? (
        <section className="case-study-selected-detail" aria-label="Selected feature detail">
          <span className="section-label">Selected contribution</span>
          <h3>{selected.feature}</h3>
          <dl>
            <div>
              <dt>Dataset-row value</dt>
              <dd>{selected.value.toFixed(3)}</dd>
            </div>
            <div>
              <dt>Signed contribution</dt>
              <dd>{formatContribution(selected.contribution)} log-odds</dd>
            </div>
            <div>
              <dt>Direction</dt>
              <dd>{directionLabel(selected.direction)}</dd>
            </div>
          </dl>
          <p>
            Direction is model behavior rather than causality or a biological explanation for
            this row.
          </p>
        </section>
      ) : null}

      <div className="case-study-explanation-columns">
        <section aria-labelledby="case-study-global-title">
          <h3 id="case-study-global-title">Global explanation</h3>
          <p>{artifact.global_explanation}</p>
        </section>
        <section aria-labelledby="case-study-local-title">
          <h3 id="case-study-local-title">Local explanation</h3>
          <p>{artifact.local_explanation}</p>
        </section>
      </div>

      <Callout tone="disclaimer" title="Educational scope">
        <p>{artifact.educational_limitation}</p>
      </Callout>
    </Surface>
  );
}
