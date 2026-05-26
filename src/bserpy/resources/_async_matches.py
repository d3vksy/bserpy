from __future__ import annotations

from typing import TYPE_CHECKING

from ..models._match import BattleUserResult

if TYPE_CHECKING:
    from .._http import AsyncTransport


class AsyncMatchesResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def get(self, game_id: int) -> list[BattleUserResult]:
        data = await self._t.get(f"/v1/games/{game_id}")
        return [BattleUserResult.from_dict(g) for g in data.get("userGames", [])]
