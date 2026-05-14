from typing import Any

from flask import jsonify
from flask.typing import ResponseReturnValue

from src.constants.codes import CODE_ERROR_INTERNAL_SERVER
from src.constants.messages import MESSAGE_ERROR_INTERNAL_SERVER


class BaseAPIError(Exception):
    status_code: int = 500
    message: str = MESSAGE_ERROR_INTERNAL_SERVER
    code: str = CODE_ERROR_INTERNAL_SERVER

    def __init__(
        self,
        code: str = code,
        message: str | None = None,
        status_code: int | None = None,
        payload: dict[str, Any] | None = None,
    ):
        super().__init__()
        if status_code is not None:
            self.status_code = status_code
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

        self.payload = payload or {}

    def to_dict(self) -> dict[str, Any]:
        response: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }

        if self.payload:
            response["payload"] = dict(self.payload)

        return response

    def flask_response(self) -> ResponseReturnValue:
        return jsonify(self.to_dict()), self.status_code


class ValidationAPIError(BaseAPIError):
    status_code = 400
    message = "Validation error"


class AuthenticationAPIError(BaseAPIError):
    status_code = 401
    message = "Authentication error"


class NotFoundAPIError(BaseAPIError):
    status_code = 404
    message = "Resource not found"


class ConflictAPIError(BaseAPIError):
    status_code = 409
    message = "Conflict error"


class BusinessAPIError(BaseAPIError):
    status_code = 422
    message = "Business rule violated"


class InternalAPIError(BaseAPIError):
    status_code = 500
    message = "Internal error"
