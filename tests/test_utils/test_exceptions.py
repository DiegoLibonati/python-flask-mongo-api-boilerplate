from typing import Any

import pytest
from flask import Flask

from src.constants.codes import CODE_ERROR_INTERNAL_SERVER
from src.constants.messages import MESSAGE_ERROR_INTERNAL_SERVER
from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


@pytest.fixture(scope="module")
def flask_app() -> Flask:
    return Flask(__name__)


class TestBaseAPIError:
    @pytest.mark.unit
    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.status_code == 500

    @pytest.mark.unit
    def test_default_code_is_internal_server_error(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.code == CODE_ERROR_INTERNAL_SERVER

    @pytest.mark.unit
    def test_default_message_is_internal_server_error(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.message == MESSAGE_ERROR_INTERNAL_SERVER

    @pytest.mark.unit
    def test_custom_status_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)

        assert error.status_code == 418

    @pytest.mark.unit
    def test_custom_message_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom message")

        assert error.message == "custom message"

    @pytest.mark.unit
    def test_custom_code_is_set(self) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE")

        assert error.code == "MY_CODE"

    @pytest.mark.unit
    def test_payload_defaults_to_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.payload == {}

    @pytest.mark.unit
    def test_payload_is_stored_when_provided(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"key": "value"})

        assert error.payload == {"key": "value"}

    @pytest.mark.unit
    def test_is_instance_of_exception(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(BaseAPIError):
            raise BaseAPIError(code="C", message="m")

    @pytest.mark.unit
    def test_to_dict_contains_code(self) -> None:
        error: BaseAPIError = BaseAPIError(code="TEST_CODE", message="m")

        result: dict[str, Any] = error.to_dict()

        assert result["code"] == "TEST_CODE"

    @pytest.mark.unit
    def test_to_dict_contains_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="C", message="test message")

        result: dict[str, Any] = error.to_dict()

        assert result["message"] == "test message"

    @pytest.mark.unit
    def test_to_dict_includes_payload_when_non_empty(self) -> None:
        error: BaseAPIError = BaseAPIError(code="C", message="m", payload={"detail": "info"})

        result: dict[str, Any] = error.to_dict()

        assert "payload" in result
        assert result["payload"] == {"detail": "info"}

    @pytest.mark.unit
    def test_to_dict_excludes_payload_key_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError(code="C", message="m")

        result: dict[str, Any] = error.to_dict()

        assert "payload" not in result

    @pytest.mark.unit
    def test_flask_response_returns_correct_status(self, flask_app: Flask) -> None:
        error: BaseAPIError = BaseAPIError(code="C", message="m", status_code=418)

        with flask_app.app_context():
            response, status = error.flask_response()

        assert status == 418

    @pytest.mark.unit
    def test_flask_response_body_contains_code(self, flask_app: Flask) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE", message="m")

        with flask_app.app_context():
            response, status = error.flask_response()
            data: dict[str, Any] = response.get_json()

        assert data["code"] == "MY_CODE"

    @pytest.mark.unit
    def test_flask_response_body_contains_message(self, flask_app: Flask) -> None:
        error: BaseAPIError = BaseAPIError(code="C", message="my message")

        with flask_app.app_context():
            response, status = error.flask_response()
            data: dict[str, Any] = response.get_json()

        assert data["message"] == "my message"


class TestValidationAPIError:
    @pytest.mark.unit
    def test_has_400_status_code(self) -> None:
        assert ValidationAPIError.status_code == 400

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(ValidationAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_400_status(self) -> None:
        error: ValidationAPIError = ValidationAPIError(code="C", message="m")

        assert error.status_code == 400


class TestAuthenticationAPIError:
    @pytest.mark.unit
    def test_has_401_status_code(self) -> None:
        assert AuthenticationAPIError.status_code == 401

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(AuthenticationAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_401_status(self) -> None:
        error: AuthenticationAPIError = AuthenticationAPIError(code="C", message="m")

        assert error.status_code == 401


class TestNotFoundAPIError:
    @pytest.mark.unit
    def test_has_404_status_code(self) -> None:
        assert NotFoundAPIError.status_code == 404

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(NotFoundAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_404_status(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError(code="C", message="m")

        assert error.status_code == 404


class TestConflictAPIError:
    @pytest.mark.unit
    def test_has_409_status_code(self) -> None:
        assert ConflictAPIError.status_code == 409

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(ConflictAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_409_status(self) -> None:
        error: ConflictAPIError = ConflictAPIError(code="C", message="m")

        assert error.status_code == 409


class TestBusinessAPIError:
    @pytest.mark.unit
    def test_has_422_status_code(self) -> None:
        assert BusinessAPIError.status_code == 422

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(BusinessAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_422_status(self) -> None:
        error: BusinessAPIError = BusinessAPIError(code="C", message="m")

        assert error.status_code == 422


class TestInternalAPIError:
    @pytest.mark.unit
    def test_has_500_status_code(self) -> None:
        assert InternalAPIError.status_code == 500

    @pytest.mark.unit
    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(InternalAPIError, BaseAPIError)

    @pytest.mark.unit
    def test_instance_has_500_status(self) -> None:
        error: InternalAPIError = InternalAPIError(code="C", message="m")

        assert error.status_code == 500
