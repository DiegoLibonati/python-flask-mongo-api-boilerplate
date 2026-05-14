import pytest
from pydantic import BaseModel
from pymongo.errors import PyMongoError

from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_INTERNAL_SERVER, CODE_ERROR_PYDANTIC
from src.utils.exceptions import ConflictAPIError, InternalAPIError, ValidationAPIError
from src.utils.exceptions_decorator import exceptions_decorator


class _IntModel(BaseModel):
    x: int


@exceptions_decorator
def _fn_ok() -> str:
    return "result"


@exceptions_decorator
def _fn_with_args(a: int, b: int) -> int:
    return a + b


@exceptions_decorator
def _fn_raises_pydantic_error() -> None:
    _IntModel(x="bad")  # type: ignore[arg-type]


@exceptions_decorator
def _fn_raises_pymongo_error() -> None:
    raise PyMongoError("db failure")


@exceptions_decorator
def _fn_raises_runtime_error() -> None:
    raise RuntimeError("unexpected")


@exceptions_decorator
def _fn_raises_conflict_error() -> None:
    raise ConflictAPIError(code="C", message="m")


class TestExceptionsDecorator:
    @pytest.mark.unit
    def test_returns_value_when_no_exception(self) -> None:
        result: str = _fn_ok()

        assert result == "result"

    @pytest.mark.unit
    def test_passes_positional_args_through(self) -> None:
        result: int = _fn_with_args(2, 3)

        assert result == 5

    @pytest.mark.unit
    def test_preserves_function_name_via_wraps(self) -> None:
        def original() -> None:
            pass

        decorated = exceptions_decorator(original)

        assert decorated.__name__ == "original"

    @pytest.mark.unit
    def test_raises_validation_api_error_on_pydantic_error(self) -> None:
        with pytest.raises(ValidationAPIError):
            _fn_raises_pydantic_error()

    @pytest.mark.unit
    def test_validation_api_error_has_pydantic_code(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _fn_raises_pydantic_error()

        assert exc_info.value.code == CODE_ERROR_PYDANTIC

    @pytest.mark.unit
    def test_validation_api_error_payload_contains_details(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _fn_raises_pydantic_error()

        assert "details" in exc_info.value.payload
        assert isinstance(exc_info.value.payload["details"], list)

    @pytest.mark.unit
    def test_raises_internal_error_on_pymongo_error(self) -> None:
        with pytest.raises(InternalAPIError):
            _fn_raises_pymongo_error()

    @pytest.mark.unit
    def test_internal_error_has_database_code_on_pymongo_error(self) -> None:
        with pytest.raises(InternalAPIError) as exc_info:
            _fn_raises_pymongo_error()

        assert exc_info.value.code == CODE_ERROR_DATABASE

    @pytest.mark.unit
    def test_raises_internal_error_on_unexpected_exception(self) -> None:
        with pytest.raises(InternalAPIError):
            _fn_raises_runtime_error()

    @pytest.mark.unit
    def test_internal_error_has_server_code_on_unexpected_exception(self) -> None:
        with pytest.raises(InternalAPIError) as exc_info:
            _fn_raises_runtime_error()

        assert exc_info.value.code == CODE_ERROR_INTERNAL_SERVER

    @pytest.mark.unit
    def test_passes_through_base_api_error_subclass_unchanged(self) -> None:
        with pytest.raises(ConflictAPIError) as exc_info:
            _fn_raises_conflict_error()
        assert exc_info.value.code == "C"
