"""
예제 02 — 랭킹 조회

글로벌 TOP 10과 서버별 TOP 10을 조회합니다.
"""

from bserpy import Client
from bserpy.models import RegionServer

API_KEY = "YOUR_API_KEY_HERE"
SEASON_ID = 39


def main() -> None:
    with Client(api_key=API_KEY) as client:
        # 글로벌 TOP 10
        top = client.ranking.get_top(season_id=SEASON_ID)
        print("=== 글로벌 TOP 10 ===")
        for r in top[:10]:
            print(f"  {r.rank:>3}위  {r.nickname:<20}  MMR: {r.mmr}")

        # 아시아 서버 TOP 10
        asia_top = client.ranking.get_top_by_server(
            season_id=SEASON_ID,
            server=RegionServer.ASIA,
        )
        print("\n=== 아시아 서버 TOP 10 ===")
        for r in asia_top[:10]:
            print(f"  {r.rank:>3}위  {r.nickname:<20}  MMR: {r.mmr}")


if __name__ == "__main__":
    main()
