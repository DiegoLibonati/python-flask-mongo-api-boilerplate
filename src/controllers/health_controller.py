from flask import jsonify
from flask.typing import ResponseReturnValue

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY


def health() -> ResponseReturnValue:
    return jsonify({"code": CODE_SUCCESS_HEALTH, "message": MESSAGE_SUCCESS_HEALTH}), 200


def ready() -> ResponseReturnValue:
    return jsonify({"code": CODE_SUCCESS_READY, "message": MESSAGE_SUCCESS_READY}), 200
