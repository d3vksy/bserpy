from __future__ import annotations

import httpx

from ._http import SyncTransport
from .resources._matches import MatchesResource
from .resources._meta import MetaResource
from .resources._ranking import RankingResource
from .resources._users import UsersResource


class Client:
    """이터널 리턴 Open API 동기 클라이언트."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout: httpx.Timeout | None = None,
        max_retries: int = 3,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = SyncTransport(
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )
        self.users = UsersResource(self._transport)
        self.ranking = RankingResource(self._transport)
        self.matches = MatchesResource(self._transport)
        self.meta = MetaResource(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return "Client(api_key='****')"
