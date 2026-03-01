import pytest
from flask import Flask
from flask.testing import FlaskClient
from pydantic import BaseModel

from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import ValidationAPIError


class TestAliveController:
    def test_alive_returns_response_tuple(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")

        assert response.status_code == 200
        assert response.get_json() is not None

    def test_alive_response_is_serializable(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data = response.get_json()

        assert isinstance(data["message"], str)
        assert isinstance(data["version_bp"], str)
        assert isinstance(data["author"], str)
        assert isinstance(data["name_bp"], str)


class TestTestErrorController:
    def test_test_error_raises_internal_api_error(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")

        assert response.status_code == 500

        data = response.get_json()
        assert data["code"] == "CODE_TEMPLATE_ERROR_TEST_MESSAGE"

    def test_test_error_is_handled_by_error_handler(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")

        data = response.get_json()
        assert "code" in data
        assert "message" in data


class TestControllerErrorHandling:
    def test_handle_exceptions_decorator_catches_validation_error(self, app: Flask) -> None:
        class StrictModel(BaseModel):
            value: int

        @handle_exceptions
        def controller_with_validation_error():
            StrictModel(value="not an int")

        with app.app_context():
            with pytest.raises(ValidationAPIError):
                controller_with_validation_error()

    def test_controllers_return_json_response(self, client: FlaskClient) -> None:
        endpoints = [
            "/api/v1/templates/alive",
            "/api/v1/templates/test_error",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.content_type == "application/json"
