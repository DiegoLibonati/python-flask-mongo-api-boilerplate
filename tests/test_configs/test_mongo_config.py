from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from src.configs.mongo_config import Mongo, init_mongo, mongo


class TestMongoClass:
    @pytest.mark.unit
    def test_initial_client_is_none(self) -> None:
        instance: Mongo = Mongo()
        assert instance.client is None

    @pytest.mark.unit
    def test_initial_db_is_none(self) -> None:
        instance: Mongo = Mongo()
        assert instance._db is None

    @pytest.mark.unit
    def test_init_app_sets_client(self) -> None:
        instance: Mongo = Mongo()
        mock_app: MagicMock = MagicMock(spec=Flask)
        mock_app.config = {
            "MONGO_URI": "mongodb://localhost:27017/test",
            "MONGO_DB_NAME": "test_db",
        }
        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client_instance: MagicMock = MagicMock()
            mock_client_cls.return_value = mock_client_instance
            instance.init_app(mock_app)
        assert instance.client == mock_client_instance

    @pytest.mark.unit
    def test_init_app_sets_db_using_db_name(self) -> None:
        instance: Mongo = Mongo()
        mock_app: MagicMock = MagicMock(spec=Flask)
        mock_app.config = {
            "MONGO_URI": "mongodb://localhost:27017/test",
            "MONGO_DB_NAME": "my_db",
        }
        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client_instance: MagicMock = MagicMock()
            mock_client_cls.return_value = mock_client_instance
            instance.init_app(mock_app)
        mock_client_instance.__getitem__.assert_called_once_with("my_db")

    @pytest.mark.unit
    def test_init_app_creates_client_with_uri(self) -> None:
        instance: Mongo = Mongo()
        uri: str = "mongodb://user:pass@localhost:27017/db"
        mock_app: MagicMock = MagicMock(spec=Flask)
        mock_app.config = {"MONGO_URI": uri, "MONGO_DB_NAME": "db"}
        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client_cls.return_value = MagicMock()
            instance.init_app(mock_app)
        mock_client_cls.assert_called_once_with(uri, serverSelectionTimeoutMS=5000)


class TestMongoSingleton:
    @pytest.mark.unit
    def test_mongo_is_mongo_instance(self) -> None:
        assert isinstance(mongo, Mongo)


class TestInitMongo:
    @pytest.mark.unit
    def test_calls_init_app_on_mongo(self) -> None:
        mock_app: MagicMock = MagicMock(spec=Flask)
        with patch("src.configs.mongo_config.mongo") as mock_mongo:
            init_mongo(mock_app)
        mock_mongo.init_app.assert_called_once_with(mock_app)
