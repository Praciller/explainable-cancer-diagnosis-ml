# ADR-0004: Artifact Identity and Semantic Replay

- Status: Accepted
- Date: 2026-09-06

## Context

`model_version` includes the SHA-256 of `models/best_model.joblib`, so it is
a byte-level artifact identity. The repository does not commit that
code-bearing model binary; supported operating systems, Python versions,
native math libraries, and serialization packages can therefore produce
different binary hashes for the same governed model behavior. CI must
regenerate the model and evidence needed for integration verification.

## Decision

Keep `model_version` as the existing byte-level artifact identity. The
committed explainability case remains tied exactly to the published
`showcase_contract.json` model version. CI reports a regenerated replay model
version separately and performs semantic replay verification across the full
86-row locked-test prediction set, row 102 score, and SHAP reconstruction
using `rtol=0` and `atol=1e-9`.

A replay binary with a different `model_version` is never silently promoted
to canonical published evidence. Binary identity mismatch is acceptable only
when all semantic replay gates pass; behavioral, data, split, threshold, and
explanation drift fails closed.

## Consequences

A fresh replay may have a different model version without representing
semantic drift. The distinction is explicit in CLI and CI evidence:
`CANONICAL_MODEL_VERSION`, `REPLAY_MODEL_VERSION`,
`BINARY_IDENTITY_MATCH`, and `SEMANTIC_REPLAY_MATCH`.

This ADR does not change governed model evidence, the current `model_version`
algorithm or canonical model version, the API contract, deployment contract,
selected model, or any canonical artifact.
