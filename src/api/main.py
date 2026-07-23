from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.types import ASGIApp, Receive, Scope, Send

from src.api.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    FeatureListResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    ReadinessResponse,
    SampleListResponse,
)
from src.api.service import PredictionService
from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import EDUCATIONAL_LIMITATION

MAX_REQUEST_BODY_BYTES = 256 * 1024


def get_prediction_service(request: Request) -> PredictionService:
    return request.app.state.prediction_service


PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]


class RequestBodyLimitMiddleware:
    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            content_length = headers.get(b"content-length")
            if content_length is not None:
                try:
                    too_large = int(content_length) > self.max_bytes
                except ValueError:
                    too_large = True
                if too_large:
                    response = JSONResponse(
                        {"detail": "Request body exceeds the configured size limit."},
                        status_code=413,
                    )
                    await response(scope, receive, send)
                    return

            received_bytes = 0

            async def limited_receive() -> dict:
                nonlocal received_bytes
                message = await receive()
                if message["type"] == "http.request":
                    received_bytes += len(message.get("body", b""))
                    if received_bytes > self.max_bytes:
                        raise RequestBodyTooLarge
                return message

            try:
                await self.app(scope, limited_receive, send)
            except RequestBodyTooLarge:
                response = JSONResponse(
                    {"detail": "Request body exceeds the configured size limit."},
                    status_code=413,
                )
                await response(scope, receive, send)
            return

        await self.app(scope, receive, send)


class RequestBodyTooLarge(Exception):
    """Raised before request parsing when streamed body content exceeds the limit."""


def create_app(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.prediction_service = PredictionService.from_artifacts(
            models_dir,
            reports_dir,
        )
        yield

    app = FastAPI(
        title="Educational Explainable Classification API",
        version="0.2.0",
        description=EDUCATIONAL_LIMITATION,
        lifespan=lifespan,
    )
    app.add_middleware(RequestBodyLimitMiddleware, max_bytes=MAX_REQUEST_BODY_BYTES)
    origins = [
        value.strip()
        for value in os.getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if value.strip()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    app.mount("/reports", StaticFiles(directory=reports_dir, check_dir=False), name="reports")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", response_model=ReadinessResponse)
    def ready(predictor: PredictionServiceDep) -> ReadinessResponse:
        return ReadinessResponse(
            status="ready",
            model_version=predictor.manifest["model_version"],
            manifest_validated=True,
        )

    @app.get("/model-info", response_model=ModelInfoResponse)
    def model_info(predictor: PredictionServiceDep) -> ModelInfoResponse:
        return predictor.model_info()

    @app.get("/features", response_model=FeatureListResponse)
    def features(predictor: PredictionServiceDep) -> FeatureListResponse:
        return FeatureListResponse(features=predictor.feature_definitions())

    @app.get("/samples", response_model=SampleListResponse)
    def samples(
        predictor: PredictionServiceDep,
        limit: Annotated[int, Query(ge=1, le=20)] = 8,
    ) -> SampleListResponse:
        return SampleListResponse(samples=predictor.samples(limit))

    @app.post("/predict", response_model=PredictionResponse)
    def predict(
        payload: PredictionRequest,
        predictor: PredictionServiceDep,
    ) -> PredictionResponse:
        return predictor.predict(payload.features)

    @app.post("/predict-batch", response_model=BatchPredictionResponse)
    def predict_batch(
        payload: BatchPredictionRequest,
        predictor: PredictionServiceDep,
    ) -> BatchPredictionResponse:
        return BatchPredictionResponse(
            results=[predictor.predict(item.features) for item in payload.items]
        )

    return app


app = create_app()
