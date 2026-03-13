from flask import Response, jsonify

from src.utils.exceptions import InternalAPIError
from src.utils.exceptions_handler import exceptions_handler


@exceptions_handler
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "author": "Diego Libonati",
        "name_bp": "Template",
    }

    return jsonify(response), 200


@exceptions_handler
def test_error() -> Response:
    message = "TemplateError test message."
    code = "CODE_TEMPLATE_ERROR_TEST_MESSAGE"

    raise InternalAPIError(code=code, message=message)
