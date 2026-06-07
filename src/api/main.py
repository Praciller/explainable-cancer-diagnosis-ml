from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    FeatureListResponse,
    PredictionRequest,
    PredictionResponse,
    SampleListResponse,
)
from src.api.service import PredictionService
from src.config import MODELS_DIR, REPORTS_DIR


def create_app(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.prediction_service = PredictionService.from_artifacts(models_dir)
        yield

    app = FastAPI(
        title="Explainable Cancer Diagnosis ML API",
        version="0.1.0",
        description=(
            "Educational portfolio inference API. Not intended for medical diagnosis "
            "or clinical decision-making."
        ),
        lifespan=lifespan,
    )
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

    def service(request: Request) -> PredictionService:
        return request.app.state.prediction_service

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/model-info")
    def model_info(request: Request) -> dict:
        return service(request).model_info()

    @app.get("/features", response_model=FeatureListResponse)
    def features(request: Request) -> FeatureListResponse:
        return FeatureListResponse(features=service(request).feature_definitions())

    @app.get("/samples", response_model=SampleListResponse)
    def samples(
        request: Request,
        limit: int = Query(default=8, ge=1, le=20),
    ) -> SampleListResponse:
        return SampleListResponse(samples=service(request).samples(limit))

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest, request: Request) -> PredictionResponse:
        return service(request).predict(payload.features)

    @app.post("/predict-batch", response_model=BatchPredictionResponse)
    def predict_batch(
        payload: BatchPredictionRequest,
        request: Request,
    ) -> BatchPredictionResponse:
        predictor = service(request)
        return BatchPredictionResponse(
            results=[predictor.predict(item.features) for item in payload.items]
        )

    return app


app = create_app()
