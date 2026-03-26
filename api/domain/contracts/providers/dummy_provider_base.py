from abc import ABC, abstractmethod
from typing import Any


class DummyProviderBase(ABC):
    @abstractmethod
    def get_user_additional_data(self, random_id: str) -> dict[str, Any]:
        pass
