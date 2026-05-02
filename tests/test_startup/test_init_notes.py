from typing import Any
from unittest.mock import patch

import pytest

from src.constants.defaults import DEFAULT_NOTES
from src.models.note_model import NoteModel
from src.startup.init_notes import add_default_notes


class TestAddDefaultNotes:
    @pytest.mark.unit
    def test_does_nothing_when_notes_already_exist(self) -> None:
        existing: list[dict[str, Any]] = [{"_id": "1", "name": "hi"}]
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=existing) as mock_get,
            patch("src.startup.init_notes.NoteService.add_note") as mock_add,
        ):
            add_default_notes()
        mock_get.assert_called_once()
        mock_add.assert_not_called()

    @pytest.mark.unit
    def test_inserts_all_default_notes_when_collection_is_empty(self) -> None:
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[]),
            patch("src.startup.init_notes.NoteService.add_note") as mock_add,
        ):
            add_default_notes()
        assert mock_add.call_count == len(DEFAULT_NOTES)

    @pytest.mark.unit
    def test_inserts_correct_note_names(self) -> None:
        inserted: list[NoteModel] = []
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[]),
            patch("src.startup.init_notes.NoteService.add_note", side_effect=lambda m: inserted.append(m)),
        ):
            add_default_notes()
        inserted_names: list[str] = [m.name for m in inserted]
        expected_names: list[str] = [n["name"] for n in DEFAULT_NOTES]
        assert inserted_names == expected_names

    @pytest.mark.unit
    def test_passes_note_model_instances_to_service(self) -> None:
        inserted: list[Any] = []
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[]),
            patch("src.startup.init_notes.NoteService.add_note", side_effect=lambda m: inserted.append(m)),
        ):
            add_default_notes()
        for item in inserted:
            assert isinstance(item, NoteModel)
