from __future__ import annotations

from typing import TYPE_CHECKING

from ..models._match import BattleUserResult
from ..models._union import UnionTeam
from ..models._user import UserInfo, UserRank, UserStats

if TYPE_CHECKING:
    from .._http import AsyncTransport


class AsyncUsersResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def get_uid(self, nickname: str) -> UserInfo:
        data = await self._t.get("/v1/user/nickname", query=nickname)
        return UserInfo.from_dict(data["user"])

    async def get_games(self, user_id: str) -> list[BattleUserResult]:
        data = await self._t.get(f"/v1/user/games/uid/{user_id}")
        return [BattleUserResult.from_dict(g) for g in data.get("userGames", [])]

    async def get_rank(self, user_id: str, season_id: int, team_mode: int = 3) -> UserRank:
        data = await self._t.get(f"/v1/rank/uid/{user_id}/{season_id}/{team_mode}")
        return UserRank.from_dict(data["userRank"])

    async def get_stats(self, user_id: str, season_id: int, mode: int = 3) -> list[UserStats]:
        data = await self._t.get(f"/v2/user/stats/uid/{user_id}/{season_id}/{mode}")
        return [UserStats.from_dict(s) for s in data.get("userStats", [])]

    async def get_union_team(self, user_id: str, season_id: int) -> list[UnionTeam]:
        data = await self._t.get(f"/v1/unionTeam/uid/{user_id}/{season_id}")
        return [UnionTeam.from_dict(t) for t in data.get("teams", [])]
