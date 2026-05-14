from typing import Any

import pytest
from flask import Flask

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY
from src.controllers.health_controller import health, ready


class TestHealthController:
    @pytest.mark.unit
    def test_returns_200(self, app: Flask) -> None:
        with app.app_context():
            response, status = health()

        assert status == 200

    @pytest.mark.unit
    def test_response_contains_code(self, app: Flask) -> None:
        with app.app_context():
            response, status = health()
            data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    @pytest.mark.unit
    def test_response_contains_message(self, app: Flask) -> None:
        with app.app_context():
            response, status = health()
            data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH


class TestReadyController:
    @pytest.mark.unit
    def test_returns_200(self, app: Flask) -> None:
        with app.app_context():
            response, status = ready()

        assert status == 200

    @pytest.mark.unit
    def test_response_contains_code(self, app: Flask) -> None:
        with app.app_context():
            response, status = ready()
            data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_READY

    @pytest.mark.unit
    def test_response_contains_message(self, app: Flask) -> None:
        with app.app_context():
            response, status = ready()
            data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_READY
