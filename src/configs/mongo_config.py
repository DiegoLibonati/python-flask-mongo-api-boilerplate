from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database


class Mongo:
    def __init__(self):
        self.client: MongoClient | None = None
        self.db: Database | None = None

    def init_app(self, app: Flask) -> None:
        mongo_uri = app.config["MONGO_URI"]
        db_name = app.config["MONGO_DB_NAME"]

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]


mongo = Mongo()


def init_mongo(app: Flask) -> None:
    mongo.init_app(app)
