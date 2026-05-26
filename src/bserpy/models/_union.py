from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# 축약 키 → 가독성 있는 이름 매핑
_TIER_WIN_KEYS: list[tuple[str, str]] = [
    ("ssstw", "SSS"),
    ("sstw", "SS"),
    ("stw", "S"),
    ("aaatw", "AAA"),
    ("aatw", "AA"),
    ("atw", "A"),
    ("bbbtw", "BBB"),
    ("bbtw", "BB"),
    ("btw", "B"),
    ("ccctw", "CCC"),
    ("cctw", "CC"),
    ("ctw", "C"),
    ("dddtw", "DDD"),
    ("ddtw", "DD"),
    ("dtw", "D"),
    ("etw", "E"),
    ("ffftw", "FFF"),
    ("fftw", "FF"),
    ("ftw", "F"),
]


@dataclass
class UnionTeam:
    """유니온 팀 티어 및 통계.

    API 응답의 단축 키(tnm, ti 등)를 가독성 있는 이름으로 변환.
    """

    team_name: str
    tier: int
    s_tier_tickets: int
    ss_tier_tickets: int
    sss_tier_tickets: int
    season_highest_tier: int
    win_count_by_tier: dict[str, int]    # {"SSS": 2, "SS": 5, ...}
    created_at: int                       # epoch time
    updated_at: int                       # epoch time

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UnionTeam:
        win_count = {label: data.get(key, 0) for key, label in _TIER_WIN_KEYS}
        return cls(
            team_name=data["tnm"],
            tier=data["ti"],
            s_tier_tickets=data.get("stt", 0),
            ss_tier_tickets=data.get("sstt", 0),
            sss_tier_tickets=data.get("ssstt", 0),
            season_highest_tier=data.get("ssti", 0),
            win_count_by_tier=win_count,
            created_at=data.get("cdt", 0),
            updated_at=data.get("udt", 0),
        )
