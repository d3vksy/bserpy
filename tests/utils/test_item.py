"""ItemHelper 단위 테스트."""

from __future__ import annotations

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.utils import ItemHelper

BASE = "https://open-api.bser.io"

_WEAPON_COMMON = {
    "code": 101104,
    "name": "칼",
    "itemType": "Weapon",
    "weaponType": "OneHandSword",
    "itemGrade": "Common",
    "isCompletedItem": False,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
    "attackPower": 4,
    "attackPowerByLv": 0,
    "defense": 0,
    "defenseByLv": 0,
    "maxHp": 0,
    "maxHpByLv": 0,
    "skillAmp": 0,
    "skillAmpByLevel": 0,
    "criticalStrikeChance": 0,
    "criticalStrikeDamage": 0,
    "cooldownReduction": 0,
    "lifeSteal": 0,
}
_WEAPON_UNCOMMON = {
    **_WEAPON_COMMON,
    "code": 101204,
    "itemGrade": "Uncommon",
    "makeMaterial1": 101104,  # 칼로 제작
    "makeMaterial2": 0,
    "attackPower": 12,
}
_WEAPON_LEGEND = {
    **_WEAPON_COMMON,
    "code": 101405,
    "itemGrade": "Legend",
    "isCompletedItem": True,
    "makeMaterial1": 101204,
    "makeMaterial2": 0,
    "attackPower": 73,
}
_ARMOR_HEAD = {
    "code": 201501,
    "name": "머리",
    "itemType": "Armor",
    "armorType": "Head",
    "itemGrade": "Legend",
    "isCompletedItem": True,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
    "defense": 15,
    "maxHp": 0,
}
_CONSUMABLE = {
    "code": 302102,
    "name": "닭",
    "itemType": "Consume",
    "consumableType": "Food",
    "itemGrade": "Common",
    "isCompletedItem": False,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
    "hpRecover": 300,
    "heal": 0,
}
_SPECIAL = {
    "code": 502207,
    "name": "카메라",
    "itemType": "Special",
    "specialItemType": "Summon",
    "itemGrade": "Uncommon",
    "isCompletedItem": True,
    "makeMaterial1": 0,
    "makeMaterial2": 0,
}


def _mock_all(respx_mock: respx.MockRouter | None = None) -> None:
    respx.get(f"{BASE}/v2/data/ItemWeapon").mock(
        return_value=httpx.Response(
            200, json={"code": 200, "data": [_WEAPON_COMMON, _WEAPON_UNCOMMON, _WEAPON_LEGEND]}
        )
    )
    respx.get(f"{BASE}/v2/data/ItemArmor").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_ARMOR_HEAD]})
    )
    respx.get(f"{BASE}/v2/data/ItemConsumable").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_CONSUMABLE]})
    )
    respx.get(f"{BASE}/v2/data/ItemSpecial").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [_SPECIAL]})
    )


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_get_by_code(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    assert h.get(101104) is not None
    assert h.get(101104)["itemType"] == "Weapon"
    assert h.get(201501) is not None
    assert h.get(201501)["armorType"] == "Head"
    assert h.get(999999) is None


@respx.mock
def test_get_weapons_filter(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    all_w = h.get_weapons()
    assert len(all_w) == 3

    legend = h.get_weapons(grade="Legend")
    assert len(legend) == 1
    assert legend[0]["code"] == 101405

    completed = h.get_weapons(completed_only=True)
    assert all(w["isCompletedItem"] for w in completed)

    osh = h.get_weapons(weapon_type="OneHandSword", grade="Common")
    assert len(osh) == 1
    assert osh[0]["code"] == 101104


@respx.mock
def test_get_armors_filter(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    assert len(h.get_armors()) == 1
    assert len(h.get_armors(armor_type="Head")) == 1
    assert len(h.get_armors(armor_type="Chest")) == 0
    assert len(h.get_armors(grade="Legend", completed_only=True)) == 1


@respx.mock
def test_get_consumables(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    assert len(h.get_consumables()) == 1
    assert len(h.get_consumables(consumable_type="Food")) == 1
    assert len(h.get_consumables(consumable_type="Drink")) == 0


@respx.mock
def test_craftable_from(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    # 101104(칼)로 만들 수 있는 아이템
    results = h.craftable_from(101104)
    codes = [r["code"] for r in results]
    assert 101204 in codes  # Uncommon이 칼을 재료로 씀

    # 존재하지 않는 재료
    assert h.craftable_from(999999) == []


@respx.mock
def test_recipe(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    # Uncommon = Common + nothing
    assert h.recipe(101204) == (101104, 0)
    # Common = 재료 없음 → None
    assert h.recipe(101104) is None
    # 없는 아이템
    assert h.recipe(999999) is None


@respx.mock
def test_craft_tree(client: Client) -> None:
    _mock_all()
    h = ItemHelper(client)

    # Legend → Uncommon → Common(101104, 기본 재료)
    tree = h.craft_tree(101405)
    assert 101104 in tree

    # 기본 재료는 자기 자신
    base_tree = h.craft_tree(101104)
    assert base_tree == [101104]


@respx.mock
def test_craft_tree_cycle_safe(client: Client) -> None:
    """순환 참조가 있어도 무한 루프에 빠지지 않아야 한다."""
    # 순환: A → B → A
    cycle_a = {**_WEAPON_COMMON, "code": 9001, "makeMaterial1": 9002, "makeMaterial2": 0}
    cycle_b = {**_WEAPON_COMMON, "code": 9002, "makeMaterial1": 9001, "makeMaterial2": 0}
    respx.get(f"{BASE}/v2/data/ItemWeapon").mock(
        return_value=httpx.Response(200, json={"code": 200, "data": [cycle_a, cycle_b]})
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

    h = ItemHelper(client)
    result = h.craft_tree(9001)  # 순환이어도 종료되어야 함
    assert isinstance(result, list)
