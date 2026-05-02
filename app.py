import importlib

from flask import Flask

from src.blueprints.routes import register_routes
from src.configs.logger_config import setup_logger
from src.configs.mongo_config import init_mongo
from src.startup.init_notes import add_default_notes
from src.utils.exceptions import BaseAPIError

logger = setup_logger()


def create_app(config_name="development") -> None:
    app = Flask(__name__)

    config_module = importlib.import_module(f"src.configs.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    @app.errorhandler(BaseAPIError)
    def handle_api_error(error: BaseAPIError):
        return error.flask_response()

    init_mongo(app)
    logger.info("MongoDB initialized successfully.")

    register_routes(app)
    logger.info("Routes initialized successfully.")

    add_default_notes()
    logger.info("Default notes initialized successfully.")

    return app


if __name__ == "__main__":
    app = create_app("development")

    logger.info("Starting Flask application.")
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
