"""CharacterHelper 단위 테스트."""
from __future__ import annotations

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.utils import CharacterHelper

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
    "charArcheType1": "Warrior",
    "charArcheType2": "None",
    "weaponRangeType": "Melee",
    "strLearnStartSkill": "Passive,Attack,SpecialSkill",
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

_MASTERY_OPTS_ROW = {
    "code": 1,
    "weapon1": "OneHandSword",
    "weapon2": "TwoHandSword",
    "weapon3": "Axe",
    "weapon4": "DualSword",
    "combat1": "Defense",
    "combat2": "Hunt",
    "survival1": "Craft",
    "survival2": "Search",
    "survival3": "Move",
}

_MASTERY_STAT_ROW = {
    "code": 10701,
    "type": "OneHandSword",
    "characterCode": 1,
    "firstOption": "AttackSpeedRatio",
    "firstOptionSection1Value": 0.041,
    "firstOptionSection2Value": 0.041,
    "firstOptionSection3Value": 0.041,
    "firstOptionSection4Value": 0.041,
    "secondOption": "IncreaseBasicAttackDamageRatio",
    "secondOptionSection1Value": 0.03,
    "secondOptionSection2Value": 0.03,
    "secondOptionSection3Value": 0.03,
    "secondOptionSection4Value": 0.03,
    "thirdOption": "None",
    "thirdOptionSection1Value": 0,
    "thirdOptionSection2Value": 0,
    "thirdOptionSection3Value": 0,
    "thirdOptionSection4Value": 0,
}


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_base_stats(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    h = CharacterHelper(client)
    s = h.base_stats(1)

    assert s.code == 1
    assert s.name == "Jackie"
    assert s.level == 1
    assert s.max_hp == 940.0
    assert s.attack_power == 36.0
    assert s.defense == 50.0
    assert s.attack_speed == 0.1
    assert s.attack_speed_limit == 2.5
    assert s.move_speed == 3.5
    assert s.sight_range == 8.5


@respx.mock
def test_stats_at_level_1_equals_base(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    respx.get(f"{BASE}/v2/data/CharacterLevelUpStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_LEVELUP_ROW]})
    )
    h = CharacterHelper(client)
    lv1 = h.stats_at_level(1, level=1)

    assert lv1.max_hp == 940.0
    assert lv1.attack_power == 36.0
    assert lv1.defense == 50.0


@respx.mock
def test_stats_at_level_20(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    respx.get(f"{BASE}/v2/data/CharacterLevelUpStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_LEVELUP_ROW]})
    )
    h = CharacterHelper(client)
    lv20 = h.stats_at_level(1, level=20)

    # base + growth * 19
    assert lv20.max_hp == pytest.approx(940 + 95 * 19)
    assert lv20.attack_power == pytest.approx(36 + 4.7 * 19)
    assert lv20.defense == pytest.approx(50 + 3.0 * 19)
    # 레벨 무관 필드
    assert lv20.attack_speed_limit == 2.5
    assert lv20.sight_range == 8.5


def test_stats_at_level_invalid(client: Client) -> None:
    h = CharacterHelper(client)
    with pytest.raises(ValueError, match="1–20"):
        h.stats_at_level(1, level=0)
    with pytest.raises(ValueError):
        h.stats_at_level(1, level=21)


@respx.mock
def test_level_up_stat(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/CharacterLevelUpStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_LEVELUP_ROW]})
    )
    h = CharacterHelper(client)
    growth = h.level_up_stat(1)

    assert growth.level == 0
    assert growth.max_hp == 95.0
    assert growth.attack_power == pytest.approx(4.7)
    assert growth.hp_regen == pytest.approx(0.077)


@respx.mock
def test_info(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    h = CharacterHelper(client)
    info = h.info(1)

    assert info.char_arche_type1 == "Warrior"
    assert info.char_arche_type2 == "None"
    assert info.weapon_range_type == "Melee"
    assert info.start_skills == ["Passive", "Attack", "SpecialSkill"]


@respx.mock
def test_mastery_options(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/CharacterMastery").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_MASTERY_OPTS_ROW]})
    )
    h = CharacterHelper(client)
    opts = h.mastery_options(1)

    assert opts.weapon_types == ["OneHandSword", "TwoHandSword", "Axe", "DualSword"]
    assert opts.combat_types == ["Defense", "Hunt"]
    assert opts.survival_types == ["Craft", "Search", "Move"]


@respx.mock
def test_mastery_stat(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/MasteryStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_MASTERY_STAT_ROW]})
    )
    h = CharacterHelper(client)
    bonus = h.mastery_stat(1, "OneHandSword")

    assert bonus is not None
    assert bonus.first_option == "AttackSpeedRatio"
    assert bonus.first_value() == pytest.approx(0.041)
    assert bonus.second_option == "IncreaseBasicAttackDamageRatio"
    assert bonus.second_value() == pytest.approx(0.03)


@respx.mock
def test_mastery_stat_not_found(client: Client) -> None:
    respx.get(f"{BASE}/v2/data/MasteryStat").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_MASTERY_STAT_ROW]})
    )
    h = CharacterHelper(client)
    assert h.mastery_stat(1, "Hammer") is None


@respx.mock
def test_data_cached_on_second_call(client: Client) -> None:
    route = respx.get(f"{BASE}/v2/data/Character").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CHAR_ROW]})
    )
    h = CharacterHelper(client)
    h.base_stats(1)
    h.base_stats(1)
    assert route.call_count == 1  # 두 번 호출해도 API 요청은 한 번
