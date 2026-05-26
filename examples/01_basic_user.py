"""
예제 01 — 유저 기본 조회

가장 기본적인 흐름:
  닉네임 → userId → 랭크 / 통계 / 경기 목록
"""

from bserpy import Client, NotFoundError

API_KEY = "YOUR_API_KEY_HERE"
NICKNAME = "oracle1"
SEASON_ID = 39  # 현재 시즌 (Season 20)


def main() -> None:
    with Client(api_key=API_KEY) as client:
        # 1. 닉네임으로 userId 획득
        try:
            user = client.users.get_uid(NICKNAME)
        except NotFoundError:
            print(f"닉네임 '{NICKNAME}' 을 찾을 수 없습니다.")
            return

        print(f"닉네임: {user.nickname}")
        print(f"userId: {user.user_id}")

        # 2. 랭크 조회 (스쿼드 고정)
        rank = client.users.get_rank(user.user_id, season_id=SEASON_ID)
        print(f"\n[랭크]")
        print(f"  글로벌 순위: {rank.rank}위  MMR: {rank.mmr}")
        print(f"  서버 내 순위: {rank.server_rank}위  (서버코드: {rank.server_code})")

        # 3. 시즌 통계 조회 (랭크 모드 = 3)
        stats_list = client.users.get_stats(user.user_id, season_id=SEASON_ID, mode=3)
        for stats in stats_list:
            print(f"\n[시즌 {stats.season_id} 통계]")
            print(f"  총 게임: {stats.total_games}  승리: {stats.total_wins}")
            print(f"  평균 순위: {stats.average_rank:.2f}  평균 킬: {stats.average_kills:.2f}")
            print(f"  상위 {stats.rank_percent * 100:.1f}%")
            print(f"  주요 캐릭터:")
            for cs in stats.character_stats[:3]:
                print(f"    코드 {cs.character_code}: {cs.total_games}게임 {cs.wins}승")

        # 4. 최근 경기 목록
        games = client.users.get_games(user.user_id)
        print(f"\n[최근 경기 {len(games)}개]")
        for g in games[:5]:
            result = "승" if g.victory else "패"
            print(
                f"  #{g.game_id}  {result}  {g.game_rank}위  "
                f"킬:{g.player_kill} 어시:{g.player_assistant}"
            )


if __name__ == "__main__":
    main()
