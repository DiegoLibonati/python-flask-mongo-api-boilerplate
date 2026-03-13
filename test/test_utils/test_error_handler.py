import pytest
from flask import Flask
from pydantic import BaseModel
from pymongo.errors import PyMongoError

from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


class TestHandleExceptionsDecorator:
    def test_passes_through_on_success(self, app: Flask) -> None:
        @exceptions_handler
        def successful_function():
            return "success"

        with app.app_context():
            result = successful_function()
            assert result == "success"

    def test_converts_validation_error(self, app: Flask) -> None:
        class StrictModel(BaseModel):
            value: int

        @exceptions_handler
        def function_with_validation():
            StrictModel(value="not an int")

        with app.app_context():
            with pytest.raises(ValidationAPIError):
                function_with_validation()

    def test_converts_pymongo_error(self, app: Flask) -> None:
        @exceptions_handler
        def function_with_mongo_error():
            raise PyMongoError("DB error")

        with app.app_context():
            with pytest.raises(InternalAPIError):
                function_with_mongo_error()

    def test_preserves_function_metadata(self) -> None:
        @exceptions_handler
        def my_function():
            """My docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."
