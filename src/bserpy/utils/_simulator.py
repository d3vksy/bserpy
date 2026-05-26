from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bserpy._client import Client

from bserpy.utils._character import CharacterHelper, MasteryStatBonus
from bserpy.utils._item import ItemHelper

# (item_camel, lv_scale_camel_or_None, SimulatedStats_snake)
# ByLv 필드: item_stat + lv_stat * level 로 계산
_ITEM_STAT_MAP: list[tuple[str, str | None, str]] = [
    ("attackPower", "attackPowerByLv", "attack_power"),
    ("defense", "defenseByLv", "defense"),
    ("skillAmp", "skillAmpByLevel", "skill_amp"),
    ("skillAmpRatio", "skillAmpRatioByLevel", "skill_amp_ratio"),
    ("adaptiveForce", "adaptiveForceByLevel", "adaptive_force"),
    ("maxHp", "maxHpByLv", "max_hp"),
    ("hpRegen", None, "hp_regen"),
    ("hpRegenRatio", None, "hp_regen_ratio"),
    ("attackSpeedRatio", "attackSpeedRatioByLv", "attack_speed_ratio"),
    ("criticalStrikeChance", None, "critical_strike_chance"),
    ("criticalStrikeDamage", None, "critical_strike_damage"),
    ("preventCriticalStrikeDamaged", None, "prevent_critical_strike_damaged"),
    ("cooldownReduction", None, "cooldown_reduction"),
    ("cooldownLimit", None, "cooldown_limit"),
    ("lifeSteal", None, "life_steal"),
    ("normalLifeSteal", None, "normal_life_steal"),
    ("skillLifeSteal", None, "skill_life_steal"),
    ("moveSpeed", None, "move_speed"),
    ("moveSpeedRatio", None, "move_speed_ratio"),
    ("moveSpeedOutOfCombat", None, "move_speed_out_of_combat"),
    ("sightRange", None, "sight_range"),
    ("attackRange", None, "attack_range"),
    ("increaseBasicAttackDamage", "increaseBasicAttackDamageByLv", "increase_basic_attack_damage"),
    (
        "increaseBasicAttackDamageRatio",
        "increaseBasicAttackDamageRatioByLv",
        "increase_basic_attack_damage_ratio",
    ),
    ("preventBasicAttackDamaged", "preventBasicAttackDamagedByLv", "prevent_basic_attack_damaged"),
    (
        "preventBasicAttackDamagedRatio",
        "preventBasicAttackDamagedRatioByLv",
        "prevent_basic_attack_damaged_ratio",
    ),
    ("preventSkillDamaged", "preventSkillDamagedByLv", "prevent_skill_damaged"),
    ("preventSkillDamagedRatio", "preventSkillDamagedRatioByLv", "prevent_skill_damaged_ratio"),
    ("penetrationDefense", None, "penetration_defense"),
    ("penetrationDefenseRatio", None, "penetration_defense_ratio"),
    ("trapDamageReduce", None, "trap_damage_reduce"),
    ("trapDamageReduceRatio", None, "trap_damage_reduce_ratio"),
    ("slowResistRatio", None, "slow_resist_ratio"),
    ("hpHealedIncreaseRatio", None, "hp_healed_increase_ratio"),
    ("healerGiveHpHealRatio", None, "healer_give_hp_heal_ratio"),
    ("uniqueAttackRange", None, "unique_attack_range"),
    ("uniqueHpHealedIncreaseRatio", None, "unique_hp_healed_increase_ratio"),
    ("uniqueCooldownLimit", None, "unique_cooldown_limit"),
    ("uniqueTenacity", None, "unique_tenacity"),
    ("uniqueMoveSpeed", None, "unique_move_speed"),
    ("uniquePenetrationDefense", None, "unique_penetration_defense"),
    ("uniquePenetrationDefenseRatio", None, "unique_penetration_defense_ratio"),
    ("uniqueLifeSteal", None, "unique_life_steal"),
    ("uniqueSkillAmpRatio", None, "unique_skill_amp_ratio"),
    ("ultCooldownReduction", None, "ult_cooldown_reduction"),
    ("weaponCooldownReduction", None, "weapon_cooldown_reduction"),
    ("tacticalCooldownReduction", None, "tactical_cooldown_reduction"),
]

# 숙련도 스탯 이름(PascalCase) → SimulatedStats 필드명(snake_case)
# MasteryBonusStat.name 은 "AttackSpeedRatio" 같은 PascalCase
_MASTERY_STAT_MAP: dict[str, str] = {
    camel[0].upper() + camel[1:]: snake for camel, _, snake in _ITEM_STAT_MAP
}


@dataclass
class SimulatedStats:
    """캐릭터 기본 스탯 + 장착 아이템 합산 결과.

    ``effective_attack_speed`` 프로퍼티로 공속 상한 적용값을 얻을 수 있습니다.
    """

    character_code: int
    character_name: str
    level: int

    # ── HP / 에너지 ──────────────────────────────────────────
    max_hp: float = 0.0
    max_vp: float = 0.0
    hp_regen: float = 0.0
    hp_regen_ratio: float = 0.0
    vp_regen: float = 0.0

    # ── 공격 ────────────────────────────────────────────────
    attack_power: float = 0.0
    attack_speed: float = 0.0  # 캐릭터 기본 공속
    weapon_type_attack_speed: float = 0.0  # 무기 타입 기본 공속 (WeaponTypeInfo)
    attack_speed_ratio: float = 0.0  # 공속 증가율 합계
    attack_speed_limit: float = 0.0  # 공속 상한
    increase_basic_attack_damage: float = 0.0  # 평타 피해 고정 증가
    increase_basic_attack_damage_ratio: float = 0.0  # 평타 피해 증폭 (%)
    attack_range: float = 0.0

    # ── 방어 ────────────────────────────────────────────────
    defense: float = 0.0
    prevent_basic_attack_damaged: float = 0.0  # 평타 피해 감소 (고정)
    prevent_basic_attack_damaged_ratio: float = 0.0  # 평타 피해 감소 (%)
    prevent_skill_damaged: float = 0.0  # 스킬 피해 감소 (고정)
    prevent_skill_damaged_ratio: float = 0.0  # 스킬 피해 감소 (%)
    prevent_critical_strike_damaged: float = 0.0  # 치명타 피해 감소
    trap_damage_reduce: float = 0.0
    trap_damage_reduce_ratio: float = 0.0

    # ── 스킬 ────────────────────────────────────────────────
    skill_amp: float = 0.0  # 스킬 증폭 (고정)
    skill_amp_ratio: float = 0.0  # 스킬 증폭 (%)
    adaptive_force: float = 0.0  # 적응형 능력치

    # ── 치명타 ──────────────────────────────────────────────
    critical_strike_chance: float = 0.0
    critical_strike_damage: float = 0.0

    # ── 쿨다운 ──────────────────────────────────────────────
    cooldown_reduction: float = 0.0
    cooldown_limit: float = 0.0
    ult_cooldown_reduction: float = 0.0
    weapon_cooldown_reduction: float = 0.0
    tactical_cooldown_reduction: float = 0.0

    # ── 흡혈 ────────────────────────────────────────────────
    life_steal: float = 0.0
    normal_life_steal: float = 0.0
    skill_life_steal: float = 0.0

    # ── 관통 ────────────────────────────────────────────────
    penetration_defense: float = 0.0
    penetration_defense_ratio: float = 0.0

    # ── 이동 ────────────────────────────────────────────────
    move_speed: float = 0.0
    move_speed_ratio: float = 0.0
    move_speed_out_of_combat: float = 0.0

    # ── 기타 ────────────────────────────────────────────────
    sight_range: float = 0.0
    slow_resist_ratio: float = 0.0
    hp_healed_increase_ratio: float = 0.0
    healer_give_hp_heal_ratio: float = 0.0

    # ── unique (아이템 간 비중첩) ─────────────────────────
    unique_attack_range: float = 0.0
    unique_hp_healed_increase_ratio: float = 0.0
    unique_cooldown_limit: float = 0.0
    unique_tenacity: float = 0.0
    unique_move_speed: float = 0.0
    unique_penetration_defense: float = 0.0
    unique_penetration_defense_ratio: float = 0.0
    unique_life_steal: float = 0.0
    unique_skill_amp_ratio: float = 0.0

    # ── 장착 아이템 정보 (repr 제외) ──────────────────────
    equipped_weapon: dict[str, Any] | None = field(default=None, repr=False)
    equipped_armors: list[dict[str, Any]] = field(default_factory=list, repr=False)

    @property
    def effective_attack_speed(self) -> float:
        """공속 상한 적용 후 최종 공격 속도.

        공식: (캐릭터 기본 공속 + 무기 타입 기본 공속) × (1 + Σ 공속 증가율)
        무기 미장착 시 weapon_type_attack_speed=0, 숙련도 미적용.
        """
        base = self.attack_speed + self.weapon_type_attack_speed
        raw = base * (1.0 + self.attack_speed_ratio)
        return min(raw, self.attack_speed_limit) if self.attack_speed_limit > 0 else raw


class CharacterSimulator:
    """캐릭터 아이템 장착 스탯 시뮬레이터.

    메서드 체이닝을 지원하므로 한 줄로 작성할 수 있습니다.

    Example::

        with Client(api_key="...") as client:
            sim = CharacterSimulator(client, character_code=1, level=15)
            stats = (
                sim
                .add_weapon(101405)
                .add_armor(201305)   # 머리
                .add_armor(202305)   # 가슴
                .get_stats()
            )
            print(f"HP: {stats.max_hp:.0f}  ATK: {stats.attack_power:.1f}")
            print(f"공속: {stats.effective_attack_speed:.3f}")
    """

    def __init__(self, client: Client, character_code: int, level: int = 1) -> None:
        if not 1 <= level <= 20:
            raise ValueError(f"level은 1–20 사이여야 합니다. 입력값: {level}")
        self._client = client
        self._char_helper = CharacterHelper(client)
        self._item_helper = ItemHelper(client)
        self._character_code = character_code
        self._level = level
        self._weapon: dict[str, Any] | None = None
        self._armors: dict[str, dict[str, Any]] = {}  # armorType → item dict
        self._mastery_types: list[tuple[str, int]] = []  # (type, mastery_level)
        self._weapon_type_info: dict[str, float] | None = None  # weaponType → attackSpeed

    # ── 아이템 장착 ──────────────────────────────────────────

    def add_weapon(self, item_code: int) -> CharacterSimulator:
        """무기 장착. 이미 무기가 있으면 교체합니다."""
        item = self._item_helper.get(item_code)
        if not item:
            raise ValueError(f"아이템 코드 {item_code}를 찾을 수 없습니다.")
        if item.get("itemType") != "Weapon":
            raise ValueError(
                f"코드 {item_code}는 무기가 아닙니다 (itemType={item.get('itemType')})."
            )
        self._weapon = item
        return self

    def add_armor(self, item_code: int) -> CharacterSimulator:
        """방어구 장착. 같은 슬롯(Head/Chest/Arm/Leg)이면 교체합니다."""
        item = self._item_helper.get(item_code)
        if not item:
            raise ValueError(f"아이템 코드 {item_code}를 찾을 수 없습니다.")
        if item.get("itemType") != "Armor":
            raise ValueError(
                f"코드 {item_code}는 방어구가 아닙니다 (itemType={item.get('itemType')})."
            )
        slot = item.get("armorType", "Unknown")
        self._armors[slot] = item
        return self

    def set_mastery(self, *mastery_types: str, mastery_level: int = 1) -> CharacterSimulator:
        """숙련도 및 레벨 설정. 기존 숙련도를 교체합니다.

        보너스 = API 기본값 × mastery_level (Lv20 단검 공속 = 0.041 × 20 = 82%)

        Args:
            mastery_types: 숙련도 타입 (예: ``"OneHandSword"``, ``"Defense"``)
            mastery_level: 숙련도 레벨 (1–20, 기본 1)
        """
        if not 1 <= mastery_level <= 20:
            raise ValueError(f"mastery_level은 1–20 사이여야 합니다. 입력값: {mastery_level}")
        self._mastery_types = [(m, mastery_level) for m in mastery_types]
        return self

    def remove_weapon(self) -> CharacterSimulator:
        """무기 해제."""
        self._weapon = None
        return self

    def remove_armor(self, armor_type: str) -> CharacterSimulator:
        """방어구 슬롯 해제. armor_type: ``'Head'``, ``'Chest'``, ``'Arm'``, ``'Leg'``"""
        self._armors.pop(armor_type, None)
        return self

    def reset(self) -> CharacterSimulator:
        """모든 아이템 해제."""
        self._weapon = None
        self._armors.clear()
        return self

    def _load_weapon_type_info(self) -> dict[str, float]:
        if self._weapon_type_info is None:
            rows = self._client.meta.get_data("WeaponTypeInfo")
            self._weapon_type_info = {r["type"]: float(r.get("attackSpeed", 0)) for r in rows}
        return self._weapon_type_info

    # ── 스탯 계산 ────────────────────────────────────────────

    def get_stats(self) -> SimulatedStats:
        """현재 장착 상태를 반영한 최종 스탯을 반환합니다."""
        base = self._char_helper.stats_at_level(self._character_code, self._level)

        result = SimulatedStats(
            character_code=base.code,
            character_name=base.name,
            level=base.level,
            max_hp=base.max_hp,
            max_vp=base.max_vp,
            hp_regen=base.hp_regen,
            vp_regen=base.vp_regen,
            attack_power=base.attack_power,
            attack_speed=base.attack_speed,
            attack_speed_ratio=base.attack_speed_ratio,
            attack_speed_limit=base.attack_speed_limit,
            increase_basic_attack_damage_ratio=base.increase_basic_attack_damage_ratio,
            defense=base.defense,
            prevent_basic_attack_damaged_ratio=base.prevent_basic_attack_damaged_ratio,
            prevent_skill_damaged_ratio=base.prevent_skill_damaged_ratio,
            skill_amp=base.skill_amp,
            skill_amp_ratio=base.skill_amp_ratio,
            adaptive_force=base.adaptive_force,
            critical_strike_chance=base.critical_strike_chance,
            move_speed=base.move_speed,
            sight_range=base.sight_range,
            equipped_weapon=self._weapon,
            equipped_armors=list(self._armors.values()),
        )

        # 무기 타입 기본 공속 (WeaponTypeInfo)
        if self._weapon:
            weapon_type = self._weapon.get("weaponType", "")
            result.weapon_type_attack_speed = self._load_weapon_type_info().get(weapon_type, 0.0)

        for item in self._all_items():
            self._apply_item(result, item)

        # 숙련도는 무기 장착 시에만 적용
        if self._weapon:
            for m_type, m_level in self._mastery_types:
                bonus = self._char_helper.mastery_stat(self._character_code, m_type)
                if bonus is None:
                    bonus = self._char_helper.mastery_stat(0, m_type)
                if bonus:
                    self._apply_mastery(result, bonus, m_level)

        return result

    def _all_items(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        if self._weapon:
            items.append(self._weapon)
        items.extend(self._armors.values())
        return items

    def _apply_mastery(self, stats: SimulatedStats, bonus: MasteryStatBonus, level: int) -> None:
        for b in bonus.bonuses:
            snake = _MASTERY_STAT_MAP.get(b.name)
            if snake:
                setattr(stats, snake, getattr(stats, snake, 0.0) + b.value * level)

    def _apply_item(self, stats: SimulatedStats, item: dict[str, Any]) -> None:
        for item_field, lv_field, stat_field in _ITEM_STAT_MAP:
            val = float(item.get(item_field, 0))
            if lv_field:
                val += float(item.get(lv_field, 0)) * self._level
            if val:
                setattr(stats, stat_field, getattr(stats, stat_field, 0.0) + val)

    # ── 편의 메서드 ──────────────────────────────────────────

    def equipped(self) -> dict[str, dict[str, Any] | None]:
        """현재 장착 중인 아이템 목록."""
        return {
            "weapon": self._weapon,
            **{f"armor_{k.lower()}": v for k, v in self._armors.items()},
        }

    def __repr__(self) -> str:
        weapon_code = self._weapon["code"] if self._weapon else None
        armor_codes = {k: v["code"] for k, v in self._armors.items()}
        return (
            f"CharacterSimulator(character={self._character_code}, "
            f"level={self._level}, weapon={weapon_code}, armors={armor_codes})"
        )
