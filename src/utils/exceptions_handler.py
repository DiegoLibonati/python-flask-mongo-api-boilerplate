from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from pydantic import ValidationError
from pymongo.errors import PyMongoError
from typing_extensions import ParamSpec

from src.configs.logger_config import setup_logger
from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_PYDANTIC
from src.constants.messages import MESSAGE_ERROR_DATABASE, MESSAGE_ERROR_PYDANTIC
from src.utils.exceptions import InternalAPIError, ValidationAPIError

logger = setup_logger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def exceptions_handler(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        except ValidationError as e:
            raise ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            )

        except PyMongoError:
            raise InternalAPIError(
                code=CODE_ERROR_DATABASE,
                message=MESSAGE_ERROR_DATABASE,
            )

    return wrapper
