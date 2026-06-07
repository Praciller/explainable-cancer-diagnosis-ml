from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


@contextmanager
def optional_mlflow_run(
    enabled: bool,
    run_name: str,
    parameters: dict[str, Any],
) -> Iterator[Any | None]:
    if not enabled:
        yield None
        return

    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError("MLflow was enabled but is not installed.") from exc

    mlflow.set_experiment("explainable-cancer-diagnosis")
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(parameters)
        yield mlflow
