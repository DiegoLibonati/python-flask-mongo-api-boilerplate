from typing import Any

import pytest
from flask.testing import FlaskClient

from src.constants.codes import CODE_SUCCESS_HEALTH
from src.constants.messages import MESSAGE_SUCCESS_HEALTH


class TestHealthRoute:
    @pytest.mark.integration
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")

        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")

        assert response.content_type == "application/json"

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH

    @pytest.mark.integration
    def test_unknown_health_subroute_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/status")

        assert response.status_code == 404
