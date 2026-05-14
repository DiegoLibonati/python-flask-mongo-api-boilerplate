from bson import ObjectId
from flask import jsonify, request
from flask.typing import ResponseReturnValue

from src.constants.codes import (
    CODE_NOT_VALID_OBJECT_ID,
    CODE_SUCCESS_ADD_NOTE,
    CODE_SUCCESS_DELETE_NOTE,
    CODE_SUCCESS_GET_NOTES,
)
from src.constants.messages import (
    MESSAGE_NOT_VALID_OBJECT_ID,
    MESSAGE_SUCCESS_ADD_NOTE,
    MESSAGE_SUCCESS_DELETE_NOTE,
    MESSAGE_SUCCESS_GET_NOTES,
)
from src.models.note_model import NoteModel
from src.services.note_service import NoteService
from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_decorator import exceptions_decorator


@exceptions_decorator
def alive() -> ResponseReturnValue:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "author": "Diego Libonati",
        "name_bp": "Note",
    }

    return jsonify(response), 200


@exceptions_decorator
def test_error() -> ResponseReturnValue:
    message = "NoteError test message."
    code = "CODE_NOTE_ERROR_TEST_MESSAGE"

    raise InternalAPIError(code=code, message=message)


@exceptions_decorator
def create_note() -> ResponseReturnValue:
    data = request.get_json()
    note = NoteModel(**data)
    result = NoteService.add_note(note)
    return jsonify(
        {
            "message": MESSAGE_SUCCESS_ADD_NOTE,
            "code": CODE_SUCCESS_ADD_NOTE,
            "data": str(result.inserted_id),
        }
    ), 201


@exceptions_decorator
def get_notes() -> ResponseReturnValue:
    notes = NoteService.get_all_notes()
    return jsonify({"code": CODE_SUCCESS_GET_NOTES, "message": MESSAGE_SUCCESS_GET_NOTES, "data": notes}), 200


@exceptions_decorator
def delete_note(id: str) -> ResponseReturnValue:
    try:
        _id = ObjectId(id)
    except Exception:
        raise ValidationAPIError(
            code=CODE_NOT_VALID_OBJECT_ID,
            message=MESSAGE_NOT_VALID_OBJECT_ID,
        ) from None

    NoteService.delete_note_by_id(_id)
    return jsonify(
        {
            "message": MESSAGE_SUCCESS_DELETE_NOTE,
            "code": CODE_SUCCESS_DELETE_NOTE,
        }
    ), 200
