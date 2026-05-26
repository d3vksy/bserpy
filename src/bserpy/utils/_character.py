from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bserpy._client import Client

# Character 테이블 (기본 스탯) camelCase → snake_case
# 주의: criticalStrikeChance (Character) vs criticalChance (CharacterLevelUpStat) — 키 이름이 다름
_BASE_FIELDS: dict[str, str] = {
    "maxHp": "max_hp",
    "maxVp": "max_vp",
    "attackPower": "attack_power",
    "defense": "defense",
    "skillAmp": "skill_amp",
    "adaptiveForce": "adaptive_force",
    "criticalStrikeChance": "critical_strike_chance",
    "hpRegen": "hp_regen",
    "vpRegen": "vp_regen",
    "attackSpeed": "attack_speed",
    "attackSpeedRatio": "attack_speed_ratio",
    "attackSpeedLimit": "attack_speed_limit",
    "increaseBasicAttackDamageRatio": "increase_basic_attack_damage_ratio",
    "skillAmpRatio": "skill_amp_ratio",
    "preventBasicAttackDamagedRatio": "prevent_basic_attack_damaged_ratio",
    "preventSkillDamagedRatio": "prevent_skill_damaged_ratio",
    "moveSpeed": "move_speed",
    "sightRange": "sight_range",
}

# CharacterLevelUpStat 테이블 — criticalChance로 다름, sightRange/attackSpeedLimit 없음
_LEVELUP_FIELDS: dict[str, str] = {
    "maxHp": "max_hp",
    "maxVp": "max_vp",
    "attackPower": "attack_power",
    "defense": "defense",
    "skillAmp": "skill_amp",
    "adaptiveForce": "adaptive_force",
    "criticalChance": "critical_strike_chance",
    "hpRegen": "hp_regen",
    "vpRegen": "vp_regen",
    "attackSpeed": "attack_speed",
    "attackSpeedRatio": "attack_speed_ratio",
    "increaseBasicAttackDamageRatio": "increase_basic_attack_damage_ratio",
    "skillAmpRatio": "skill_amp_ratio",
    "preventBasicAttackDamagedRatio": "prevent_basic_attack_damaged_ratio",
    "preventSkillDamagedRatio": "prevent_skill_damaged_ratio",
    "moveSpeed": "move_speed",
}


@dataclass
class CharacterStats:
    """캐릭터 스탯 (특정 레벨 기준).

    Attributes:
        level: 0이면 레벨당 증가량(growth), 1이면 기본값, 2–20이면 해당 레벨 계산값.
        attack_speed_limit: 공격 속도 상한 (기본 스탯에만 존재, growth에는 0).
        sight_range: 시야 범위 (기본 스탯에만 존재, growth에는 0).
    """

    code: int
    name: str
    level: int
    # ── HP / 에너지 ─────────────────────────────────────────
    max_hp: float = 0.0
    max_vp: float = 0.0
    hp_regen: float = 0.0
    vp_regen: float = 0.0
    # ── 공격 ────────────────────────────────────────────────
    attack_power: float = 0.0
    attack_speed: float = 0.0
    attack_speed_ratio: float = 0.0
    attack_speed_limit: float = 0.0
    increase_basic_attack_damage_ratio: float = 0.0  # 평타 증폭
    # ── 방어 ────────────────────────────────────────────────
    defense: float = 0.0
    prevent_basic_attack_damaged_ratio: float = 0.0  # 평타 피해 감소
    prevent_skill_damaged_ratio: float = 0.0          # 스킬 피해 감소
    # ── 스킬 ────────────────────────────────────────────────
    skill_amp: float = 0.0
    skill_amp_ratio: float = 0.0                      # 스킬 증폭
    adaptive_force: float = 0.0                       # 적응형 능력치
    # ── 기타 ────────────────────────────────────────────────
    critical_strike_chance: float = 0.0
    move_speed: float = 0.0
    sight_range: float = 0.0


@dataclass
class CharacterInfo:
    """캐릭터 메타 정보 (수치 스탯 외)."""

    code: int
    name: str
    char_arche_type1: str = ""    # 주 타입: "Warrior", "Assassin", "Hunter", "Scientist", "Tanker", "Support"
    char_arche_type2: str = ""    # 부 타입 (없으면 "None")
    weapon_range_type: str = ""   # "Melee" / "Ranged"
    start_skills: list[str] = field(default_factory=list)  # 시작 시 배운 스킬


@dataclass
class MasteryBonusStat:
    """숙련도 보너스 스탯 하나."""

    name: str
    value: float


@dataclass
class MasteryStatBonus:
    """숙련도별 스탯 보너스 (무기·전투·생존 공통).

    ``bonuses`` 는 실제 보너스 스탯만 담습니다 (``"None"`` 항목 제외, 최대 3개).
    """

    mastery_type: str
    character_code: int
    bonuses: list[MasteryBonusStat]


@dataclass
class CharacterMasteryOptions:
    """캐릭터가 선택 가능한 숙련도 종류."""

    code: int
    weapon_types: list[str] = field(default_factory=list)
    combat_types: list[str] = field(default_factory=list)
    survival_types: list[str] = field(default_factory=list)


class CharacterHelper:
    """캐릭터 스탯 조회 및 레벨별 계산 헬퍼.

    메타 테이블은 최초 접근 시 한 번만 로드하고 이후 캐시합니다.

    Example::

        with Client(api_key="...") as client:
            chars = CharacterHelper(client)

            # 레벨별 스탯
            lv15 = chars.stats_at_level(1, level=15)
            print(lv15.max_hp, lv15.skill_amp_ratio)

            # 무기 숙련도 스탯
            bonus = chars.mastery_stat(1, "OneHandSword")
            print(bonus.first_option, bonus.first_value())

            # 캐릭터 메타
            info = chars.info(1)
            print(info.char_arche_type1, info.weapon_range_type)
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._base: dict[int, dict[str, Any]] | None = None
        self._levelup: dict[int, dict[str, Any]] | None = None
        self._mastery_opts: dict[int, dict[str, Any]] | None = None
        # (character_code, weapon_type) → MasteryStatBonus
        self._mastery_stat: dict[tuple[int, str], MasteryStatBonus] | None = None

    # ── 데이터 로딩 (첫 접근 시 캐시, 이후 캐시 반환) ─────────

    def _load_base(self) -> dict[int, dict[str, Any]]:
        if self._base is None:
            rows = self._client.meta.get_data("Character")
            self._base = {r["code"]: r for r in rows}
        return self._base

    def _load_levelup(self) -> dict[int, dict[str, Any]]:
        if self._levelup is None:
            rows = self._client.meta.get_data("CharacterLevelUpStat")
            self._levelup = {r["code"]: r for r in rows}
        return self._levelup

    def _load_mastery_opts(self) -> dict[int, dict[str, Any]]:
        if self._mastery_opts is None:
            rows = self._client.meta.get_data("CharacterMastery")
            self._mastery_opts = {r["code"]: r for r in rows}
        return self._mastery_opts

    def _load_mastery_stat(self) -> dict[tuple[int, str], MasteryStatBonus]:
        if self._mastery_stat is None:
            rows = self._client.meta.get_data("MasteryStat")
            self._mastery_stat = {}
            for r in rows:
                key = (r["characterCode"], r["type"])
                raw = [
                    (r.get("firstOption", "None"), r.get("firstOptionSection1Value", 0)),
                    (r.get("secondOption", "None"), r.get("secondOptionSection1Value", 0)),
                    (r.get("thirdOption", "None"), r.get("thirdOptionSection1Value", 0)),
                ]
                bonuses = [
                    MasteryBonusStat(name=name, value=float(val))
                    for name, val in raw
                    if name != "None"
                ]
                self._mastery_stat[key] = MasteryStatBonus(
                    mastery_type=r["type"],
                    character_code=r["characterCode"],
                    bonuses=bonuses,
                )
        return self._mastery_stat

    # ── 내부 유틸 ────────────────────────────────────────────

    def _apply_fields(
        self, stats: CharacterStats, row: dict[str, Any], mapping: dict[str, str]
    ) -> None:
        for camel, snake in mapping.items():
            val = row.get(camel)
            if val is not None:
                setattr(stats, snake, float(val))

    # ── 공개 API ─────────────────────────────────────────────

    def base_stats(self, character_code: int) -> CharacterStats:
        """레벨 1 기본 스탯."""
        base = self._load_base()
        row = base[character_code]
        stats = CharacterStats(code=character_code, name=row.get("name", ""), level=1)
        self._apply_fields(stats, row, _BASE_FIELDS)
        return stats

    def level_up_stat(self, character_code: int) -> CharacterStats:
        """레벨당 증가량 (level=0으로 표시)."""
        levelup = self._load_levelup()
        row = levelup[character_code]
        stats = CharacterStats(code=character_code, name=row.get("name", ""), level=0)
        self._apply_fields(stats, row, _LEVELUP_FIELDS)
        return stats

    def stats_at_level(self, character_code: int, level: int) -> CharacterStats:
        """특정 레벨의 최종 스탯 계산.

        공식: base + growth * (level - 1)
        ``attack_speed_limit``, ``sight_range``는 레벨과 무관하게 기본값 그대로.
        """
        if not 1 <= level <= 20:
            raise ValueError(f"level은 1–20 사이여야 합니다. 입력값: {level}")
        base_table = self._load_base()
        growth_table = self._load_levelup()
        base_row = base_table[character_code]
        growth_row = growth_table[character_code]
        stats = CharacterStats(
            code=character_code, name=base_row.get("name", ""), level=level
        )
        # 공통 필드: base + growth * (level - 1)
        for camel, snake in _LEVELUP_FIELDS.items():
            b = float(base_row.get(camel) or base_row.get(
                "criticalStrikeChance" if camel == "criticalChance" else camel, 0
            ))
            g = float(growth_row.get(camel, 0))
            setattr(stats, snake, b + g * (level - 1))
        # 레벨 무관 필드 (base 전용)
        stats.attack_speed_limit = float(base_row.get("attackSpeedLimit", 0))
        stats.sight_range = float(base_row.get("sightRange", 0))
        return stats

    def info(self, character_code: int) -> CharacterInfo:
        """캐릭터 메타 정보 (타입, 사거리, 시작 스킬)."""
        base = self._load_base()
        row = base[character_code]
        start_skills = [
            s.strip()
            for s in row.get("strLearnStartSkill", "").split(",")
            if s.strip()
        ]
        return CharacterInfo(
            code=character_code,
            name=row.get("name", ""),
            char_arche_type1=row.get("charArcheType1", ""),
            char_arche_type2=row.get("charArcheType2", ""),
            weapon_range_type=row.get("weaponRangeType", ""),
            start_skills=start_skills,
        )

    def mastery_options(self, character_code: int) -> CharacterMasteryOptions:
        """캐릭터가 선택 가능한 무기·전투·생존 숙련도 목록."""
        mastery_table = self._load_mastery_opts()
        row = mastery_table[character_code]
        weapons = [row[k] for k in ("weapon1", "weapon2", "weapon3", "weapon4") if row.get(k)]
        combats = [row[k] for k in ("combat1", "combat2") if row.get(k)]
        survivals = [row[k] for k in ("survival1", "survival2", "survival3") if row.get(k)]
        return CharacterMasteryOptions(
            code=character_code,
            weapon_types=weapons,
            combat_types=combats,
            survival_types=survivals,
        )

    def mastery_stat(
        self, character_code: int, mastery_type: str
    ) -> MasteryStatBonus | None:
        """특정 무기 숙련도의 스탯 보너스.

        무기 숙련도는 캐릭터별로 다르며 ``character_code`` 로 구분됩니다.
        방어·사냥·제작 등 공통 숙련도는 ``character_code=0`` 으로 저장되어 있습니다.

        Args:
            character_code: 캐릭터 코드 (공통 숙련도는 0)
            mastery_type: ``"OneHandSword"``, ``"Axe"`` 등

        Returns:
            ``MasteryStatBonus`` 또는 해당 조합이 없으면 ``None``
        """
        return self._load_mastery_stat().get((character_code, mastery_type))

    def all_mastery_stats(self, character_code: int) -> list[MasteryStatBonus]:
        """캐릭터의 모든 숙련도 스탯 보너스 목록 (무기·전투·생존 포함)."""
        return [v for (code, _), v in self._load_mastery_stat().items() if code == character_code]

    def all_character_codes(self) -> list[int]:
        """모든 유효한 캐릭터 코드 목록."""
        return sorted(self._load_base().keys())
