import os

from src.configs.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "templates_db")
    MONGO_URI = os.getenv(
        "MONGO_URI",
        f"mongodb://admin:secret123@host.docker.internal:27017/{MONGO_DB_NAME}?authSource=admin",
    )

    TESTING = True
    DEBUG = True
    ENV = "testing"
