from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import (
    CODE_ALREADY_EXISTS_NOTE,
    CODE_NOT_FOUND_NOTE,
)
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_NOTE,
    MESSAGE_NOT_FOUND_NOTE,
)
from src.data_access.note_dao import NoteDAO
from src.models.note_model import NoteModel
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class NoteService:
    @staticmethod
    def add_note(note: NoteModel) -> InsertOneResult:
        existing = NoteDAO.find_one_by_name(note.name)
        if existing:
            raise ConflictAPIError(
                code=CODE_ALREADY_EXISTS_NOTE,
                message=MESSAGE_ALREADY_EXISTS_NOTE,
            )
        return NoteDAO.insert_one(note.model_dump())

    @staticmethod
    def get_all_notes() -> list[dict[str, Any]]:
        return NoteDAO.find()

    @staticmethod
    def delete_note_by_id(_id: ObjectId) -> DeleteResult:
        existing = NoteDAO.find_one_by_id(_id)

        if not existing:
            raise NotFoundAPIError(code=CODE_NOT_FOUND_NOTE, message=MESSAGE_NOT_FOUND_NOTE)

        return NoteDAO.delete_one_by_id(_id)
