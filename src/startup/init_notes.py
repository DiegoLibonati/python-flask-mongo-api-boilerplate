from src.constants.defaults import DEFAULT_NOTES
from src.models.note_model import NoteModel
from src.services.note_service import NoteService


def add_default_notes() -> None:
    notes = NoteService.get_all_notes()

    if notes:
        return

    for default_note in DEFAULT_NOTES:
        NoteService.add_note(NoteModel(**default_note))
