from api.domain.contracts.repositories.user_repository_base import UserRepositoryBase
from api.domain.entities.user import User


class UserRepository(UserRepositoryBase):
    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def create(self, user: User) -> User:
        self._store[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return self._store.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)
