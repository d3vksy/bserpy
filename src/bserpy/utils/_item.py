from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bserpy._client import Client


class ItemHelper:
    """Helper for item lookups across all item types (Weapon, Armor, Consumable, Special).

    Lazy-loads each item table on first access.

    Example::

        with Client(api_key="...") as client:
            items = ItemHelper(client)
            sword = items.get(101104)
            ep_weapons = items.get_weapons(grade="Epic", completed_only=True)
            mats = items.craftable_from(101104)
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._weapons: list[dict[str, Any]] | None = None
        self._armors: list[dict[str, Any]] | None = None
        self._consumables: list[dict[str, Any]] | None = None
        self._specials: list[dict[str, Any]] | None = None
        self._index: dict[int, dict[str, Any]] | None = None

    def _load_weapons(self) -> None:
        if self._weapons is None:
            self._weapons = self._client.meta.get_data("ItemWeapon")

    def _load_armors(self) -> None:
        if self._armors is None:
            self._armors = self._client.meta.get_data("ItemArmor")

    def _load_consumables(self) -> None:
        if self._consumables is None:
            self._consumables = self._client.meta.get_data("ItemConsumable")

    def _load_specials(self) -> None:
        if self._specials is None:
            self._specials = self._client.meta.get_data("ItemSpecial")

    def _load_all(self) -> None:
        self._load_weapons()
        self._load_armors()
        self._load_consumables()
        self._load_specials()
        if self._index is None:
            self._index = {}
            for table in (self._weapons, self._armors, self._consumables, self._specials):
                assert table is not None
                for item in table:
                    self._index[item["code"]] = item

    def get(self, code: int) -> dict[str, Any] | None:
        """Find any item by code across all item types. Returns None if not found."""
        self._load_all()
        assert self._index is not None
        return self._index.get(code)

    def get_weapons(
        self,
        *,
        weapon_type: str | None = None,
        grade: str | None = None,
        completed_only: bool = False,
    ) -> list[dict[str, Any]]:
        """Filter weapon items.

        Args:
            weapon_type: e.g. ``"OneHandSword"``, ``"Bow"``, ``"Glove"``
            grade: ``"Common"``, ``"Uncommon"``, ``"Rare"``, ``"Epic"``, ``"Legend"``
            completed_only: only fully crafted (end-tier) weapons
        """
        self._load_weapons()
        assert self._weapons is not None
        result: list[dict[str, Any]] = self._weapons
        if weapon_type:
            result = [i for i in result if i.get("weaponType") == weapon_type]
        if grade:
            result = [i for i in result if i.get("itemGrade") == grade]
        if completed_only:
            result = [i for i in result if i.get("isCompletedItem")]
        return result

    def get_armors(
        self,
        *,
        armor_type: str | None = None,
        grade: str | None = None,
        completed_only: bool = False,
    ) -> list[dict[str, Any]]:
        """Filter armor items.

        Args:
            armor_type: ``"Head"``, ``"Chest"``, ``"Arm"``, ``"Leg"``
            grade: ``"Common"``, ``"Uncommon"``, ``"Rare"``, ``"Epic"``, ``"Legend"``
            completed_only: only fully crafted (end-tier) armors
        """
        self._load_armors()
        assert self._armors is not None
        result: list[dict[str, Any]] = self._armors
        if armor_type:
            result = [i for i in result if i.get("armorType") == armor_type]
        if grade:
            result = [i for i in result if i.get("itemGrade") == grade]
        if completed_only:
            result = [i for i in result if i.get("isCompletedItem")]
        return result

    def get_consumables(self, *, consumable_type: str | None = None) -> list[dict[str, Any]]:
        """Filter consumable items.

        Args:
            consumable_type: ``"Food"``, ``"Drink"``, etc.
        """
        self._load_consumables()
        assert self._consumables is not None
        if consumable_type:
            return [i for i in self._consumables if i.get("consumableType") == consumable_type]
        return list(self._consumables)

    def get_specials(self) -> list[dict[str, Any]]:
        """Return all special items."""
        self._load_specials()
        assert self._specials is not None
        return list(self._specials)

    def craftable_from(self, material_code: int) -> list[dict[str, Any]]:
        """Return all items craftable using ``material_code`` as either material."""
        self._load_all()
        assert self._index is not None
        return [
            item
            for item in self._index.values()
            if material_code in (item.get("makeMaterial1", 0), item.get("makeMaterial2", 0))
        ]

    def recipe(self, item_code: int) -> tuple[int, int] | None:
        """Return ``(material1_code, material2_code)`` for an item, or ``None`` if not craftable."""
        self._load_all()
        assert self._index is not None
        item = self._index.get(item_code)
        if not item:
            return None
        m1 = item.get("makeMaterial1", 0)
        m2 = item.get("makeMaterial2", 0)
        if m1 == 0 and m2 == 0:
            return None
        return (m1, m2)

    def craft_tree(self, item_code: int) -> list[int]:
        """Return flat list of all base material codes needed to craft an item recursively.

        Returns only uncraftable (base) material codes.
        Cycle-safe: if a circular recipe is detected the branch is skipped.
        """
        self._load_all()
        result: list[int] = []
        self._recurse(item_code, result, set())
        return result

    def _recurse(self, code: int, acc: list[int], seen: set[int]) -> None:
        if code in seen:
            return  # 순환 참조 방지
        seen.add(code)
        assert self._index is not None
        item = self._index.get(code)
        if not item:
            return
        m1 = item.get("makeMaterial1", 0)
        m2 = item.get("makeMaterial2", 0)
        if m1 == 0 and m2 == 0:
            acc.append(code)
            return
        if m1:
            self._recurse(m1, acc, seen)
        if m2:
            self._recurse(m2, acc, seen)
