from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UserInfo:
    """닉네임으로 조회한 사용자 식별 정보.

    실제 응답 키는 ``userId`` (문서에는 ``uid`` 로 잘못 기재됨).
    userId 값은 닉네임 변경 시 새로 발급되는 임시 토큰.
    """

    user_id: str
    nickname: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserInfo:
        return cls(
            user_id=data["userId"],
            nickname=data["nickname"],
        )


@dataclass
class UserRank:
    """특정 시즌/팀 모드에서의 플레이어 랭크."""

    nickname: str
    mmr: int
    rank: int
    server_code: int
    server_rank: int
    reward_server_code: int | None = None  # 문서 미기재, 실제 응답에 존재

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserRank:
        return cls(
            nickname=data["nickname"],
            mmr=data["mmr"],
            rank=data["rank"],
            server_code=data["serverCode"],
            server_rank=data["serverRank"],
            reward_server_code=data.get("rewardServerCode"),
        )


@dataclass
class CharacterStat:
    """유저가 특정 캐릭터로 플레이한 집계 통계."""

    character_code: int
    total_games: int
    usages: int
    max_killings: int
    top3: int
    wins: int
    most_used_skin_code: int | None = None  # 문서 미기재, 실제 존재
    latest_used_skin_code: int | None = None  # 문서 미기재, 실제 존재
    top3_rate: float | None = None  # 문서 미기재, 실제 존재
    average_rank: float | None = None  # 문서 미기재, 실제 존재

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CharacterStat:
        return cls(
            character_code=data["characterCode"],
            total_games=data["totalGames"],
            usages=data.get("usages", data["totalGames"]),
            max_killings=data["maxKillings"],
            top3=data["top3"],
            wins=data["wins"],
            most_used_skin_code=data.get("mostUsedSkinCode"),
            latest_used_skin_code=data.get("latestUsedSkinCode"),
            top3_rate=data.get("top3Rate"),
            average_rank=data.get("averageRank"),
        )


@dataclass
class UserStats:
    """시즌별 유저 통계 (matchingMode 단위)."""

    season_id: int
    matching_mode: int
    matching_team_mode: int
    mmr: int
    nickname: str
    rank: int
    rank_size: int
    total_games: int
    total_wins: int
    total_team_kills: int
    total_deaths: int
    escape_count: int
    rank_percent: float
    average_rank: float
    average_kills: float
    average_assistants: float
    average_hunts: float
    top1: float
    top2: float
    top3: float
    top5: float
    top7: float
    character_stats: list[CharacterStat] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserStats:
        return cls(
            season_id=data["seasonId"],
            matching_mode=data["matchingMode"],
            matching_team_mode=data["matchingTeamMode"],
            mmr=data["mmr"],
            nickname=data.get("nickname", ""),
            rank=data["rank"],
            rank_size=data["rankSize"],
            total_games=data["totalGames"],
            total_wins=data["totalWins"],
            total_team_kills=data["totalTeamKills"],
            total_deaths=data["totalDeaths"],
            escape_count=data["escapeCount"],
            rank_percent=data["rankPercent"],
            average_rank=data["averageRank"],
            average_kills=data["averageKills"],
            average_assistants=data["averageAssistants"],
            average_hunts=data["averageHunts"],
            top1=data["top1"],
            top2=data["top2"],
            top3=data["top3"],
            top5=data["top5"],
            top7=data["top7"],
            character_stats=[CharacterStat.from_dict(c) for c in data.get("characterStats", [])],
        )
