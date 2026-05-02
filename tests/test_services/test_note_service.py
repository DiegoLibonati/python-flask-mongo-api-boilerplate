from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ALREADY_EXISTS_NOTE, CODE_NOT_FOUND_NOTE
from src.models.note_model import NoteModel
from src.services.note_service import NoteService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestAddNote:
    @pytest.mark.unit
    def test_adds_note_when_name_does_not_exist(self) -> None:
        model: NoteModel = NoteModel(name="new_note")
        mock_result: MagicMock = MagicMock(spec=InsertOneResult)
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=None) as mock_find,
            patch("src.services.note_service.NoteDAO.insert_one", return_value=mock_result) as mock_insert,
        ):
            result = NoteService.add_note(model)
        mock_find.assert_called_once_with("new_note")
        mock_insert.assert_called_once_with(model.model_dump())
        assert result == mock_result

    @pytest.mark.unit
    def test_raises_conflict_when_name_already_exists(self) -> None:
        model: NoteModel = NoteModel(name="existing")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "existing"}
        with patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=existing):
            with pytest.raises(ConflictAPIError) as exc_info:
                NoteService.add_note(model)
        assert exc_info.value.code == CODE_ALREADY_EXISTS_NOTE

    @pytest.mark.unit
    def test_conflict_error_has_409_status(self) -> None:
        model: NoteModel = NoteModel(name="existing")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "existing"}
        with patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=existing):
            with pytest.raises(ConflictAPIError) as exc_info:
                NoteService.add_note(model)
        assert exc_info.value.status_code == 409

    @pytest.mark.unit
    def test_does_not_call_insert_when_conflict(self) -> None:
        model: NoteModel = NoteModel(name="dup")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "dup"}
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=existing),
            patch("src.services.note_service.NoteDAO.insert_one") as mock_insert,
        ):
            with pytest.raises(ConflictAPIError):
                NoteService.add_note(model)
        mock_insert.assert_not_called()


class TestGetAllNotes:
    @pytest.mark.unit
    def test_returns_list_from_dao(self) -> None:
        expected: list[dict[str, Any]] = [{"_id": str(ObjectId()), "name": "note"}]
        with patch("src.services.note_service.NoteDAO.find", return_value=expected) as mock_find:
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        mock_find.assert_called_once()
        assert result == expected

    @pytest.mark.unit
    def test_returns_empty_list_when_no_notes(self) -> None:
        with patch("src.services.note_service.NoteDAO.find", return_value=[]):
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        assert result == []

    @pytest.mark.unit
    def test_returns_multiple_notes(self) -> None:
        notes: list[dict[str, Any]] = [
            {"_id": str(ObjectId()), "name": "a"},
            {"_id": str(ObjectId()), "name": "b"},
        ]
        with patch("src.services.note_service.NoteDAO.find", return_value=notes):
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        assert len(result) == 2


class TestDeleteNoteById:
    @pytest.mark.unit
    def test_deletes_note_when_exists(self) -> None:
        _id: ObjectId = ObjectId()
        existing: dict[str, Any] = {"_id": str(_id), "name": "to_delete"}
        mock_result: MagicMock = MagicMock(spec=DeleteResult)
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=existing),
            patch("src.services.note_service.NoteDAO.delete_one_by_id", return_value=mock_result) as mock_delete,
        ):
            result = NoteService.delete_note_by_id(_id)
        mock_delete.assert_called_once_with(_id)
        assert result == mock_result

    @pytest.mark.unit
    def test_raises_not_found_when_note_does_not_exist(self) -> None:
        _id: ObjectId = ObjectId()
        with patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None):
            with pytest.raises(NotFoundAPIError) as exc_info:
                NoteService.delete_note_by_id(_id)
        assert exc_info.value.code == CODE_NOT_FOUND_NOTE

    @pytest.mark.unit
    def test_not_found_error_has_404_status(self) -> None:
        _id: ObjectId = ObjectId()
        with patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None):
            with pytest.raises(NotFoundAPIError) as exc_info:
                NoteService.delete_note_by_id(_id)
        assert exc_info.value.status_code == 404

    @pytest.mark.unit
    def test_does_not_call_delete_when_not_found(self) -> None:
        _id: ObjectId = ObjectId()
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None),
            patch("src.services.note_service.NoteDAO.delete_one_by_id") as mock_delete,
        ):
            with pytest.raises(NotFoundAPIError):
                NoteService.delete_note_by_id(_id)
        mock_delete.assert_not_called()
