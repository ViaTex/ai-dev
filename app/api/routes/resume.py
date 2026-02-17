from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Request, Response, UploadFile

from app.core.security import verify_internal_api_key
from app.schemas.response_schema import SuccessResponse
from app.services.resume_parser import parse_resume

router = APIRouter()


@router.post("/resume-parse", response_model=SuccessResponse)
async def resume_parse(
    request: Request,
    response: Response,
    user_id: str = Form(...),
    file: UploadFile = File(...),
    _: None = Depends(verify_internal_api_key),
) -> SuccessResponse:
    request.state.user_id = user_id
    parsed_resume = await parse_resume(user_id, file)
    response.headers["X-User-Id"] = user_id
    return SuccessResponse(
        success=True,
        message="Resume parsed successfully",
        data=parsed_resume,
    )
