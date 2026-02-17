from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.resume import router as resume_router
from app.core.logging import get_logger, setup_logging
from app.schemas.response_schema import ErrorResponse
from app.utils.validators import (
    FileTooLargeError,
    InvalidAPIKeyError,
    InvalidFileTypeError,
    ParsingError,
)

setup_logging()
logger = get_logger(__name__)

app = FastAPI()
app.include_router(resume_router)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next: Any):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        "request.completed",
        extra={
            "request_id": request_id,
            "user_id": getattr(request.state, "user_id", None),
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )
    response.headers["X-Request-Id"] = request_id
    return response


def _error_response(message: str, error: str, status_code: int) -> JSONResponse:
    payload = ErrorResponse(success=False, message=message, error=error).model_dump()
    return JSONResponse(status_code=status_code, content=payload)


@app.exception_handler(InvalidAPIKeyError)
async def invalid_api_key_handler(request: Request, exc: InvalidAPIKeyError):
    logger.error(
        "auth.invalid_api_key",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "user_id": getattr(request.state, "user_id", None),
            "error": str(exc),
        },
    )
    return _error_response("Unauthorized", str(exc), 401)


@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_handler(request: Request, exc: InvalidFileTypeError):
    logger.error(
        "file.invalid_type",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "user_id": getattr(request.state, "user_id", None),
            "error": str(exc),
        },
    )
    return _error_response("Invalid file", str(exc), 400)


@app.exception_handler(FileTooLargeError)
async def file_too_large_handler(request: Request, exc: FileTooLargeError):
    logger.error(
        "file.too_large",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "user_id": getattr(request.state, "user_id", None),
            "error": str(exc),
        },
    )
    return _error_response("File too large", str(exc), 413)


@app.exception_handler(ParsingError)
async def parsing_error_handler(request: Request, exc: ParsingError):
    logger.error(
        "parsing.failed",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "user_id": getattr(request.state, "user_id", None),
            "error": str(exc),
        },
    )
    return _error_response("Parsing failed", str(exc), 500)


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.error(
        "server.error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "user_id": getattr(request.state, "user_id", None),
            "error": str(exc),
        },
    )
    return _error_response("Internal server error", "Unexpected error", 500)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}
