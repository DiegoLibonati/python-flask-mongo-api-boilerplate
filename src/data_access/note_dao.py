from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.configs.mongo_config import mongo


class NoteDAO:
    @staticmethod
    def insert_one(note: dict[str, Any]) -> InsertOneResult:
        return mongo.db.notes.insert_one(note)

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return NoteDAO.parse_notes(list(mongo.db.notes.find()))

    @staticmethod
    def find_one_by_id(_id: ObjectId) -> dict[str, Any] | None:
        return NoteDAO.parse_note(mongo.db.notes.find_one({"_id": ObjectId(_id)}))

    @staticmethod
    def find_one_by_name(name: str) -> dict[str, Any] | None:
        return NoteDAO.parse_note(mongo.db.notes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}}))

    @staticmethod
    def delete_one_by_id(_id: ObjectId) -> DeleteResult:
        return mongo.db.notes.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def parse_notes(notes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [NoteDAO.parse_note(note) for note in notes]

    @staticmethod
    def parse_note(note: dict[str, Any]) -> dict[str, Any]:
        if not note:
            return None

        return {
            **{k: v for k, v in note.items() if k != "_id"},
            "_id": str(note["_id"]),
        }
