from typing import Any

import pytest

from src.utils.helpers import is_positive_integer


class TestIsPositiveInteger:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "value,expected",
        [
            (1, True),
            (100, True),
            ("1", True),
            ("99", True),
            (0, False),
            (-1, False),
            (-100, False),
            (True, False),
            (False, False),
            (None, False),
            (1.5, False),
            (0.5, False),
            ("", False),
            ("abc", False),
            ("0", False),
            ("-1", False),
            ("1.5", False),
        ],
        ids=[
            "positive_int",
            "large_positive_int",
            "positive_digit_string",
            "large_positive_digit_string",
            "zero",
            "negative_int",
            "large_negative_int",
            "bool_true",
            "bool_false",
            "none",
            "positive_float",
            "fractional_float",
            "empty_string",
            "non_numeric_string",
            "zero_string",
            "negative_string",
            "float_string",
        ],
    )
    def test_returns_expected(self, value: Any, expected: bool) -> None:
        assert is_positive_integer(value) is expected
