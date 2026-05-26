from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


def _parse_int_list(raw: str | list[Any] | None) -> list[int]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [int(x) for x in raw]
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [int(x) for x in parsed]
    except (json.JSONDecodeError, ValueError):
        pass
    return []


def _parse_late_game(raw: str | dict[str, Any] | None) -> dict[str, list[int]]:
    """lateGameItemCodes: JSON 문자열 또는 dict → dict[str, list[int]]."""
    if raw is None:
        return {}
    if isinstance(raw, dict):
        result = {}
        for k, v in raw.items():
            result[k] = _parse_int_list(v)
        return result
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            result = {}
            for k, v in parsed.items():
                result[k] = _parse_int_list(v)
            return result
    except (json.JSONDecodeError, ValueError):
        pass
    return {}


@dataclass
class RecommendWeaponRoute:
    """추천 무기 루트 정보.

    실제 응답 키: ``recommendWeaponRoute``
    (문서는 ``recommendedWeaponRoute`` 로 잘못 기재 — d 하나 차이)
    """

    id: int
    title: str
    user_num: int  # 레거시 userNum 그대로 노출 (문서의 userId와 다름)
    user_nickname: str
    character_code: int
    slot_id: int
    weapon_type: int
    weapon_codes: list[int]  # JSON 문자열 → 자동 파싱
    trait_codes: list[int]  # JSON 문자열 → 자동 파싱
    late_game_item_codes: dict[str, list[int]]  # JSON 문자열 → 자동 파싱
    remote_transfer_item_codes: list[int]
    tactical_skill_group_code: int
    paths: list[int]  # JSON 문자열 → 자동 파싱
    count: int
    version: str
    team_mode: int
    language_code: str
    route_version: int
    share: bool
    update_dtm: int
    v2_like: int
    v2_win_rate: float
    v2_season_id: int
    v2_accumulate_like: int
    v2_accumulate_win_rate: float
    v2_accumulate_season_id: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RecommendWeaponRoute:
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            user_num=data.get("userNum", 0),
            user_nickname=data.get("userNickname", ""),
            character_code=data["characterCode"],
            slot_id=data.get("slotId", 0),
            weapon_type=data.get("weaponType", 0),
            weapon_codes=_parse_int_list(data.get("weaponCodes")),
            trait_codes=_parse_int_list(data.get("traitCodes")),
            late_game_item_codes=_parse_late_game(data.get("lateGameItemCodes")),
            remote_transfer_item_codes=_parse_int_list(data.get("remoteTransferItemCodes")),
            tactical_skill_group_code=data.get("tacticalSkillGroupCode", 0),
            paths=_parse_int_list(data.get("paths")),
            count=data.get("count", 0),
            version=data.get("version", ""),
            team_mode=data.get("teamMode", 0),
            language_code=data.get("languageCode", ""),
            route_version=data.get("routeVersion", 1),
            share=data.get("share", False),
            update_dtm=data.get("updateDtm", 0),
            v2_like=data.get("v2Like", 0),
            v2_win_rate=data.get("v2WinRate", 0.0),
            v2_season_id=data.get("v2SeasonId", 0),
            v2_accumulate_like=data.get("v2AccumulateLike", 0),
            v2_accumulate_win_rate=data.get("v2AccumulateWinRate", 0.0),
            v2_accumulate_season_id=data.get("v2AccumulateSeasonId", 0),
        )


@dataclass
class RecommendWeaponRouteDesc:
    """추천 무기 루트의 스킬 오더 및 설명."""

    recommend_weapon_route_id: int
    skill_path: str
    desc: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RecommendWeaponRouteDesc:
        return cls(
            recommend_weapon_route_id=data["recommendWeaponRouteId"],
            skill_path=data.get("skillPath", ""),
            desc=data.get("desc", ""),
        )


@dataclass
class WeaponRouteBundle:
    """루트 정보와 설명을 묶은 번들."""

    route: RecommendWeaponRoute
    desc: RecommendWeaponRouteDesc

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WeaponRouteBundle:
        # 실제 키: recommendWeaponRoute (문서 오기: recommendedWeaponRoute)
        route_data = data.get("recommendWeaponRoute") or data.get("recommendedWeaponRoute", {})
        desc_data = data.get("recommendWeaponRouteDesc") or data.get(
            "recommendedWeaponRouteDesc", {}
        )
        return cls(
            route=RecommendWeaponRoute.from_dict(route_data),
            desc=RecommendWeaponRouteDesc.from_dict(desc_data),
        )
