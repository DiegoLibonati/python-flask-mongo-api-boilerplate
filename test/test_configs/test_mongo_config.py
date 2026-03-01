from unittest.mock import MagicMock, patch

from flask import Flask

from src.configs.mongo_config import Mongo, init_mongo, mongo


class TestMongoClass:
    def test_mongo_client_is_none_on_init(self) -> None:
        m = Mongo()
        assert m.client is None

    def test_mongo_db_is_none_on_init(self) -> None:
        m = Mongo()
        assert m.db is None

    def test_init_app_sets_client(self) -> None:
        m = Mongo()
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            m.init_app(app)

        assert m.client == mock_client

    def test_init_app_sets_db(self) -> None:
        m = Mongo()
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            m.init_app(app)

        assert m.db == mock_client["test_db"]

    def test_init_app_uses_mongo_uri_from_config(self) -> None:
        m = Mongo()
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://user:pass@localhost:27017/mydb"
        app.config["MONGO_DB_NAME"] = "mydb"

        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client_cls.return_value = MagicMock()
            m.init_app(app)

        mock_client_cls.assert_called_once_with("mongodb://user:pass@localhost:27017/mydb")

    def test_init_app_uses_db_name_from_config(self) -> None:
        m = Mongo()
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
        app.config["MONGO_DB_NAME"] = "custom_db"

        with patch("src.configs.mongo_config.MongoClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            m.init_app(app)

        mock_client.__getitem__.assert_called_once_with("custom_db")


class TestMongoSingleton:
    def test_mongo_is_mongo_instance(self) -> None:
        assert isinstance(mongo, Mongo)

    def test_mongo_client_starts_as_none(self) -> None:
        fresh = Mongo()
        assert fresh.client is None

    def test_mongo_db_starts_as_none(self) -> None:
        fresh = Mongo()
        assert fresh.db is None


class TestInitMongo:
    def test_init_mongo_calls_init_app(self) -> None:
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch("src.configs.mongo_config.MongoClient"):
            with patch.object(mongo, "init_app") as mock_init_app:
                init_mongo(app)

        mock_init_app.assert_called_once_with(app)

    def test_init_mongo_passes_app_to_init_app(self) -> None:
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch.object(mongo, "init_app") as mock_init_app:
            init_mongo(app)

        args, _ = mock_init_app.call_args
        assert args[0] is app
