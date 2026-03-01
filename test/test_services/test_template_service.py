import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import (
    CODE_ERROR_TEMPLATE_ALREADY_EXISTS,
    CODE_NOT_FOUND_TEMPLATE,
)
from src.models.template_model import TemplateModel
from src.services.template_service import TemplateService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestTemplateServiceAddTemplate:
    def test_add_template_inserts_document(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = TemplateModel(name="New Template")
        result = TemplateService.add_template(template)

        assert result.inserted_id is not None

        doc = mongo_db.templates.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == "New Template"

    def test_add_template_raises_conflict_for_duplicate(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = TemplateModel(name="Duplicate Template")
        TemplateService.add_template(template)

        with pytest.raises(ConflictAPIError) as exc_info:
            TemplateService.add_template(template)

        assert exc_info.value.status_code == 409

    def test_add_template_duplicate_is_case_insensitive(self, app_without_startup: Flask, mongo_db: Database) -> None:
        TemplateService.add_template(TemplateModel(name="MyTemplate"))

        with pytest.raises(ConflictAPIError):
            TemplateService.add_template(TemplateModel(name="mytemplate"))

        with pytest.raises(ConflictAPIError):
            TemplateService.add_template(TemplateModel(name="MYTEMPLATE"))

    def test_add_template_returns_insert_result(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = TemplateModel(name="Another Template")
        result = TemplateService.add_template(template)

        assert isinstance(result, InsertOneResult)


class TestTemplateServiceGetAllTemplates:
    def test_get_all_templates_returns_empty_list(self, app_without_startup: Flask, mongo_db: Database) -> None:
        result = TemplateService.get_all_templates()

        assert result == []

    def test_get_all_templates_returns_all(self, inserted_templates: list[dict[str, str]]) -> None:
        result = TemplateService.get_all_templates()

        assert len(result) == len(inserted_templates)

    def test_get_all_templates_returns_parsed_documents(self, inserted_template: dict[str, str]) -> None:
        result = TemplateService.get_all_templates()

        assert len(result) == 1
        assert isinstance(result[0]["_id"], str)


class TestTemplateServiceDeleteTemplate:
    def test_delete_template_removes_document(self, inserted_template: dict[str, str], mongo_db: Database) -> None:
        assert mongo_db.templates.count_documents({}) == 1

        result = TemplateService.delete_template_by_id(inserted_template["_id"])

        assert result.deleted_count == 1
        assert mongo_db.templates.count_documents({}) == 0

    def test_delete_template_raises_not_found(self, app_without_startup: Flask, mongo_db: Database) -> None:
        fake_id = str(ObjectId())

        with pytest.raises(NotFoundAPIError) as exc_info:
            TemplateService.delete_template_by_id(fake_id)

        assert exc_info.value.status_code == 404

    def test_delete_template_returns_delete_result(self, inserted_template: dict[str, str]) -> None:
        result = TemplateService.delete_template_by_id(inserted_template["_id"])

        assert isinstance(result, DeleteResult)

    def test_delete_template_only_removes_one(self, inserted_templates: list[dict[str, str]], mongo_db: Database) -> None:
        initial_count = mongo_db.templates.count_documents({})

        TemplateService.delete_template_by_id(inserted_templates[0]["_id"])

        final_count = mongo_db.templates.count_documents({})
        assert final_count == initial_count - 1


class TestTemplateServiceErrorCodes:
    def test_conflict_error_has_correct_code(self, inserted_template: dict[str, str]) -> None:
        with pytest.raises(ConflictAPIError) as exc_info:
            TemplateService.add_template(TemplateModel(name=inserted_template["name"]))

        assert exc_info.value.code == CODE_ERROR_TEMPLATE_ALREADY_EXISTS

    def test_not_found_error_has_correct_code(self, app_without_startup: Flask, mongo_db: Database) -> None:
        with pytest.raises(NotFoundAPIError) as exc_info:
            TemplateService.delete_template_by_id(str(ObjectId()))

        assert exc_info.value.code == CODE_NOT_FOUND_TEMPLATE


class TestTemplateServiceIntegration:
    def test_full_crud_cycle(self, app_without_startup: Flask, mongo_db: Database) -> None:
        template = TemplateModel(name="CRUD Template")
        create_result = TemplateService.add_template(template)
        template_id = str(create_result.inserted_id)

        templates = TemplateService.get_all_templates()
        assert len(templates) == 1
        assert templates[0]["_id"] == template_id

        delete_result = TemplateService.delete_template_by_id(template_id)
        assert delete_result.deleted_count == 1

        templates = TemplateService.get_all_templates()
        assert len(templates) == 0

    def test_multiple_templates_management(self, app_without_startup: Flask, mongo_db: Database) -> None:
        names = ["Template A", "Template B", "Template C"]
        ids = []

        for name in names:
            result = TemplateService.add_template(TemplateModel(name=name))
            ids.append(str(result.inserted_id))

        templates = TemplateService.get_all_templates()
        assert len(templates) == 3

        TemplateService.delete_template_by_id(ids[1])

        templates = TemplateService.get_all_templates()
        assert len(templates) == 2
        assert all(t["name"] != "Template B" for t in templates)
