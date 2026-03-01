import os

from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig
from src.configs.production_config import ProductionConfig
from src.configs.testing_config import TestingConfig


class TestTestingConfigInheritance:
    def test_inherits_from_default_config(self) -> None:
        assert issubclass(TestingConfig, DefaultConfig)

    def test_inherits_timezone(self) -> None:
        assert TestingConfig.TZ == DefaultConfig.TZ

    def test_inherits_host(self) -> None:
        assert TestingConfig.HOST == DefaultConfig.HOST

    def test_inherits_port(self) -> None:
        assert TestingConfig.PORT == DefaultConfig.PORT


class TestTestingConfigOverrides:
    def test_testing_is_true(self) -> None:
        assert TestingConfig.TESTING is True

    def test_testing_is_bool(self) -> None:
        assert isinstance(TestingConfig.TESTING, bool)

    def test_testing_overrides_default(self) -> None:
        assert TestingConfig.TESTING != DefaultConfig.TESTING

    def test_debug_is_true(self) -> None:
        assert TestingConfig.DEBUG is True

    def test_debug_is_bool(self) -> None:
        assert isinstance(TestingConfig.DEBUG, bool)

    def test_debug_overrides_default(self) -> None:
        assert TestingConfig.DEBUG != DefaultConfig.DEBUG


class TestTestingConfigEnv:
    def test_env_is_testing(self) -> None:
        assert TestingConfig.ENV == "testing"

    def test_env_is_string(self) -> None:
        assert isinstance(TestingConfig.ENV, str)

    def test_env_not_in_default_config(self) -> None:
        assert not hasattr(DefaultConfig, "ENV")


class TestTestingConfigMongo:
    def test_mongo_db_name_is_string(self) -> None:
        assert isinstance(TestingConfig.MONGO_DB_NAME, str)

    def test_mongo_db_name_default_value(self) -> None:
        if "MONGO_DB_NAME" not in os.environ:
            assert TestingConfig.MONGO_DB_NAME == "templates_db"

    def test_mongo_uri_is_string(self) -> None:
        assert isinstance(TestingConfig.MONGO_URI, str)

    def test_mongo_uri_starts_with_mongodb_scheme(self) -> None:
        assert TestingConfig.MONGO_URI.startswith("mongodb://")

    def test_mongo_uri_contains_db_name(self) -> None:
        assert TestingConfig.MONGO_DB_NAME in TestingConfig.MONGO_URI

    def test_mongo_uri_overrides_default(self) -> None:
        if "MONGO_URI" not in os.environ and "MONGO_DB_NAME" not in os.environ:
            assert TestingConfig.MONGO_URI == DefaultConfig.MONGO_URI


class TestTestingConfigVsOtherConfigs:
    def test_testing_differs_from_production(self) -> None:
        assert TestingConfig.TESTING != ProductionConfig.TESTING
        assert TestingConfig.ENV != ProductionConfig.ENV

    def test_debug_differs_from_production(self) -> None:
        assert TestingConfig.DEBUG != ProductionConfig.DEBUG

    def test_env_differs_from_development(self) -> None:
        assert TestingConfig.ENV != DevelopmentConfig.ENV
