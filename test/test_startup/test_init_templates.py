import os
from collections.abc import Generator

from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database

from app import create_app
from src.configs.mongo_config import mongo
from src.constants.defaults import DEFAULT_TEMPLATES
from src.models.template_model import TemplateModel
from src.services.template_service import TemplateService
from src.startup.init_templates import add_default_templates
from test.conftest import (
    TEST_MONGO_DB,
    TEST_MONGO_HOST,
    TEST_MONGO_PORT,
    TEST_MONGO_URI,
)


class TestAddDefaultTemplates:
    def test_adds_default_templates_when_empty(self, app_without_startup: Generator[Flask, None, None], clean_db: Database) -> None:
        assert clean_db.templates.count_documents({}) == 0

        add_default_templates()

        count = clean_db.templates.count_documents({})
        assert count == len(DEFAULT_TEMPLATES)

    def test_does_not_add_if_templates_exist(self, app_without_startup: Generator[Flask, None, None], clean_db: Database) -> None:
        clean_db.templates.insert_one({"name": "Existing Template"})

        add_default_templates()

        count = clean_db.templates.count_documents({})
        assert count == 1

    def test_is_idempotent(self, app_without_startup: Generator[Flask, None, None], clean_db: Database) -> None:
        add_default_templates()
        add_default_templates()
        add_default_templates()

        count = clean_db.templates.count_documents({})
        assert count == len(DEFAULT_TEMPLATES)

    def test_creates_correct_templates(self, app_without_startup: Generator[Flask, None, None], clean_db: Database) -> None:
        add_default_templates()

        for default in DEFAULT_TEMPLATES:
            doc = clean_db.templates.find_one({"name": default["name"]})
            assert doc is not None


class TestDefaultTemplatesConstants:
    def test_default_templates_is_list(self) -> None:
        assert isinstance(DEFAULT_TEMPLATES, list)

    def test_default_templates_have_name_field(self) -> None:
        for template in DEFAULT_TEMPLATES:
            assert "name" in template
            assert isinstance(template["name"], str)
            assert len(template["name"]) > 0

    def test_default_templates_are_valid_models(self) -> None:
        for template in DEFAULT_TEMPLATES:
            model = TemplateModel(**template)
            assert model.name == template["name"]


class TestStartupIntegration:
    def test_app_creation_runs_startup(self, clean_db: Database) -> None:
        os.environ["MONGO_URI"] = TEST_MONGO_URI
        os.environ["MONGO_DB_NAME"] = TEST_MONGO_DB
        os.environ["MONGO_HOST"] = TEST_MONGO_HOST
        os.environ["MONGO_PORT"] = str(TEST_MONGO_PORT)

        app = create_app("testing")

        mongo.client = MongoClient(TEST_MONGO_URI)
        mongo.db = mongo.client[TEST_MONGO_DB]

        with app.app_context():
            count = mongo.db.templates.count_documents({})
            assert count == len(DEFAULT_TEMPLATES)

        mongo.client.close()

    def test_startup_uses_template_service(self, app_without_startup: Generator[Flask, None, None], clean_db: Database) -> None:
        add_default_templates()

        templates = TemplateService.get_all_templates()
        assert len(templates) == len(DEFAULT_TEMPLATES)
