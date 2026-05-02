from typing import Any

import pytest
from bson import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.note_dao import NoteDAO


class TestInsertOne:
    @pytest.mark.integration
    def test_inserts_document_and_returns_result(self, app, mongo_db: Database) -> None:
        note: dict[str, Any] = {"name": "test_note"}
        result: InsertOneResult = NoteDAO.insert_one(note)
        assert result.inserted_id is not None

    @pytest.mark.integration
    def test_inserted_document_is_findable(self, app, mongo_db: Database) -> None:
        NoteDAO.insert_one({"name": "findable_note"})
        found: dict[str, Any] | None = NoteDAO.find_one_by_name("findable_note")
        assert found is not None
        assert found["name"] == "findable_note"


class TestFind:
    @pytest.mark.integration
    def test_returns_empty_list_when_no_documents(self, app, mongo_db: Database) -> None:
        result: list[dict[str, Any]] = NoteDAO.find()
        assert result == []

    @pytest.mark.integration
    def test_returns_all_documents(self, app, mongo_db: Database) -> None:
        NoteDAO.insert_one({"name": "alpha"})
        NoteDAO.insert_one({"name": "beta"})
        result: list[dict[str, Any]] = NoteDAO.find()
        assert len(result) == 2

    @pytest.mark.integration
    def test_documents_have_string_id(self, app, mongo_db: Database) -> None:
        NoteDAO.insert_one({"name": "typed_id"})
        result: list[dict[str, Any]] = NoteDAO.find()
        assert isinstance(result[0]["_id"], str)


class TestFindOneById:
    @pytest.mark.integration
    def test_returns_document_when_found(self, app, mongo_db: Database) -> None:
        insert_result: InsertOneResult = NoteDAO.insert_one({"name": "by_id"})
        _id: ObjectId = insert_result.inserted_id
        found: dict[str, Any] | None = NoteDAO.find_one_by_id(_id)
        assert found is not None
        assert found["name"] == "by_id"

    @pytest.mark.integration
    def test_returns_none_when_not_found(self, app, mongo_db: Database) -> None:
        result: dict[str, Any] | None = NoteDAO.find_one_by_id(ObjectId())
        assert result is None

    @pytest.mark.integration
    def test_returned_document_has_string_id(self, app, mongo_db: Database) -> None:
        insert_result: InsertOneResult = NoteDAO.insert_one({"name": "str_id"})
        found: dict[str, Any] | None = NoteDAO.find_one_by_id(insert_result.inserted_id)
        assert isinstance(found["_id"], str)


class TestFindOneByName:
    @pytest.mark.integration
    def test_returns_document_when_name_matches(self, app, mongo_db: Database) -> None:
        NoteDAO.insert_one({"name": "exact_name"})
        found: dict[str, Any] | None = NoteDAO.find_one_by_name("exact_name")
        assert found is not None
        assert found["name"] == "exact_name"

    @pytest.mark.integration
    def test_matches_case_insensitively(self, app, mongo_db: Database) -> None:
        NoteDAO.insert_one({"name": "CaseName"})
        found: dict[str, Any] | None = NoteDAO.find_one_by_name("casename")
        assert found is not None

    @pytest.mark.integration
    def test_returns_none_when_not_found(self, app, mongo_db: Database) -> None:
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("nonexistent")
        assert result is None


class TestDeleteOneById:
    @pytest.mark.integration
    def test_deletes_existing_document(self, app, mongo_db: Database) -> None:
        insert_result: InsertOneResult = NoteDAO.insert_one({"name": "to_delete"})
        _id: ObjectId = insert_result.inserted_id
        delete_result: DeleteResult = NoteDAO.delete_one_by_id(_id)
        assert delete_result.deleted_count == 1

    @pytest.mark.integration
    def test_document_is_gone_after_delete(self, app, mongo_db: Database) -> None:
        insert_result: InsertOneResult = NoteDAO.insert_one({"name": "gone"})
        _id: ObjectId = insert_result.inserted_id
        NoteDAO.delete_one_by_id(_id)
        found: dict[str, Any] | None = NoteDAO.find_one_by_id(_id)
        assert found is None

    @pytest.mark.integration
    def test_deleting_nonexistent_id_returns_zero_count(self, app, mongo_db: Database) -> None:
        result: DeleteResult = NoteDAO.delete_one_by_id(ObjectId())
        assert result.deleted_count == 0


class TestParseNote:
    @pytest.mark.unit
    def test_returns_none_for_falsy_input(self) -> None:
        result: dict[str, Any] | None = NoteDAO.parse_note(None)
        assert result is None

    @pytest.mark.unit
    def test_converts_objectid_to_string(self) -> None:
        _id: ObjectId = ObjectId()
        raw: dict[str, Any] = {"_id": _id, "name": "note"}
        result: dict[str, Any] = NoteDAO.parse_note(raw)
        assert result["_id"] == str(_id)
        assert isinstance(result["_id"], str)

    @pytest.mark.unit
    def test_preserves_other_fields(self) -> None:
        raw: dict[str, Any] = {"_id": ObjectId(), "name": "preserved"}
        result: dict[str, Any] = NoteDAO.parse_note(raw)
        assert result["name"] == "preserved"

    @pytest.mark.unit
    def test_does_not_include_raw_objectid_in_result(self) -> None:
        _id: ObjectId = ObjectId()
        raw: dict[str, Any] = {"_id": _id, "name": "no_raw"}
        result: dict[str, Any] = NoteDAO.parse_note(raw)
        assert not isinstance(result["_id"], ObjectId)


class TestParseNotes:
    @pytest.mark.unit
    def test_returns_empty_list_for_empty_input(self) -> None:
        result: list[dict[str, Any]] = NoteDAO.parse_notes([])
        assert result == []

    @pytest.mark.unit
    def test_parses_all_documents(self) -> None:
        docs: list[dict[str, Any]] = [
            {"_id": ObjectId(), "name": "a"},
            {"_id": ObjectId(), "name": "b"},
        ]
        result: list[dict[str, Any]] = NoteDAO.parse_notes(docs)
        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)
