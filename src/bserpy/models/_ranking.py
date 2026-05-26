from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TopRank:
    """통합/서버별 상위 랭커."""

    nickname: str
    rank: int
    mmr: int
    user_emblems: list[Any] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TopRank:
        return cls(
            nickname=data["nickname"],
            rank=data["rank"],
            mmr=data["mmr"],
            user_emblems=data.get("userEmblems", []),
        )
