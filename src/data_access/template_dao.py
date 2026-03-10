from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.configs.mongo_config import mongo


class TemplateDAO:
    @staticmethod
    def insert_one(template: dict[str, Any]) -> InsertOneResult:
        return mongo.db.templates.insert_one(template)

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return TemplateDAO.parse_templates(list(mongo.db.templates.find()))

    @staticmethod
    def find_one_by_id(_id: ObjectId) -> dict[str, Any] | None:
        return TemplateDAO.parse_template(mongo.db.templates.find_one({"_id": ObjectId(_id)}))

    @staticmethod
    def find_one_by_name(name: str) -> dict[str, Any] | None:
        return TemplateDAO.parse_template(mongo.db.templates.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}}))

    @staticmethod
    def delete_one_by_id(_id: ObjectId) -> DeleteResult:
        return mongo.db.templates.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def parse_templates(templates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [TemplateDAO.parse_template(template) for template in templates]

    @staticmethod
    def parse_template(template: dict[str, Any]) -> dict[str, Any]:
        if not template:
            return None

        return {
            **{k: v for k, v in template.items() if k != "_id"},
            "_id": str(template["_id"]),
        }
