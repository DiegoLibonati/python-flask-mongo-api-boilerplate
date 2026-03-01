from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.template_dao import TemplateDAO


class TestTemplateDAOInsert:
    def test_insert_one_creates_document(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = {"name": "Test Template"}
        result = TemplateDAO.insert_one(template)

        assert result.inserted_id is not None

        doc = mongo_db.templates.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == "Test Template"

    def test_insert_one_returns_insert_result(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = {"name": "Another Template"}
        result = TemplateDAO.insert_one(template)

        assert isinstance(result, InsertOneResult)
        assert result.acknowledged is True

    def test_insert_multiple_documents(self, app_without_startup: Flask, mongo_db: Database) -> None:
        templates = [
            {"name": "Template 1"},
            {"name": "Template 2"},
            {"name": "Template 3"},
        ]

        for template in templates:
            TemplateDAO.insert_one(template)

        count = mongo_db.templates.count_documents({})
        assert count == 3


class TestTemplateDAOFind:
    def test_find_returns_empty_list_when_no_documents(self, app_without_startup: Flask, mongo_db: Database) -> None:
        result = TemplateDAO.find()
        assert result == []

    def test_find_returns_all_documents(self, inserted_templates: list[dict[str, str]]) -> None:
        result = TemplateDAO.find()

        assert len(result) == len(inserted_templates)

    def test_find_returns_parsed_documents(self, inserted_template: dict[str, str]) -> None:
        result = TemplateDAO.find()

        assert len(result) == 1
        assert isinstance(result[0]["_id"], str)
        assert result[0]["name"] == inserted_template["name"]


class TestTemplateDAOFindOneById:
    def test_find_one_by_id_returns_document(self, inserted_template: dict[str, str]) -> None:
        result = TemplateDAO.find_one_by_id(inserted_template["_id"])

        assert result is not None
        assert result["_id"] == inserted_template["_id"]
        assert result["name"] == inserted_template["name"]

    def test_find_one_by_id_returns_none_for_nonexistent(self, app_without_startup: Flask, mongo_db: Database) -> None:
        fake_id = str(ObjectId())
        result = TemplateDAO.find_one_by_id(fake_id)

        assert result is None

    def test_find_one_by_id_accepts_string_id(self, inserted_template: dict[str, str]) -> None:
        result = TemplateDAO.find_one_by_id(inserted_template["_id"])

        assert result is not None


class TestTemplateDAOFindOneByName:
    def test_find_one_by_name_returns_document(self, inserted_template: dict[str, str]) -> None:
        result = TemplateDAO.find_one_by_name(inserted_template["name"])

        assert result is not None
        assert result["name"] == inserted_template["name"]

    def test_find_one_by_name_is_case_insensitive(self, app_without_startup: Flask, mongo_db: Database) -> None:
        mongo_db.templates.insert_one({"name": "MyTemplate"})

        result_lower = TemplateDAO.find_one_by_name("mytemplate")
        result_upper = TemplateDAO.find_one_by_name("MYTEMPLATE")
        result_mixed = TemplateDAO.find_one_by_name("MyTemplate")

        assert result_lower is not None
        assert result_upper is not None
        assert result_mixed is not None
        assert result_lower["name"] == result_upper["name"] == result_mixed["name"]

    def test_find_one_by_name_returns_none_for_nonexistent(self, app_without_startup: Flask, mongo_db: Database) -> None:
        result = TemplateDAO.find_one_by_name("NonExistentTemplate")

        assert result is None

    def test_find_one_by_name_exact_match(self, app_without_startup: Flask, mongo_db: Database) -> None:
        mongo_db.templates.insert_one({"name": "Template"})

        result_partial = TemplateDAO.find_one_by_name("Temp")
        result_extended = TemplateDAO.find_one_by_name("Template Extra")

        assert result_partial is None
        assert result_extended is None


class TestTemplateDAODelete:
    def test_delete_one_by_id_removes_document(self, inserted_template: dict[str, str], mongo_db: Database) -> None:
        assert mongo_db.templates.count_documents({}) == 1

        result = TemplateDAO.delete_one_by_id(inserted_template["_id"])

        assert result.deleted_count == 1
        assert mongo_db.templates.count_documents({}) == 0

    def test_delete_one_by_id_returns_delete_result(self, inserted_template: dict[str, str]) -> None:
        result = TemplateDAO.delete_one_by_id(inserted_template["_id"])

        assert isinstance(result, DeleteResult)
        assert result.acknowledged is True

    def test_delete_one_by_id_nonexistent_returns_zero(self, app_without_startup: Flask, mongo_db: Database) -> None:
        fake_id = str(ObjectId())
        result = TemplateDAO.delete_one_by_id(fake_id)

        assert result.deleted_count == 0


class TestTemplateDAOParsing:
    def test_parse_template_converts_id_to_string(self, app_without_startup: Flask) -> None:
        doc = {"_id": ObjectId(), "name": "Test"}
        result = TemplateDAO.parse_template(doc)

        assert isinstance(result["_id"], str)

    def test_parse_template_preserves_other_fields(self, app_without_startup: Flask) -> None:
        doc = {"_id": ObjectId(), "name": "Test", "extra": "value"}
        result = TemplateDAO.parse_template(doc)

        assert result["name"] == "Test"
        assert result["extra"] == "value"

    def test_parse_template_returns_none_for_none(self, app_without_startup: Flask) -> None:
        result = TemplateDAO.parse_template(None)

        assert result is None

    def test_parse_templates_handles_list(self, app_without_startup: Flask) -> None:
        docs = [
            {"_id": ObjectId(), "name": "Test1"},
            {"_id": ObjectId(), "name": "Test2"},
        ]
        result = TemplateDAO.parse_templates(docs)

        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_parse_templates_handles_empty_list(self, app_without_startup: Flask) -> None:
        result = TemplateDAO.parse_templates([])

        assert result == []
