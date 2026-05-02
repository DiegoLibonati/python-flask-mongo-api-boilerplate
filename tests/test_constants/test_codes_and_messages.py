import pytest

from src.constants.codes import (
    CODE_ALREADY_EXISTS_NOTE,
    CODE_ERROR_AUTHENTICATION,
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_INTERNAL_SERVER,
    CODE_ERROR_PYDANTIC,
    CODE_NOT_FOUND_NOTE,
    CODE_NOT_VALID_INTEGER,
    CODE_NOT_VALID_OBJECT_ID,
    CODE_SUCCESS_ADD_NOTE,
    CODE_SUCCESS_DELETE_NOTE,
    CODE_SUCCESS_GET_NOTES,
)
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_NOTE,
    MESSAGE_ERROR_AUTHENTICATION,
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_INTERNAL_SERVER,
    MESSAGE_ERROR_PYDANTIC,
    MESSAGE_NOT_FOUND_NOTE,
    MESSAGE_NOT_VALID_INTEGER,
    MESSAGE_NOT_VALID_OBJECT_ID,
    MESSAGE_SUCCESS_ADD_NOTE,
    MESSAGE_SUCCESS_DELETE_NOTE,
    MESSAGE_SUCCESS_GET_NOTES,
)


class TestCodes:
    @pytest.mark.unit
    def test_code_success_add_note(self) -> None:
        assert CODE_SUCCESS_ADD_NOTE == "SUCCESS_ADD_NOTE"

    @pytest.mark.unit
    def test_code_success_get_notes(self) -> None:
        assert CODE_SUCCESS_GET_NOTES == "SUCCESS_GET_NOTES"

    @pytest.mark.unit
    def test_code_success_delete_note(self) -> None:
        assert CODE_SUCCESS_DELETE_NOTE == "SUCCESS_DELETE_NOTE"

    @pytest.mark.unit
    def test_code_error_internal_server(self) -> None:
        assert CODE_ERROR_INTERNAL_SERVER == "ERROR_INTERNAL_SERVER"

    @pytest.mark.unit
    def test_code_error_pydantic(self) -> None:
        assert CODE_ERROR_PYDANTIC == "ERROR_PYDANTIC"

    @pytest.mark.unit
    def test_code_error_database(self) -> None:
        assert CODE_ERROR_DATABASE == "ERROR_DATABASE"

    @pytest.mark.unit
    def test_code_not_valid_object_id(self) -> None:
        assert CODE_NOT_VALID_OBJECT_ID == "NOT_VALID_OBJECT_ID"

    @pytest.mark.unit
    def test_code_already_exists_note(self) -> None:
        assert CODE_ALREADY_EXISTS_NOTE == "ALREADY_EXISTS_NOTE"

    @pytest.mark.unit
    def test_code_not_found_note(self) -> None:
        assert CODE_NOT_FOUND_NOTE == "NOT_FOUND_NOTE"

    @pytest.mark.unit
    def test_all_codes_are_non_empty_strings(self) -> None:
        codes: list[str] = [
            CODE_SUCCESS_ADD_NOTE,
            CODE_SUCCESS_GET_NOTES,
            CODE_SUCCESS_DELETE_NOTE,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_DATABASE,
            CODE_ERROR_GENERIC,
            CODE_ERROR_AUTHENTICATION,
            CODE_NOT_VALID_INTEGER,
            CODE_NOT_VALID_OBJECT_ID,
            CODE_ALREADY_EXISTS_NOTE,
            CODE_NOT_FOUND_NOTE,
        ]
        for code in codes:
            assert isinstance(code, str)
            assert len(code) > 0


class TestMessages:
    @pytest.mark.unit
    def test_message_success_add_note_is_non_empty(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_ADD_NOTE, str)
        assert len(MESSAGE_SUCCESS_ADD_NOTE) > 0

    @pytest.mark.unit
    def test_message_success_get_notes(self) -> None:
        assert MESSAGE_SUCCESS_GET_NOTES == "Notes retrieved successfully."

    @pytest.mark.unit
    def test_message_success_delete_note(self) -> None:
        assert MESSAGE_SUCCESS_DELETE_NOTE == "The note was successfully deleted."

    @pytest.mark.unit
    def test_message_error_internal_server_is_non_empty(self) -> None:
        assert isinstance(MESSAGE_ERROR_INTERNAL_SERVER, str)
        assert len(MESSAGE_ERROR_INTERNAL_SERVER) > 0

    @pytest.mark.unit
    def test_message_not_valid_object_id(self) -> None:
        assert MESSAGE_NOT_VALID_OBJECT_ID == "The value entered is not a valid ObjectId."

    @pytest.mark.unit
    def test_message_already_exists_note(self) -> None:
        assert MESSAGE_ALREADY_EXISTS_NOTE == "Note already exists."

    @pytest.mark.unit
    def test_message_not_found_note(self) -> None:
        assert MESSAGE_NOT_FOUND_NOTE == "No note found."

    @pytest.mark.unit
    def test_all_messages_are_non_empty_strings(self) -> None:
        messages: list[str] = [
            MESSAGE_SUCCESS_ADD_NOTE,
            MESSAGE_SUCCESS_GET_NOTES,
            MESSAGE_SUCCESS_DELETE_NOTE,
            MESSAGE_ERROR_INTERNAL_SERVER,
            MESSAGE_ERROR_PYDANTIC,
            MESSAGE_ERROR_DATABASE,
            MESSAGE_ERROR_GENERIC,
            MESSAGE_ERROR_AUTHENTICATION,
            MESSAGE_NOT_VALID_INTEGER,
            MESSAGE_NOT_VALID_OBJECT_ID,
            MESSAGE_ALREADY_EXISTS_NOTE,
            MESSAGE_NOT_FOUND_NOTE,
        ]
        for message in messages:
            assert isinstance(message, str)
            assert len(message) > 0
