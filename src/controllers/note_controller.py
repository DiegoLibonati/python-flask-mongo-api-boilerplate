from bson import ObjectId
from flask import Response, jsonify, request

from src.constants.codes import CODE_NOT_VALID_OBJECT_ID, CODE_SUCCESS_ADD_NOTE, CODE_SUCCESS_DELETE_NOTE, CODE_SUCCESS_GET_NOTES
from src.constants.messages import MESSAGE_NOT_VALID_OBJECT_ID, MESSAGE_SUCCESS_ADD_NOTE, MESSAGE_SUCCESS_DELETE_NOTE, MESSAGE_SUCCESS_GET_NOTES
from src.models.note_model import NoteModel
from src.services.note_service import NoteService
from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


@exceptions_handler
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "author": "Diego Libonati",
        "name_bp": "Note",
    }

    return jsonify(response), 200


@exceptions_handler
def test_error() -> Response:
    message = "NoteError test message."
    code = "CODE_NOTE_ERROR_TEST_MESSAGE"

    raise InternalAPIError(code=code, message=message)


@exceptions_handler
def create_note() -> Response:
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


@exceptions_handler
def get_notes() -> Response:
    notes = NoteService.get_all_notes()
    return jsonify({"code": CODE_SUCCESS_GET_NOTES, "message": MESSAGE_SUCCESS_GET_NOTES, "data": notes}), 200


@exceptions_handler
def delete_note(id: str) -> Response:
    try:
        _id = ObjectId(id)
    except Exception:
        raise ValidationAPIError(
            code=CODE_NOT_VALID_OBJECT_ID,
            message=MESSAGE_NOT_VALID_OBJECT_ID,
        )

    NoteService.delete_note_by_id(_id)
    return jsonify(
        {
            "message": MESSAGE_SUCCESS_DELETE_NOTE,
            "code": CODE_SUCCESS_DELETE_NOTE,
        }
    ), 200
