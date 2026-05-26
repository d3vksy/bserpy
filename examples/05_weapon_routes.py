"""
예제 05 — 추천 무기 루트

추천 무기 루트 목록을 가져와서 캐릭터별로 정리합니다.
"""

from collections import defaultdict

from bserpy import Client

API_KEY = "YOUR_API_KEY_HERE"


def main() -> None:
    with Client(api_key=API_KEY) as client:
        # l10n으로 캐릭터 이름 먼저 로드
        l10n = client.meta.get_l10n_parsed("Korean")

        # 추천 루트 전체 (최대 100개)
        bundles = client.meta.get_weapon_routes()

    print(f"총 {len(bundles)}개 루트 로드\n")

    # 캐릭터별 그룹화
    by_char: dict[int, list] = defaultdict(list)
    for b in bundles:
        by_char[b.route.character_code].append(b)

    for char_code, char_bundles in sorted(by_char.items()):
        char_name = l10n.get_character_name(char_code) or f"코드{char_code}"
        print(f"[{char_name}]  ({len(char_bundles)}개 루트)")
        for b in char_bundles[:2]:  # 캐릭터당 최대 2개 출력
            route = b.route
            desc = b.desc
            print(f"  루트명: {route.title}")
            print(f"  작성자: {route.user_nickname}")
            print(f"  무기 코드: {route.weapon_codes}")
            print(f"  경로: {route.paths}")
            print(f"  스킬 순서: {desc.skill_path}")
            print()


if __name__ == "__main__":
    main()
