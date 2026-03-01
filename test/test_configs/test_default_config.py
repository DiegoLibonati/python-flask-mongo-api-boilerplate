import os

import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfigGeneral:
    def test_tz_is_string(self) -> None:
        assert isinstance(DefaultConfig.TZ, str)

    def test_tz_default_value(self) -> None:
        if "TZ" not in os.environ:
            assert DefaultConfig.TZ == "America/Argentina/Buenos_Aires"

    def test_tz_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        result = os.getenv("TZ", "America/Argentina/Buenos_Aires")
        assert isinstance(result, str)

    def test_json_as_ascii_is_false(self) -> None:
        assert DefaultConfig.JSON_AS_ASCII is False

    def test_json_as_ascii_is_bool(self) -> None:
        assert isinstance(DefaultConfig.JSON_AS_ASCII, bool)

    def test_debug_is_false(self) -> None:
        assert DefaultConfig.DEBUG is False

    def test_debug_is_bool(self) -> None:
        assert isinstance(DefaultConfig.DEBUG, bool)

    def test_testing_is_false(self) -> None:
        assert DefaultConfig.TESTING is False

    def test_testing_is_bool(self) -> None:
        assert isinstance(DefaultConfig.TESTING, bool)


class TestDefaultConfigMongo:
    def test_mongo_host_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_HOST, str)

    def test_mongo_host_default_value(self) -> None:
        if "MONGO_HOST" not in os.environ:
            assert DefaultConfig.MONGO_HOST == "host.docker.internal"

    def test_mongo_port_default_value(self) -> None:
        if "MONGO_PORT" not in os.environ:
            assert DefaultConfig.MONGO_PORT == 27017

    def test_mongo_user_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_USER, str)

    def test_mongo_user_default_value(self) -> None:
        if "MONGO_USER" not in os.environ:
            assert DefaultConfig.MONGO_USER == "admin"

    def test_mongo_pass_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_PASS, str)

    def test_mongo_pass_default_value(self) -> None:
        if "MONGO_PASS" not in os.environ:
            assert DefaultConfig.MONGO_PASS == "secret123"

    def test_mongo_db_name_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_DB_NAME, str)

    def test_mongo_db_name_default_value(self) -> None:
        if "MONGO_DB_NAME" not in os.environ:
            assert DefaultConfig.MONGO_DB_NAME == "templates_db"

    def test_mongo_auth_source_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_AUTH_SOURCE, str)

    def test_mongo_auth_source_default_value(self) -> None:
        if "MONGO_AUTH_SOURCE" not in os.environ:
            assert DefaultConfig.MONGO_AUTH_SOURCE == "admin"

    def test_mongo_uri_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_URI, str)

    def test_mongo_uri_contains_host(self) -> None:
        assert DefaultConfig.MONGO_HOST in DefaultConfig.MONGO_URI

    def test_mongo_uri_contains_user(self) -> None:
        assert DefaultConfig.MONGO_USER in DefaultConfig.MONGO_URI

    def test_mongo_uri_contains_db_name(self) -> None:
        assert DefaultConfig.MONGO_DB_NAME in DefaultConfig.MONGO_URI

    def test_mongo_uri_contains_auth_source(self) -> None:
        assert DefaultConfig.MONGO_AUTH_SOURCE in DefaultConfig.MONGO_URI

    def test_mongo_uri_starts_with_mongodb_scheme(self) -> None:
        assert DefaultConfig.MONGO_URI.startswith("mongodb://")


class TestDefaultConfigFlask:
    def test_host_is_string(self) -> None:
        assert isinstance(DefaultConfig.HOST, str)

    def test_host_default_value(self) -> None:
        if "HOST" not in os.environ:
            assert DefaultConfig.HOST == "0.0.0.0"

    def test_port_default_value(self) -> None:
        if "PORT" not in os.environ:
            assert DefaultConfig.PORT == 5000
