import os

from src.configs.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "boilerplate_db")
    MONGO_URI = os.environ["MONGO_URI"]

    TESTING = True
    DEBUG = True
    ENV = "testing"
