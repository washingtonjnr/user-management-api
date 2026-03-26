from abc import ABC, abstractmethod
from typing import Any


class UseCaseBase(ABC):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass
