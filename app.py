import importlib

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from werkzeug.exceptions import HTTPException

from src.blueprints.routes import register_routes
from src.configs.logger_config import setup_logger
from src.configs.mongo_config import init_mongo
from src.constants.codes import CODE_ERROR_INTERNAL_SERVER, CODE_NOT_FOUND_ROUTE
from src.constants.messages import MESSAGE_ERROR_INTERNAL_SERVER, MESSAGE_NOT_FOUND_ROUTE
from src.startup.init_notes import add_default_notes
from src.utils.exceptions import BaseAPIError

logger = setup_logger()

ALLOWED_CONFIGS = {"development", "production", "testing"}


def create_app(config_name="development") -> Flask:
    if config_name not in ALLOWED_CONFIGS:
        raise ValueError(f"Invalid config_name: {config_name!r}. Allowed values are: {sorted(ALLOWED_CONFIGS)}")

    app = Flask(__name__)
    if isinstance(app.json, DefaultJSONProvider):
        app.json.ensure_ascii = False

    config_module = importlib.import_module(f"src.configs.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    @app.errorhandler(BaseAPIError)
    def handle_api_error(error: BaseAPIError):
        return error.flask_response()

    @app.errorhandler(404)
    def handle_not_found(error):
        logger.warning("404 Not Found: %s", error)
        return jsonify(
            {
                "code": CODE_NOT_FOUND_ROUTE,
                "message": MESSAGE_NOT_FOUND_ROUTE,
            }
        ), 404

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error: Exception):
        if isinstance(error, HTTPException):
            return error
        logger.exception("Unhandled exception: %s", error)
        return jsonify(
            {
                "code": CODE_ERROR_INTERNAL_SERVER,
                "message": MESSAGE_ERROR_INTERNAL_SERVER,
            }
        ), 500

    init_mongo(app)
    logger.info("MongoDB initialized successfully.")

    register_routes(app)
    logger.info("Routes initialized successfully.")

    if app.config.get("SEED_DEFAULT_DATA", False):
        add_default_notes()
        logger.info("Default notes initialized successfully.")

    return app


if __name__ == "__main__":
    app = create_app("development")

    logger.info("Starting Flask application.")
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
