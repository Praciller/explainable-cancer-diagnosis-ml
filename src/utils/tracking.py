from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


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

    mlflow.set_experiment("explainable-wdbc-classification")
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(parameters)
        yield mlflow
