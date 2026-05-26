"""
예제 07 — 비동기(async) 사용

AsyncClient를 사용해서 여러 플레이어의 정보를 동시에 조회합니다.
"""

import asyncio

from bserpy import AsyncClient, NotFoundError

API_KEY = "YOUR_API_KEY_HERE"
SEASON_ID = 39
NICKNAMES = ["oracle1", "Masuhana", "Daehu"]


async def fetch_user_summary(client: AsyncClient, nickname: str) -> None:
    """단일 플레이어 요약 정보 비동기 조회."""
    try:
        user = await client.users.get_uid(nickname)
    except NotFoundError:
        print(f"  [{nickname}] 찾을 수 없음")
        return

    rank = await client.users.get_rank(user.user_id, season_id=SEASON_ID)
    stats_list = await client.users.get_stats(user.user_id, season_id=SEASON_ID, mode=3)

    stats = stats_list[0] if stats_list else None
    win_rate = f"{stats.total_wins / stats.total_games * 100:.1f}%" if stats and stats.total_games else "N/A"

    print(
        f"  {nickname:<20}  {rank.rank:>4}위  MMR:{rank.mmr:>5}  "
        f"게임:{stats.total_games if stats else 'N/A':>3}  승률:{win_rate}"
    )


async def main() -> None:
    async with AsyncClient(api_key=API_KEY) as client:
        print("=== 플레이어 동시 조회 ===")
        # asyncio.gather로 병렬 실행
        await asyncio.gather(
            *[fetch_user_summary(client, nick) for nick in NICKNAMES]
        )


if __name__ == "__main__":
    asyncio.run(main())
