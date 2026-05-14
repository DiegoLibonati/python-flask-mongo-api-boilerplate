import traceback
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from pydantic import ValidationError
from pymongo.errors import PyMongoError
from typing_extensions import ParamSpec

from src.configs.logger_config import setup_logger
from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_INTERNAL_SERVER, CODE_ERROR_PYDANTIC
from src.constants.messages import MESSAGE_ERROR_DATABASE, MESSAGE_ERROR_INTERNAL_SERVER, MESSAGE_ERROR_PYDANTIC
from src.utils.exceptions import BaseAPIError, InternalAPIError, ValidationAPIError

logger = setup_logger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def exceptions_decorator(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        except BaseAPIError:
            raise

        except ValidationError as e:
            logger.warning("Validation error in %s: %s", fn.__name__, e)
            raise ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            ) from e

        except PyMongoError as e:
            logger.error("Database error in %s: %s", fn.__name__, e)
            raise InternalAPIError(
                code=CODE_ERROR_DATABASE,
                message=MESSAGE_ERROR_DATABASE,
            ) from e

        except Exception as e:
            logger.error("Unexpected error in %s: %s\n%s", fn.__name__, e, traceback.format_exc())
            raise InternalAPIError(
                code=CODE_ERROR_INTERNAL_SERVER,
                message=MESSAGE_ERROR_INTERNAL_SERVER,
            ) from e

    return wrapper
