from src.configs.default_config import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    ENV = "production"
