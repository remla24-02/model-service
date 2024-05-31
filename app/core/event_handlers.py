from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Callable, Union
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from utils.logging import AppLogger
from core.config import DEFAULT_MODEL_PATH
from services.model_service import PhishingModel
from utils.get_model import get_model

logger = AppLogger.__call__().get_logger()


def _download_model() -> None:
    logger.info("Downloading model.")
    get_model()


def _startup_model(app: FastAPI) -> None:
    logger.info("Starting up model.")

    _download_model()
    model_instance = PhishingModel(DEFAULT_MODEL_PATH)

    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def startup_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)

    return startup


def shutdown_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )
