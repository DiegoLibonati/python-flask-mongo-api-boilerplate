from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import (
    CODE_ERROR_TEMPLATE_ALREADY_EXISTS,
    CODE_NOT_FOUND_TEMPLATE,
)
from src.constants.messages import (
    MESSAGE_ERROR_TEMPLATE_ALREADY_EXISTS,
    MESSAGE_NOT_FOUND_TEMPLATE,
)
from src.data_access.template_dao import TemplateDAO
from src.models.template_model import TemplateModel
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TemplateService:
    @staticmethod
    def add_template(template: TemplateModel) -> InsertOneResult:
        existing = TemplateDAO.find_one_by_name(template.name)
        if existing:
            raise ConflictAPIError(
                code=CODE_ERROR_TEMPLATE_ALREADY_EXISTS,
                message=MESSAGE_ERROR_TEMPLATE_ALREADY_EXISTS,
            )
        return TemplateDAO.insert_one(template.model_dump())

    @staticmethod
    def get_all_templates() -> list[dict[str, Any]]:
        return TemplateDAO.find()

    @staticmethod
    def delete_template_by_id(_id: ObjectId) -> DeleteResult:
        existing = TemplateDAO.find_one_by_id(_id)

        if not existing:
            raise NotFoundAPIError(code=CODE_NOT_FOUND_TEMPLATE, message=MESSAGE_NOT_FOUND_TEMPLATE)

        return TemplateDAO.delete_one_by_id(_id)
