from __future__ import annotations

from typing import Set


class InvalidAPIKeyError(Exception):
    pass


class InvalidFileTypeError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


class ParsingError(Exception):
    pass


def validate_file_type(filename: str, allowed_types: Set[str]) -> str:
    if not filename or "." not in filename:
        raise InvalidFileTypeError("File type is missing")
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in allowed_types:
        raise InvalidFileTypeError("Unsupported file type")
    return extension
