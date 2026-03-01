from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from src.configs.mongo_config import mongo


class TestTemplateBlueprintRegistration:
    def test_blueprint_is_registered(self, app: Flask):
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "template" in blueprint_names

    def test_routes_have_correct_prefix(self, app: Flask):
        rules = [rule.rule for rule in app.url_map.iter_rules()]

        assert any("/api/v1/templates/alive" in rule for rule in rules)
        assert any("/api/v1/templates/test_error" in rule for rule in rules)

    def test_alive_endpoint_exists(self, client: FlaskClient):
        response = client.get("/api/v1/templates/alive")
        assert response.status_code == 200

    def test_test_error_endpoint_exists(self, client: FlaskClient):
        response = client.get("/api/v1/templates/test_error")
        assert response.status_code == 500


class TestAliveEndpoint:
    def test_alive_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data = response.get_json()

        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_alive_returns_correct_values(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data = response.get_json()

        assert data["message"] == "I am Alive!"
        assert data["version_bp"] == "1.0.0"
        assert data["author"] == "Diego Libonati"
        assert data["name_bp"] == "Template"

    def test_alive_returns_json_content_type(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        assert response.content_type == "application/json"


class TestErrorEndpoint:
    def test_test_error_returns_500(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        assert response.status_code == 500

    def test_test_error_returns_error_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        data = response.get_json()

        assert "code" in data
        assert "message" in data

    def test_test_error_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        data = response.get_json()

        assert data["code"] == "CODE_TEMPLATE_ERROR_TEST_MESSAGE"
        assert data["message"] == "TemplateError test message."


class TestNonExistentRoutes:
    def test_non_existent_route_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/nonexistent")
        assert response.status_code == 404

    def test_wrong_method_returns_405(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/templates/alive")
        assert response.status_code == 405


class TestBlueprintWithDatabaseInteraction:
    def test_app_initializes_with_database(self, app: Flask, clean_db: Database) -> None:
        assert mongo.db is not None
        assert mongo.client is not None
