from flask import Blueprint

from src.controllers.health_controller import health

health_bp = Blueprint("health", __name__)

health_bp.route("/", methods=["GET"])(health)
