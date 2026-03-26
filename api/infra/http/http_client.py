from typing import Any

import requests

from api.domain.contracts.http.http_client_base import HttpClientBase


class HttpClient(HttpClientBase):
    def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = requests.get(url, headers=headers, params=params)

        response.raise_for_status()

        return response.json()

    def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        response = requests.post(url, headers=headers, json=body)

        response.raise_for_status()

        return response.json()

    def put(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        response = requests.put(url, headers=headers, json=body)

        response.raise_for_status()

        return response.json()

    def delete(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        response = requests.delete(
            url,
            headers=headers,
        )

        response.raise_for_status()

        return response.json()
