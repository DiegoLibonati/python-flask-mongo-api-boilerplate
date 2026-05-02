from flask import Blueprint

from src.controllers.note_controller import alive, create_note, delete_note, get_notes, test_error

note_bp = Blueprint("note", __name__)

note_bp.route("/alive", methods=["GET"])(alive)
note_bp.route("/test_error", methods=["GET"])(test_error)
note_bp.route("/", methods=["POST"])(create_note)
note_bp.route("/", methods=["GET"])(get_notes)
note_bp.route("/<id>", methods=["DELETE"])(delete_note)
