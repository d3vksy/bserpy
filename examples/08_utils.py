"""
예제 08 — utils 헬퍼 사용

CharacterHelper: 캐릭터 레벨별 스탯 계산
ItemHelper: 아이템 검색 및 제작 트리
SeasonHelper: 시즌 정보 조회
CharacterSimulator: 아이템 장착 스탯 시뮬레이션
"""

from bserpy import Client, CharacterHelper, CharacterSimulator, ItemHelper, SeasonHelper

API_KEY = "YOUR_API_KEY_HERE"
CHARACTER_CODE = 1   # Jackie


def main() -> None:
    with Client(api_key=API_KEY) as client:
        l10n = client.meta.get_l10n_parsed("Korean")

        # ── CharacterHelper ────────────────────────────────────
        print("=== 캐릭터 스탯 ===")
        chars = CharacterHelper(client)

        base = chars.base_stats(CHARACTER_CODE)
        lv20 = chars.stats_at_level(CHARACTER_CODE, level=20)
        mastery = chars.mastery_options(CHARACTER_CODE)

        char_name = l10n.get_character_name(CHARACTER_CODE) or base.name
        print(f"[{char_name}]")
        print(f"  레벨 1  HP:{base.max_hp:>7.1f}  공격력:{base.attack_power:>6.1f}  방어:{base.defense:>5.1f}")
        print(f"  레벨 20 HP:{lv20.max_hp:>7.1f}  공격력:{lv20.attack_power:>6.1f}  방어:{lv20.defense:>5.1f}")
        print(f"  사용 가능 무기: {mastery.weapon_types}")
        print(f"  전투 마스터리: {mastery.combat_types}")
        print(f"  생존 마스터리: {mastery.survival_types}")

        # ── ItemHelper ─────────────────────────────────────────
        print("\n=== 아이템 검색 ===")
        items = ItemHelper(client)

        # 전설 등급 완성 무기
        legend_weapons = items.get_weapons(grade="Legend", completed_only=True)
        print(f"전설 완성 무기 ({len(legend_weapons)}개):")
        for w in legend_weapons[:3]:
            print(f"  [{w['code']}] weaponType={w['weaponType']}  "
                  f"ATK={w['attackPower']}  AS={w['attackSpeedRatio']}")

        # 특정 아이템 제작 트리
        if legend_weapons:
            target = legend_weapons[0]
            tree = items.craft_tree(target["code"])
            print(f"\n코드 {target['code']} 제작에 필요한 기본 재료: {tree}")

        # ── SeasonHelper ───────────────────────────────────────
        print("\n=== 시즌 정보 ===")
        seasons = SeasonHelper(client)

        current = seasons.current_season()
        if current:
            print(f"현재 시즌: {current['seasonName']} (ID:{current['seasonID']})")
            print(f"  기간: {current.get('seasonStart', 'N/A')} ~ {current.get('seasonEnd', 'N/A')}")

        all_s = seasons.all_seasons()
        print(f"전체 시즌 수: {len(all_s)}")


def simulation_demo(client: Client) -> None:
    items = ItemHelper(client)
    legend_weapon = items.get_weapons(grade="Legend", completed_only=True)[0]
    legend_armors = items.get_armors(grade="Legend", completed_only=True)

    # 슬롯별로 하나씩 고르기
    by_slot: dict[str, dict] = {}
    for a in legend_armors:
        slot = a.get("armorType", "")
        if slot and slot not in by_slot:
            by_slot[slot] = a

    print("\n=== 스탯 시뮬레이션 ===")
    sim = CharacterSimulator(client, character_code=CHARACTER_CODE, level=20)
    naked = sim.get_stats()

    sim.add_weapon(legend_weapon["code"])
    for armor in by_slot.values():
        sim.add_armor(armor["code"])
    geared = sim.get_stats()

    headers = ["항목", "아이템 없음", "풀 세팅"]
    rows = [
        ("체력",        f"{naked.max_hp:.0f}",      f"{geared.max_hp:.0f}"),
        ("공격력",      f"{naked.attack_power:.1f}", f"{geared.attack_power:.1f}"),
        ("방어",        f"{naked.defense:.1f}",      f"{geared.defense:.1f}"),
        ("공격 속도",   f"{naked.effective_attack_speed:.3f}", f"{geared.effective_attack_speed:.3f}"),
        ("스킬증폭(%)", f"{naked.skill_amp_ratio:.3f}", f"{geared.skill_amp_ratio:.3f}"),
        ("치명타",      f"{naked.critical_strike_chance:.3f}", f"{geared.critical_strike_chance:.3f}"),
        ("쿨다운감소",  f"{naked.cooldown_reduction:.3f}", f"{geared.cooldown_reduction:.3f}"),
        ("흡혈",        f"{naked.life_steal:.3f}",   f"{geared.life_steal:.3f}"),
    ]
    col = [max(len(h), max(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    fmt = "  ".join(f"{{:<{c}}}" for c in col)
    print(fmt.format(*headers))
    print("-" * (sum(col) + 4))
    for row in rows:
        print(fmt.format(*row))

    slots = ["weapon"] + [f"armor_{k.lower()}" for k in by_slot]
    print(f"\n장착: {slots}")


if __name__ == "__main__":
    main()
