"""CharacterSimulator 단위 테스트."""

from __future__ import annotations

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.utils import CharacterSimulator

BASE = "https://open-api.bser.io"

_CHAR_ROW = {
    "code": 1,
    "name": "Jackie",
    "maxHp": 940,
    "maxVp": 0,
    "attackPower": 36,
    "defense": 50,
    "skillAmp": 0,
    "adaptiveForce": 0,
    "criticalStrikeChance": 0,
    "hpRegen": 1.28,
    "vpRegen": 0,
    "attackSpeed": 0.1,
    "attackSpeedRatio": 0,
    "attackSpeedLimit": 2.5,
    "increaseBasicAttackDamageRatio": 0,
    "skillAmpRatio": 0,
    "preventBasicAttackDamagedRatio": 0,
    "preventSkillDamagedRatio": 0,
    "moveSpeed": 3.5,
    "sightRange": 8.5,
}
_LEVELUP_ROW = {
    "code": 1,
    "name": "Jackie",
    "maxHp": 95,
    "maxVp": 0,
    "attackPower": 4.7,
    "defense": 3.0,
    "skillAmp": 0,
    "adaptiveForce": 0,
    "criticalChance": 0,
    "hpRegen": 0.077,
    "vpRegen": 0,
    "attackSpeed": 0,
    "moveSpeed": 0,
    "attackSpeedRatio": 0,
    "increaseBasicAttackDamageRatio": 0,
    "skillAmpRatio": 0,
    "preventBasicAttackDamagedRatio": 0,
    "preventSkillDamagedRatio": 0,
}
_WEAPON = {
    "code": 101405,
    "itemType": "Weapon",
    "weaponType": "OneHandSword",
    "itemGrade": "Legend",
    "isCompletedItem": True,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
    "attackPower": 73,
    "attackPowerByLv": 0,
    "defense": 0,
    "defenseByLv": 0,
    "maxHp": 0,
    "maxHpByLv": 0,
    "skillAmp": 0,
    "skillAmpByLevel": 0,
    "skillAmpRatio": 0,
    "skillAmpRatioByLevel": 0,
    "adaptiveForce": 0,
    "adaptiveForceByLevel": 0,
    "attackSpeedRatio": 0,
    "attackSpeedRatioByLv": 0,
    "criticalStrikeChance": 0.2,
    "criticalStrikeDamage": 0,
    "cooldownReduction": 0,
    "cooldownLimit": 0,
    "lifeSteal": 0.1,
    "normalLifeSteal": 0,
    "skillLifeSteal": 0,
    "moveSpeed": 0,
    "moveSpeedRatio": 0,
    "moveSpeedOutOfCombat": 0,
    "hpRegen": 0,
    "hpRegenRatio": 0,
    "sightRange": 0,
    "attackRange": 0,
    "increaseBasicAttackDamage": 0,
    "increaseBasicAttackDamageByLv": 0,
    "increaseBasicAttackDamageRatio": 0,
    "increaseBasicAttackDamageRatioByLv": 0,
    "preventBasicAttackDamaged": 0,
    "preventBasicAttackDamagedByLv": 0,
    "preventBasicAttackDamagedRatio": 0,
    "preventBasicAttackDamagedRatioByLv": 0,
    "preventSkillDamaged": 0,
    "preventSkillDamagedByLv": 0,
    "preventSkillDamagedRatio": 0,
    "preventSkillDamagedRatioByLv": 0,
    "penetrationDefense": 0,
    "penetrationDefenseRatio": 0,
    "trapDamageReduce": 0,
    "trapDamageReduceRatio": 0,
    "slowResistRatio": 0,
    "hpHealedIncreaseRatio": 0,
    "healerGiveHpHealRatio": 0,
    "uniqueAttackRange": 0,
    "uniqueHpHealedIncreaseRatio": 0,
    "uniqueCooldownLimit": 0,
    "uniqueTenacity": 0,
    "uniqueMoveSpeed": 0,
    "uniquePenetrationDefense": 0,
    "uniquePenetrationDefenseRatio": 0,
    "uniqueLifeSteal": 0,
    "uniqueSkillAmpRatio": 0,
    "ultCooldownReduction": 0,
    "weaponCooldownReduction": 0,
    "tacticalCooldownReduction": 0,
    "preventCriticalStrikeDamaged": 0,
}
_ARMOR = {
    "code": 201501,
    "itemType": "Armor",
    "armorType": "Head",
    "itemGrade": "Legend",
    "isCompletedItem": True,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
    "defense": 15,
    "defenseByLv": 0,
    "attackPower": 0,
    "attackPowerByLv": 0,
    "maxHp": 300,
    "maxHpByLv": 0,
    "skillAmp": 0,
    "skillAmpByLevel": 0,
    "skillAmpRatio": 0,
    "skillAmpRatioByLevel": 0,
    "adaptiveForce": 0,
    "adaptiveForceByLevel": 0,
    "attackSpeedRatio": 0,
    "attackSpeedRatioByLv": 0,
    "criticalStrikeChance": 0,
    "criticalStrikeDamage": 0,
    "cooldownReduction": 0,
    "cooldownLimit": 0,
    "lifeSteal": 0,
    "normalLifeSteal": 0,
    "skillLifeSteal": 0,
    "moveSpeed": 0,
    "moveSpeedRatio": 0,
    "moveSpeedOutOfCombat": 0,
    "hpRegen": 0,
    "hpRegenRatio": 0,
    "sightRange": 0,
    "attackRange": 0,
    "increaseBasicAttackDamage": 0,
    "increaseBasicAttackDamageByLv": 0,
    "increaseBasicAttackDamageRatio": 0,
    "increaseBasicAttackDamageRatioByLv": 0,
    "preventBasicAttackDamaged": 0,
    "preventBasicAttackDamagedByLv": 0,
    "preventBasicAttackDamagedRatio": 0,
    "preventBasicAttackDamagedRatioByLv": 0,
    "preventSkillDamaged": 0,
    "preventSkillDamagedByLv": 0,
    "preventSkillDamagedRatio": 0,
    "preventSkillDamagedRatioByLv": 0,
    "penetrationDefense": 0,
    "penetrationDefenseRatio": 0,
    "trapDamageReduce": 0,
    "trapDamageReduceRatio": 0,
    "slowResistRatio": 0,
    "hpHealedIncreaseRatio": 0,
    "healerGiveHpHealRatio": 0,
    "uniqueAttackRange": 0,
    "uniqueHpHealedIncreaseRatio": 0,
    "uniqueCooldownLimit": 0,
    "uniqueTenacity": 0,
    "uniqueMoveSpeed": 0,
    "uniquePenetrationDefense": 0,
    "uniquePenetrationDefenseRatio": 0,
    "uniqueLifeSteal": 0,
    "uniqueSkillAmpRatio": 0,
    "ultCooldownReduction": 0,
    "weaponCooldownReduction": 0,
    "tacticalCooldownReduction": 0,
    "preventCriticalStrikeDamaged": 0,
}


def _mock_char_tables() -> None:
    respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    respx.get(f"{BASE}/v2/data/CharacterLevelUpStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_LEVELUP_ROW]})
    )


def _mock_item_tables() -> None:
    respx.get(f"{BASE}/v2/data/ItemWeapon").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_WEAPON]})
    )
    respx.get(f"{BASE}/v2/data/ItemArmor").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_ARMOR]})
    )
    respx.get(f"{BASE}/v2/data/ItemConsumable").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": []})
    )
    respx.get(f"{BASE}/v2/data/ItemSpecial").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": []})
    )


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_naked_stats(client: Client) -> None:
    _mock_char_tables()
    stats = CharacterSimulator(client, character_code=1, level=1).get_stats()

    assert stats.max_hp == pytest.approx(940.0)
    assert stats.attack_power == pytest.approx(36.0)
    assert stats.defense == pytest.approx(50.0)
    assert stats.equipped_weapon is None
    assert stats.equipped_armors == []


@respx.mock
def test_add_weapon_increases_atk(client: Client) -> None:
    _mock_char_tables()
    _mock_item_tables()
    sim = CharacterSimulator(client, character_code=1, level=1)
    sim.add_weapon(101405)
    stats = sim.get_stats()

    assert stats.attack_power == pytest.approx(36 + 73)
    assert stats.critical_strike_chance == pytest.approx(0.2)
    assert stats.life_steal == pytest.approx(0.1)
    assert stats.equipped_weapon is not None
    assert stats.equipped_weapon["code"] == 101405


@respx.mock
def test_add_armor_increases_def_hp(client: Client) -> None:
    _mock_char_tables()
    _mock_item_tables()
    sim = CharacterSimulator(client, character_code=1, level=1)
    sim.add_armor(201501)
    stats = sim.get_stats()

    assert stats.defense == pytest.approx(50 + 15)
    assert stats.max_hp == pytest.approx(940 + 300)
    assert len(stats.equipped_armors) == 1


@respx.mock
def test_method_chaining(client: Client) -> None:
    _mock_char_tables()
    _mock_item_tables()
    stats = (
        CharacterSimulator(client, character_code=1, level=1)
        .add_weapon(101405)
        .add_armor(201501)
        .get_stats()
    )
    assert stats.attack_power == pytest.approx(36 + 73)
    assert stats.defense == pytest.approx(50 + 15)
    assert stats.max_hp == pytest.approx(940 + 300)


@respx.mock
def test_armor_slot_replaced(client: Client) -> None:
    """같은 슬롯 방어구는 교체되어야 한다."""
    _mock_char_tables()
    _mock_item_tables()
    sim = CharacterSimulator(client, character_code=1, level=1)
    sim.add_armor(201501)  # Head
    sim.add_armor(201501)  # 같은 Head 다시 추가
    stats = sim.get_stats()

    # 두 번 적용되면 안 됨
    assert stats.defense == pytest.approx(50 + 15)
    assert len(stats.equipped_armors) == 1


@respx.mock
def test_reset_clears_items(client: Client) -> None:
    _mock_char_tables()
    _mock_item_tables()
    sim = CharacterSimulator(client, character_code=1, level=1)
    sim.add_weapon(101405).add_armor(201501)
    sim.reset()
    stats = sim.get_stats()

    assert stats.attack_power == pytest.approx(36.0)
    assert stats.equipped_weapon is None
    assert stats.equipped_armors == []


@respx.mock
def test_effective_attack_speed_capped(client: Client) -> None:
    """공격 속도가 상한을 넘으면 클리핑되어야 한다."""
    # 공속비율이 매우 높은 무기 생성
    fast_weapon = {**_WEAPON, "attackSpeedRatio": 100.0}  # 말도 안 되게 높음
    respx.get(f"{BASE}/v2/data/ItemWeapon").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [fast_weapon]})
    )
    respx.get(f"{BASE}/v2/data/ItemArmor").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": []})
    )
    respx.get(f"{BASE}/v2/data/ItemConsumable").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": []})
    )
    respx.get(f"{BASE}/v2/data/ItemSpecial").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": []})
    )
    _mock_char_tables()

    sim = CharacterSimulator(client, character_code=1, level=1)
    sim.add_weapon(101405)
    stats = sim.get_stats()

    assert stats.effective_attack_speed <= stats.attack_speed_limit


def test_invalid_level(client: Client) -> None:
    with pytest.raises(ValueError, match="1–20"):
        CharacterSimulator(client, character_code=1, level=0)


@respx.mock
def test_wrong_item_type_raises(client: Client) -> None:
    _mock_char_tables()
    _mock_item_tables()
    sim = CharacterSimulator(client, character_code=1, level=1)

    with pytest.raises(ValueError, match="무기가 아닙니다"):
        sim.add_weapon(201501)  # 방어구를 무기 슬롯에 넣으면 에러

    with pytest.raises(ValueError, match="방어구가 아닙니다"):
        sim.add_armor(101405)  # 무기를 방어구 슬롯에 넣으면 에러
