import uuid
from typing import Any

from app.models.exceptions.core_exception import ErrorModel


class NotFoundException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "not-found",
        message: str = "Item Not Found",
        details: Any = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class BadRequestException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "bad-request",
        message: str = "Bad Request",
        details: str = ""
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class BadRequestError(ErrorModel):
    details: str