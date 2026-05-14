from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database

from src.configs.logger_config import setup_logger

logger = setup_logger(__name__)


class Mongo:
    def __init__(self) -> None:
        self.client: MongoClient | None = None
        self._db: Database | None = None

    @property
    def db(self) -> Database:
        if self._db is None:
            raise RuntimeError("MongoDB not initialized. Call init_app() first.")
        return self._db

    def init_app(self, app: Flask) -> None:
        mongo_uri = app.config["MONGO_URI"]
        db_name = app.config["MONGO_DB_NAME"]

        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        self._db = self.client[db_name]

        self.client.admin.command("ping")
        logger.info("MongoDB connection verified.")


mongo = Mongo()


def init_mongo(app: Flask) -> None:
    mongo.init_app(app)
