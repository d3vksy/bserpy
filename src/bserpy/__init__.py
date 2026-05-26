"""bserpy — 이터널 리턴 Open API Python 래퍼."""

from __future__ import annotations

from ._async_client import AsyncClient
from ._client import Client
from ._errors import (
    AuthenticationError,
    BserError,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TransportError,
)
from .models import (
    BattleUserResult,
    CharacterStat,
    L10nData,
    MatchingMode,
    MatchingTeamMode,
    RecommendWeaponRoute,
    RecommendWeaponRouteDesc,
    RegionServer,
    TopRank,
    UnionTeam,
    UserInfo,
    UserRank,
    UserStats,
    WeaponRouteBundle,
)
from .utils import (
    CharacterHelper,
    CharacterInfo,
    CharacterMasteryOptions,
    CharacterSimulator,
    CharacterStats,
    ItemHelper,
    MasteryBonusStat,
    MasteryStatBonus,
    SeasonHelper,
    SimulatedStats,
)

__all__ = [
    # 클라이언트
    "Client",
    "AsyncClient",
    # 예외
    "BserError",
    "ConfigurationError",
    "TransportError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ServerError",
    # 모델
    "BattleUserResult",
    "CharacterStat",
    "L10nData",
    "MatchingMode",
    "MatchingTeamMode",
    "RegionServer",
    "RecommendWeaponRoute",
    "RecommendWeaponRouteDesc",
    "TopRank",
    "UnionTeam",
    "UserInfo",
    "UserRank",
    "UserStats",
    "WeaponRouteBundle",
    # 유틸리티
    "CharacterHelper",
    "CharacterInfo",
    "CharacterMasteryOptions",
    "CharacterSimulator",
    "CharacterStats",
    "ItemHelper",
    "MasteryBonusStat",
    "MasteryStatBonus",
    "SeasonHelper",
    "SimulatedStats",
]

__version__ = "0.2.3"
