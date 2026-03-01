from src.configs.default_config import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    ENV = "development"
