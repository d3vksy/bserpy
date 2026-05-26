"""
예제 04 — 현지화 데이터(l10n) & 게임 메타 데이터

l10n: 캐릭터명, 지역명, 몬스터명 등 인게임 텍스트 조회
meta: 캐릭터 기본 스탯, 아이템 정보 등 게임 데이터 테이블 조회
"""

from bserpy import Client

API_KEY = "YOUR_API_KEY_HERE"


def main() -> None:
    with Client(api_key=API_KEY) as client:
        # ── l10n ──────────────────────────────────────────
        print("=== l10n 로딩 중... ===")
        l10n = client.meta.get_l10n_parsed("Korean")
        print(f"총 {len(l10n)}개 키 로드 완료\n")

        # 캐릭터 이름 (코드 1~5)
        print("[캐릭터 이름]")
        for code in range(1, 6):
            name = l10n.get_character_name(code)
            print(f"  {code}: {name}")

        # 주요 지역
        print("\n[지역 이름]")
        areas = ["Harbor", "Hospital", "School", "Forest", "Archery"]
        for area in areas:
            name = l10n.get_area_name(area)
            print(f"  {area}: {name}")

        # 몬스터
        print("\n[몬스터 이름]")
        for code in range(1, 6):
            name = l10n.get_monster_name(code)
            print(f"  {code}: {name}")

        # ── 메타 데이터 ───────────────────────────────────
        print("\n=== 게임 메타 데이터 ===")

        # 현재 시즌 확인
        seasons = client.meta.get_data("Season")
        current = next((s for s in seasons if s.get("isCurrent") == 1), None)
        if current:
            print(f"현재 시즌: {current['seasonName']} (ID: {current['seasonID']})")

        # 사용 가능한 모든 테이블 목록
        table_hash = client.meta.get_hash()
        print(f"\n사용 가능한 데이터 테이블 ({len(table_hash)}개):")
        for name in sorted(table_hash.keys()):
            print(f"  {name}")


if __name__ == "__main__":
    main()
