import os
import subprocess
import time
from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo import MongoClient
from pymongo.database import Database

from app import create_app
from src.blueprints.routes import register_routes
from src.configs.mongo_config import init_mongo, mongo
from src.utils.exceptions import BaseAPIError

TEST_MONGO_HOST = os.getenv("TEST_MONGO_HOST", "localhost")
TEST_MONGO_PORT = int(os.getenv("TEST_MONGO_PORT", "27018"))
TEST_MONGO_USER = os.getenv("TEST_MONGO_USER", "admin")
TEST_MONGO_PASS = os.getenv("TEST_MONGO_PASS", "secret123")
TEST_MONGO_DB = os.getenv("TEST_MONGO_DB", "test_db")
TEST_MONGO_URI = f"mongodb://{TEST_MONGO_USER}:{TEST_MONGO_PASS}@{TEST_MONGO_HOST}:{TEST_MONGO_PORT}/{TEST_MONGO_DB}?authSource=admin"


def is_mongo_ready(uri: str, timeout: int = 30) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=1000)
            client.admin.command("ping")
            client.close()
            return True
        except Exception:
            time.sleep(1)
    return False


def start_docker_compose() -> None:
    compose_file = os.path.join(os.path.dirname(__file__), "..", "test.docker-compose.yml")

    if not os.path.exists(compose_file):
        raise FileNotFoundError(f"The docker-compose file was not found: {compose_file}")

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "-d", "--wait"],
        check=True,
        capture_output=True,
    )


def stop_docker_compose() -> None:
    compose_file = os.path.join(os.path.dirname(__file__), "..", "test.docker-compose.yml")

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down", "-v"],
        check=False,
        capture_output=True,
    )


def clean_all_collections(db: Database) -> None:
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})


@pytest.fixture(scope="session")
def docker_compose_up() -> Generator[None, None, None]:
    skip_docker = os.getenv("SKIP_DOCKER_COMPOSE", "").lower() in ("true", "1", "yes")

    if not skip_docker:
        try:
            start_docker_compose()
        except subprocess.CalledProcessError:
            raise

    if not is_mongo_ready(TEST_MONGO_URI):
        raise RuntimeError("MongoDB is unavailable after the timeout.")

    yield

    if not skip_docker:
        stop_docker_compose()


@pytest.fixture(scope="session")
def mongo_client(docker_compose_up: Generator[None, None, None]) -> Generator[MongoClient, None, None]:
    client = MongoClient(TEST_MONGO_URI)
    yield client
    client.close()


@pytest.fixture(scope="session")
def mongo_db(mongo_client: MongoClient) -> Database:
    return mongo_client[TEST_MONGO_DB]


@pytest.fixture(scope="function")
def clean_db(mongo_db: Database) -> Generator[Database, None, None]:
    clean_all_collections(mongo_db)

    yield mongo_db

    clean_all_collections(mongo_db)


@pytest.fixture(scope="function")
def app(mongo_db: Database) -> Generator[Flask, None, None]:
    os.environ["MONGO_URI"] = TEST_MONGO_URI
    os.environ["MONGO_DB_NAME"] = TEST_MONGO_DB
    os.environ["MONGO_HOST"] = TEST_MONGO_HOST
    os.environ["MONGO_PORT"] = str(TEST_MONGO_PORT)

    clean_all_collections(mongo_db)

    application = create_app("testing")
    application.config["TESTING"] = True

    mongo.client = MongoClient(TEST_MONGO_URI)
    mongo.db = mongo.client[TEST_MONGO_DB]

    with application.app_context():
        yield application

    clean_all_collections(mongo_db)

    if mongo.client:
        mongo.client.close()


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def app_without_startup(mongo_db: Database) -> Generator[Flask, None, None]:
    os.environ["MONGO_URI"] = TEST_MONGO_URI
    os.environ["MONGO_DB_NAME"] = TEST_MONGO_DB
    os.environ["MONGO_HOST"] = TEST_MONGO_HOST
    os.environ["MONGO_PORT"] = str(TEST_MONGO_PORT)

    clean_all_collections(mongo_db)

    application = Flask(__name__)

    application.config["TESTING"] = True
    application.config["MONGO_URI"] = TEST_MONGO_URI
    application.config["MONGO_DB_NAME"] = TEST_MONGO_DB

    @application.errorhandler(BaseAPIError)
    def handle_api_error(error: BaseAPIError):
        return error.flask_response()

    init_mongo(application)
    register_routes(application)

    with application.app_context():
        yield application

    clean_all_collections(mongo_db)

    if mongo.client:
        mongo.client.close()


@pytest.fixture(scope="function")
def client_without_startup(app_without_startup: Flask) -> FlaskClient:
    return app_without_startup.test_client()


# ============================================================================
# Test data fixtures
# ============================================================================


@pytest.fixture
def sample_template() -> dict[str, str]:
    return {"name": "Test Template"}


@pytest.fixture
def sample_templates() -> list[dict[str, str]]:
    return [
        {"name": "Template 1"},
        {"name": "Template 2"},
        {"name": "Template 3"},
    ]


@pytest.fixture
def inserted_template(app_without_startup: Flask, mongo_db: Database, sample_template: dict[str, str]) -> dict[str, str]:
    result = mongo_db.templates.insert_one(sample_template.copy())
    return {
        **sample_template,
        "_id": str(result.inserted_id),
    }


@pytest.fixture
def inserted_templates(
    app_without_startup: Flask,
    mongo_db: Database,
    sample_templates: list[dict[str, str]],
) -> list[dict[str, str]]:
    inserted = []
    for template in sample_templates:
        result = mongo_db.templates.insert_one(template.copy())
        inserted.append(
            {
                **template,
                "_id": str(result.inserted_id),
            }
        )
    return inserted
