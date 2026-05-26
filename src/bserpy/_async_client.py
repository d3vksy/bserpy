from __future__ import annotations

import httpx

from ._http import AsyncTransport
from .resources._async_matches import AsyncMatchesResource
from .resources._async_meta import AsyncMetaResource
from .resources._async_ranking import AsyncRankingResource
from .resources._async_users import AsyncUsersResource


class AsyncClient:
    """이터널 리턴 Open API 비동기 클라이언트."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout: httpx.Timeout | None = None,
        max_retries: int = 3,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )
        self.users = AsyncUsersResource(self._transport)
        self.ranking = AsyncRankingResource(self._transport)
        self.matches = AsyncMatchesResource(self._transport)
        self.meta = AsyncMetaResource(self._transport)

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return "AsyncClient(api_key='****')"
