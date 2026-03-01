import os


class DefaultConfig:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")

    # Mongo
    MONGO_HOST = os.getenv("MONGO_HOST", "host.docker.internal")
    MONGO_PORT = os.getenv("MONGO_PORT", 27017)
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASS", "secret123")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "templates_db")
    MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE", "admin")
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource={MONGO_AUTH_SOURCE}"
    JSON_AS_ASCII = False

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 5000)

    # Flask general
    DEBUG = False
    TESTING = False
