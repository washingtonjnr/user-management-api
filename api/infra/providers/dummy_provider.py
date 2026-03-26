from typing import Any

from api.config.settings import settings
from api.domain.contracts.http.http_client_base import HttpClientBase
from api.domain.contracts.providers.dummy_provider_base import DummyProviderBase


class DummyProvider(DummyProviderBase):
    def __init__(self, http_client: HttpClientBase) -> None:
        self._http_client = http_client

    async def get_user_additional_data(self, random_id: str) -> dict[str, Any]:
        url = f"{settings.dummy_url}/user/{random_id}"

        return await self._http_client.get(url)
