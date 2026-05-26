"""
예제 03 — 경기 상세 조회

게임 ID로 해당 경기에 참가한 전체 플레이어의 결과를 조회합니다.
"""

from bserpy import Client

API_KEY = "YOUR_API_KEY_HERE"
GAME_ID = 60903118  # 조회할 게임 ID


def main() -> None:
    with Client(api_key=API_KEY) as client:
        players = client.matches.get(game_id=GAME_ID)

    print(f"경기 #{GAME_ID}  참가 인원: {len(players)}명\n")

    # 순위별 정렬
    players.sort(key=lambda p: p.game_rank)

    print(f"{'순위':>4}  {'닉네임':<20}  {'킬':>3}  {'어시':>4}  {'몬스터':>6}  {'MMR변동':>7}")
    print("-" * 60)
    for p in players:
        mmr_str = f"{p.mmr_gain:+d}" if p.mmr_gain is not None else "  -"
        print(
            f"  {p.game_rank:>2}위  {p.nickname:<20}  "
            f"{p.player_kill:>3}  {p.player_assistant:>4}  "
            f"{p.monster_kill:>6}  {mmr_str:>7}"
        )

    # 1위 상세 정보
    winner = next((p for p in players if p.game_rank == 1), None)
    if winner:
        print(f"\n[1위 상세 — {winner.nickname}]")
        print(f"  캐릭터 코드: {winner.character_num}  레벨: {winner.character_level}")
        print(f"  대 플레이어 피해: {winner.damage_to_player:,}")
        print(f"  대 몬스터 피해:   {winner.damage_to_monster:,}")
        print(f"  회복량: {winner.heal_amount:,}")
        print(f"  최고 무기 숙련도: {winner.best_weapon} (레벨 {winner.best_weapon_level})")
        if winner.total_vf_credits:
            print(f"  획득 크레딧 총합: {sum(winner.total_vf_credits):,}")


if __name__ == "__main__":
    main()
