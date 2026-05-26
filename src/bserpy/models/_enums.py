from __future__ import annotations

from enum import IntEnum


class RegionServer(IntEnum):
    ASIA = 10
    NA = 12
    EUROPE = 13
    SA = 14
    ASIA2 = 17
    ASIA3 = 18


class MatchingMode(IntEnum):
    SQUAD_NORMAL = 2
    SQUAD_RANKED = 3
    COBALT = 6
    LONEWOLF = 9


class MatchingTeamMode(IntEnum):
    LONEWOLF = 1
    SQUAD = 3
    COBALT = 4
