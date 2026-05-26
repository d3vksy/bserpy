from __future__ import annotations

from typing import TYPE_CHECKING

from ..models._match import BattleUserResult

if TYPE_CHECKING:
    from .._http import SyncTransport


class MatchesResource:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def get(self, game_id: int) -> list[BattleUserResult]:
        """특정 경기의 전체 플레이어 결과."""
        data = self._t.get(f"/v1/games/{game_id}")
        return [BattleUserResult.from_dict(g) for g in data.get("userGames", [])]
