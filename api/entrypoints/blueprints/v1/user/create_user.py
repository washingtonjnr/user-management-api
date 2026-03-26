from flask import Blueprint, jsonify, request
from flask_pydantic_spec import Response
from pydantic import ValidationError

from api.app.dtos.user.create_user_dto import CreateUserInputDTO, CreateUserOutputDTO
from api.app.usecases.v1.user.create_user_usecase import CreateUserUseCase
from api.config.spec import spec
from api.infra.repositories.user_repository import UserRepository

create_user_bp = Blueprint("create_user", __name__)

_user_repository = UserRepository()


@create_user_bp.post("/")
@spec.validate(
    body=CreateUserInputDTO,
    resp=Response(HTTP_201=CreateUserOutputDTO),
    tags=["Users"],
)
def create_user():
    try:
        body = CreateUserInputDTO(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    usecase = CreateUserUseCase(user_repository=_user_repository)
    output = usecase.execute(body)

    return jsonify(output.model_dump()), 201
