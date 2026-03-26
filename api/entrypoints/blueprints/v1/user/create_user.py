from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from api.app.dtos.user.create_user_dto import CreateUserInputDTO

create_user_bp = Blueprint("create_user", __name__)


@create_user_bp.post("/")
def create_user():
    try:
        body = CreateUserInputDTO(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    # TODO: usecase vai aqui

    return jsonify({"message": "ok"}), 201
