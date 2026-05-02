from typing import Any

import pytest
from bson import ObjectId
from flask.testing import FlaskClient
from pymongo.database import Database


class TestAliveRoute:
    @pytest.mark.integration
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    @pytest.mark.integration
    def test_response_contains_version_bp(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, Any] = response.get_json()
        assert "version_bp" in data
        assert data["version_bp"] == "1.0.0"

    @pytest.mark.integration
    def test_response_contains_author(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, Any] = response.get_json()
        assert data["author"] == "Diego Libonati"

    @pytest.mark.integration
    def test_response_contains_name_bp(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, Any] = response.get_json()
        assert data["name_bp"] == "Note"

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/alive")
        assert response.content_type == "application/json"


class TestTestErrorRoute:
    @pytest.mark.integration
    def test_returns_500(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/test_error")
        assert response.status_code == 500

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/test_error")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "CODE_NOTE_ERROR_TEST_MESSAGE"

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/test_error")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "NoteError test message."

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/test_error")
        assert response.content_type == "application/json"


class TestCreateNoteRoute:
    @pytest.mark.integration
    def test_returns_201_when_created(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/notes/", json={"name": "new_note"})
        assert response.status_code == 201

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/notes/", json={"name": "msg_note"})
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "The note was successfully added."

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/notes/", json={"name": "code_note"})
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_ADD_NOTE"

    @pytest.mark.integration
    def test_response_contains_data_with_inserted_id(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/notes/", json={"name": "id_note"})
        data: dict[str, Any] = response.get_json()
        assert "data" in data
        assert isinstance(data["data"], str)

    @pytest.mark.integration
    def test_returns_400_with_empty_name(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/notes/", json={"name": ""})
        assert response.status_code == 400

    @pytest.mark.integration
    def test_returns_400_with_missing_name_field(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/notes/", json={})
        assert response.status_code == 400

    @pytest.mark.integration
    def test_returns_409_when_name_already_exists(self, client: FlaskClient, mongo_db: Database) -> None:
        client.post("/api/v1/notes/", json={"name": "duplicate_note"})
        response = client.post("/api/v1/notes/", json={"name": "duplicate_note"})
        assert response.status_code == 409

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/notes/", json={"name": "json_note"})
        assert response.content_type == "application/json"


class TestGetNotesRoute:
    @pytest.mark.integration
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_GET_NOTES"

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "Notes retrieved successfully."

    @pytest.mark.integration
    def test_response_data_is_list(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert isinstance(data["data"], list)

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/notes/")
        assert response.content_type == "application/json"

    @pytest.mark.integration
    def test_returns_inserted_notes(self, client: FlaskClient, mongo_db: Database) -> None:
        client.post("/api/v1/notes/", json={"name": "note_alpha"})
        client.post("/api/v1/notes/", json={"name": "note_beta"})
        response = client.get("/api/v1/notes/")
        notes: list[dict[str, Any]] = response.get_json()["data"]
        names: list[str] = [n["name"] for n in notes]
        assert "note_alpha" in names
        assert "note_beta" in names

    @pytest.mark.integration
    def test_returns_empty_data_after_cleanup(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["data"] == []


class TestDeleteNoteRoute:
    @pytest.mark.integration
    def test_returns_200_when_deleted(self, client: FlaskClient, mongo_db: Database) -> None:
        post_data: dict[str, Any] = client.post("/api/v1/notes/", json={"name": "to_delete"}).get_json()
        _id: str = post_data["data"]
        response = client.delete(f"/api/v1/notes/{_id}")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient, mongo_db: Database) -> None:
        post_data: dict[str, Any] = client.post("/api/v1/notes/", json={"name": "msg_delete"}).get_json()
        _id: str = post_data["data"]
        response = client.delete(f"/api/v1/notes/{_id}")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "The note was successfully deleted."

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient, mongo_db: Database) -> None:
        post_data: dict[str, Any] = client.post("/api/v1/notes/", json={"name": "code_delete"}).get_json()
        _id: str = post_data["data"]
        response = client.delete(f"/api/v1/notes/{_id}")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_DELETE_NOTE"

    @pytest.mark.integration
    def test_returns_404_when_note_not_found(self, client: FlaskClient) -> None:
        response = client.delete(f"/api/v1/notes/{str(ObjectId())}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_returns_400_with_invalid_id(self, client: FlaskClient) -> None:
        response = client.delete("/api/v1/notes/not_a_valid_id")
        assert response.status_code == 400

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient, mongo_db: Database) -> None:
        post_data: dict[str, Any] = client.post("/api/v1/notes/", json={"name": "json_delete"}).get_json()
        _id: str = post_data["data"]
        response = client.delete(f"/api/v1/notes/{_id}")
        assert response.content_type == "application/json"
