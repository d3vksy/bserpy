from __future__ import annotations

from typing import TYPE_CHECKING

from ..models._match import BattleUserResult
from ..models._union import UnionTeam
from ..models._user import UserInfo, UserRank, UserStats

if TYPE_CHECKING:
    from .._http import SyncTransport


class UsersResource:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def get_uid(self, nickname: str) -> UserInfo:
        """닉네임으로 userId 조회."""
        data = self._t.get("/v1/user/nickname", query=nickname)
        return UserInfo.from_dict(data["user"])

    def get_games(self, user_id: str) -> list[BattleUserResult]:
        """지난 90일간 플레이한 경기 목록."""
        data = self._t.get(f"/v1/user/games/uid/{user_id}")
        return [BattleUserResult.from_dict(g) for g in data.get("userGames", [])]

    def get_rank(self, user_id: str, season_id: int, team_mode: int = 3) -> UserRank:
        """특정 시즌의 랭크 정보. team_mode는 현재 3(스쿼드)만 지원."""
        data = self._t.get(f"/v1/rank/uid/{user_id}/{season_id}/{team_mode}")
        return UserRank.from_dict(data["userRank"])

    def get_stats(self, user_id: str, season_id: int, mode: int = 3) -> list[UserStats]:
        """시즌별 통계. mode: 2=일반, 3=랭크."""
        data = self._t.get(f"/v2/user/stats/uid/{user_id}/{season_id}/{mode}")
        return [UserStats.from_dict(s) for s in data.get("userStats", [])]

    def get_union_team(self, user_id: str, season_id: int) -> list[UnionTeam]:
        """유니온 팀 정보."""
        data = self._t.get(f"/v1/unionTeam/uid/{user_id}/{season_id}")
        return [UnionTeam.from_dict(t) for t in data.get("teams", [])]
