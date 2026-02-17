from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.resume_schema import ResumeSchema


class SuccessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: Literal[True]
    message: str
    data: ResumeSchema


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: Literal[False]
    message: str
    error: str
