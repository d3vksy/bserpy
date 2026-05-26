from __future__ import annotations

from typing import TYPE_CHECKING

from ..models._enums import RegionServer
from ..models._ranking import TopRank

if TYPE_CHECKING:
    from .._http import AsyncTransport


class AsyncRankingResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def get_top(self, season_id: int, team_mode: int = 3) -> list[TopRank]:
        data = await self._t.get(f"/v1/rank/top/{season_id}/{team_mode}")
        return [TopRank.from_dict(r) for r in data.get("topRanks", [])]

    async def get_top_by_server(
        self, season_id: int, server: RegionServer | int, team_mode: int = 3
    ) -> list[TopRank]:
        data = await self._t.get(f"/v1/rank/top/{season_id}/{team_mode}/{int(server)}")
        return [TopRank.from_dict(r) for r in data.get("topRanks", [])]
