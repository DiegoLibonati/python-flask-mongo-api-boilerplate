import pytest
from flask import Flask

from src.blueprints.routes import register_routes


@pytest.fixture(scope="module")
def bare_app() -> Flask:
    app = Flask(__name__)
    register_routes(app)
    return app


class TestRegisterRoutes:
    @pytest.mark.unit
    def test_health_prefix_is_registered(self, bare_app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in bare_app.url_map.iter_rules()]

        assert any("/api/v1/health" in rule for rule in rules)

    @pytest.mark.unit
    def test_notes_prefix_is_registered(self, bare_app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in bare_app.url_map.iter_rules()]

        assert any("/api/v1/notes" in rule for rule in rules)

    @pytest.mark.unit
    def test_get_method_available_on_health_route(self, bare_app: Flask) -> None:
        health_rules = [rule for rule in bare_app.url_map.iter_rules() if "/api/v1/health" in str(rule)]

        assert any("GET" in rule.methods for rule in health_rules)

    @pytest.mark.unit
    def test_post_method_available_on_notes_route(self, bare_app: Flask) -> None:
        note_rules = [rule for rule in bare_app.url_map.iter_rules() if "/api/v1/notes" in str(rule)]

        assert any("POST" in rule.methods for rule in note_rules)
