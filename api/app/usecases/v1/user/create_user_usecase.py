from api.app.dtos.user.create_user_dto import CreateUserInputDTO, CreateUserOutputDTO
from api.domain.contracts.app.usecase import UseCaseBase
from api.domain.contracts.repositories.user_repository_base import UserRepositoryBase
from api.domain.entities.user import User


class CreateUserUseCase(UseCaseBase):
    def __init__(self, user_repository: UserRepositoryBase) -> None:
        self._user_repository = user_repository

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        user = User(
            name=input_dto.name,
            email=input_dto.email,
            password=input_dto.password,
            role=input_dto.role,
        )

        created_user = self._user_repository.create(user)

        return CreateUserOutputDTO(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
        )
