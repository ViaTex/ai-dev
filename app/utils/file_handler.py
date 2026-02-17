from __future__ import annotations

import io
from typing import Tuple

import anyio
import pdfplumber
from docx import Document
from fastapi import UploadFile

from app.utils.validators import FileTooLargeError, ParsingError


async def read_upload_file(upload_file: UploadFile, max_size_mb: int) -> bytes:
    max_bytes = max_size_mb * 1024 * 1024
    buffer = bytearray()
    while True:
        chunk = await upload_file.read(1024 * 1024)
        if not chunk:
            break
        buffer.extend(chunk)
        if len(buffer) > max_bytes:
            raise FileTooLargeError("File exceeds maximum size")
    await upload_file.close()
    return bytes(buffer)


def _extract_pdf_text(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages_text).strip()


def _extract_docx_text(file_bytes: bytes) -> str:
    document = Document(io.BytesIO(file_bytes))
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(paragraphs).strip()


async def extract_text(file_bytes: bytes, file_extension: str) -> str:
    if file_extension == "pdf":
        return await anyio.to_thread.run_sync(_extract_pdf_text, file_bytes)
    if file_extension == "docx":
        return await anyio.to_thread.run_sync(_extract_docx_text, file_bytes)
    raise ParsingError("Unsupported file type for extraction")
