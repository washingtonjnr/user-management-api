from abc import ABC, abstractmethod
from typing import Any


class HttpClientBase(ABC):
    @abstractmethod
    def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        pass

    @abstractmethod
    def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        pass

    @abstractmethod
    def put(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        pass

    @abstractmethod
    def delete(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        pass
