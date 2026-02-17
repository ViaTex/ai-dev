from __future__ import annotations

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.resume_schema import ResumeSchema
from app.services.llm_service import parse_resume_with_llm
from app.utils.file_handler import extract_text, read_upload_file
from app.utils.hashing import sha256_bytes
from app.utils.validators import ParsingError, validate_file_type

logger = get_logger(__name__)


async def parse_resume(user_id: str, upload_file: UploadFile) -> ResumeSchema:
    settings = get_settings()
    allowed_types = settings.allowed_file_type_set()
    file_extension = validate_file_type(upload_file.filename or "", allowed_types)

    logger.info(
        "resume.parse_start",
        extra={"user_id": user_id, "original_filename": upload_file.filename, "file_type": file_extension},
    )

    file_bytes = await read_upload_file(upload_file, settings.max_file_size_mb)
    _file_hash = sha256_bytes(file_bytes)

    logger.info(
        "resume.file_read",
        extra={"user_id": user_id, "file_size": len(file_bytes), "file_hash": _file_hash},
    )

    resume_text = await extract_text(file_bytes, file_extension)
    if not resume_text.strip():
        raise ParsingError("No text extracted from resume")

    logger.info(
        "resume.text_extracted",
        extra={"user_id": user_id, "text_length": len(resume_text)},
    )

    return await parse_resume_with_llm(resume_text)
