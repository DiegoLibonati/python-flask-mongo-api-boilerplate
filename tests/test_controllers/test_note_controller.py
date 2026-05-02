from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId
from flask import Flask
from pymongo.results import InsertOneResult

from src.constants.codes import CODE_SUCCESS_ADD_NOTE, CODE_SUCCESS_DELETE_NOTE, CODE_SUCCESS_GET_NOTES
from src.constants.messages import MESSAGE_SUCCESS_ADD_NOTE, MESSAGE_SUCCESS_DELETE_NOTE, MESSAGE_SUCCESS_GET_NOTES
from src.controllers.note_controller import alive, create_note, delete_note, get_notes
from src.controllers.note_controller import test_error as controller_test_error
from src.utils.exceptions import ConflictAPIError, InternalAPIError, NotFoundAPIError, ValidationAPIError


class TestAliveController:
    @pytest.mark.unit
    def test_returns_tuple_with_200_status(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
        assert status == 200

    @pytest.mark.unit
    def test_response_json_has_message(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    @pytest.mark.unit
    def test_response_json_has_version_bp(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["version_bp"] == "1.0.0"

    @pytest.mark.unit
    def test_response_json_has_author(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["author"] == "Diego Libonati"

    @pytest.mark.unit
    def test_response_json_has_name_bp(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["name_bp"] == "Note"


class TestTestErrorController:
    @pytest.mark.unit
    def test_raises_internal_api_error(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError):
                controller_test_error()

    @pytest.mark.unit
    def test_error_has_correct_code(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.code == "CODE_NOTE_ERROR_TEST_MESSAGE"

    @pytest.mark.unit
    def test_error_has_correct_message(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.message == "NoteError test message."

    @pytest.mark.unit
    def test_error_has_500_status_code(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.status_code == 500


class TestCreateNoteController:
    @pytest.mark.unit
    def test_returns_201_when_created(self, app: Flask) -> None:
        mock_result: MagicMock = MagicMock(spec=InsertOneResult, inserted_id=ObjectId())
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": "test_note"}):
            with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_result):
                response, status = create_note()
        assert status == 201

    @pytest.mark.unit
    def test_response_contains_message(self, app: Flask) -> None:
        mock_result: MagicMock = MagicMock(spec=InsertOneResult, inserted_id=ObjectId())
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": "test_note"}):
            with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_result):
                response, status = create_note()
                data: dict[str, Any] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_ADD_NOTE

    @pytest.mark.unit
    def test_response_contains_code(self, app: Flask) -> None:
        mock_result: MagicMock = MagicMock(spec=InsertOneResult, inserted_id=ObjectId())
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": "test_note"}):
            with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_result):
                response, status = create_note()
                data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_ADD_NOTE

    @pytest.mark.unit
    def test_response_data_contains_inserted_id(self, app: Flask) -> None:
        _id: ObjectId = ObjectId()
        mock_result: MagicMock = MagicMock(spec=InsertOneResult, inserted_id=_id)
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": "test_note"}):
            with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_result):
                response, status = create_note()
                data: dict[str, Any] = response.get_json()
        assert data["data"] == str(_id)

    @pytest.mark.unit
    def test_raises_conflict_when_name_already_exists(self, app: Flask) -> None:
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": "existing"}):
            with patch(
                "src.controllers.note_controller.NoteService.add_note",
                side_effect=ConflictAPIError(code="ALREADY_EXISTS_NOTE", message="Note already exists."),
            ):
                with pytest.raises(ConflictAPIError):
                    create_note()

    @pytest.mark.unit
    def test_raises_validation_error_for_empty_name(self, app: Flask) -> None:
        with app.test_request_context("/api/v1/notes/", method="POST", json={"name": ""}):
            with pytest.raises(ValidationAPIError):
                create_note()


class TestGetNotesController:
    @pytest.mark.unit
    def test_returns_200(self, app: Flask) -> None:
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
                response, status = get_notes()
        assert status == 200

    @pytest.mark.unit
    def test_response_contains_code(self, app: Flask) -> None:
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
                response, status = get_notes()
                data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_GET_NOTES

    @pytest.mark.unit
    def test_response_contains_message(self, app: Flask) -> None:
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
                response, status = get_notes()
                data: dict[str, Any] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_GET_NOTES

    @pytest.mark.unit
    def test_response_data_is_list(self, app: Flask) -> None:
        notes: list[dict[str, Any]] = [{"_id": str(ObjectId()), "name": "a"}]
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=notes):
                response, status = get_notes()
                data: dict[str, Any] = response.get_json()
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 1

    @pytest.mark.unit
    def test_response_data_is_empty_when_no_notes(self, app: Flask) -> None:
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
                response, status = get_notes()
                data: dict[str, Any] = response.get_json()
        assert data["data"] == []

    @pytest.mark.unit
    def test_service_is_called_once(self, app: Flask) -> None:
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]) as mock_get:
                get_notes()
        mock_get.assert_called_once()


class TestDeleteNoteController:
    @pytest.mark.unit
    def test_returns_200_when_deleted(self, app: Flask) -> None:
        _id: str = str(ObjectId())
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.delete_note_by_id"):
                response, status = delete_note(id=_id)
        assert status == 200

    @pytest.mark.unit
    def test_response_contains_message(self, app: Flask) -> None:
        _id: str = str(ObjectId())
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.delete_note_by_id"):
                response, status = delete_note(id=_id)
                data: dict[str, Any] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_DELETE_NOTE

    @pytest.mark.unit
    def test_response_contains_code(self, app: Flask) -> None:
        _id: str = str(ObjectId())
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.delete_note_by_id"):
                response, status = delete_note(id=_id)
                data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_DELETE_NOTE

    @pytest.mark.unit
    def test_raises_validation_error_for_invalid_id(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValidationAPIError) as exc_info:
                delete_note(id="not_a_valid_id")
        assert exc_info.value.status_code == 400

    @pytest.mark.unit
    def test_raises_not_found_when_note_does_not_exist(self, app: Flask) -> None:
        _id: str = str(ObjectId())
        with app.app_context():
            with patch(
                "src.controllers.note_controller.NoteService.delete_note_by_id",
                side_effect=NotFoundAPIError(code="NOT_FOUND_NOTE", message="No note found."),
            ):
                with pytest.raises(NotFoundAPIError):
                    delete_note(id=_id)

    @pytest.mark.unit
    def test_service_called_with_objectid(self, app: Flask) -> None:
        _id: ObjectId = ObjectId()
        with app.app_context():
            with patch("src.controllers.note_controller.NoteService.delete_note_by_id") as mock_delete:
                delete_note(id=str(_id))
        mock_delete.assert_called_once_with(_id)
