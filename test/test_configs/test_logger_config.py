import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        assert isinstance(setup_logger(), logging.Logger)

    def test_logger_has_correct_name(self) -> None:
        logger = setup_logger("test-logger")
        assert logger.name == "test-logger"

    def test_logger_uses_default_name(self) -> None:
        logger = setup_logger()
        assert logger.name == "flask-app"

    def test_logger_has_debug_level(self) -> None:
        logger = setup_logger("test-level")
        assert logger.level == logging.DEBUG

    def test_logger_has_handler(self) -> None:
        logger = setup_logger("test-handler")
        assert len(logger.handlers) > 0

    def test_logger_does_not_duplicate_handlers(self) -> None:
        logger = setup_logger("test-no-duplicate")
        initial_count = len(logger.handlers)
        setup_logger("test-no-duplicate")
        assert len(logger.handlers) == initial_count

    def test_same_name_returns_same_logger(self) -> None:
        logger1 = setup_logger("test-same")
        logger2 = setup_logger("test-same")
        assert logger1 is logger2

    def test_different_names_return_different_loggers(self) -> None:
        logger1 = setup_logger("test-diff-1")
        logger2 = setup_logger("test-diff-2")
        assert logger1 is not logger2

    def test_handler_is_stream_handler(self) -> None:
        logger = setup_logger("test-stream-handler")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_handler_has_formatter(self) -> None:
        logger = setup_logger("test-formatter")
        for handler in logger.handlers:
            assert handler.formatter is not None

    def test_formatter_includes_levelname(self) -> None:
        logger = setup_logger("test-fmt-level")
        for handler in logger.handlers:
            assert "%(levelname)s" in handler.formatter._fmt

    def test_formatter_includes_name(self) -> None:
        logger = setup_logger("test-fmt-name")
        for handler in logger.handlers:
            assert "%(name)s" in handler.formatter._fmt

    def test_formatter_includes_message(self) -> None:
        logger = setup_logger("test-fmt-msg")
        for handler in logger.handlers:
            assert "%(message)s" in handler.formatter._fmt
