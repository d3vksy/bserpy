<div align="center">
  <h1>Bserpy</h1>
  <img src="./logo_black.png"></img>
  <p><strong>이터널리턴 Open API Python 래퍼 라이브러리</strong></p>
</div>

[<img src="https://img.shields.io/pypi/v/bserpy.svg">](https://pypi.python.org/pypi/bserpy)
[<img src="https://img.shields.io/pypi/pyversions/bserpy.svg">](https://pypi.python.org/pypi/bserpy)
[<img src="https://img.shields.io/github/actions/workflow/status/d3vksy/bserpy/ci.yml?branch=main">](https://github.com/d3vksy/bserpy/actions)
[<img src="https://img.shields.io/badge/License-MIT-yellow.svg">](https://github.com/d3vksy/bserpy/blob/main/LICENSE)<br>

```python
from bserpy import Client

with Client(api_key="...") as client:
user = client.users.get_uid("oracle1")
rank = client.users.get_rank(user.user_id, season_id=39)
print(f"{rank.rank}위 MMR {rank.mmr}")

```

## 설치

```bash
pip install bserpy
```

Python 3.11 이상 필요.

## 기능

- 동기(`Client`) / 비동기(`AsyncClient`) 모두 지원
- 자동 재시도 — 429·5xx에서 지수 백오프 + jitter (최대 3회)
- 예외 계층 — HTTP 상태코드별 명시적 예외 클래스
- `utils` — 레벨별 스탯 계산, 아이템 검색, 시뮬레이터 등 편의 헬퍼

## 빠른 시작

### 유저 정보

```python
from bserpy import Client

with Client(api_key="YOUR_API_KEY") as client:
    # 닉네임 → userId
    user = client.users.get_uid("oracle1")

    # 시즌 랭크
    rank = client.users.get_rank(user.user_id, season_id=39)
    print(f"{rank.rank}위  MMR {rank.mmr}")

    # 시즌 통계 (mode=3: 스쿼드 랭크)
    stats_list = client.users.get_stats(user.user_id, season_id=39, mode=3)
    if stats_list:
        s = stats_list[0]
        print(f"{s.total_games}게임  {s.total_wins}승")

    # 최근 게임 목록
    games = client.users.get_games(user.user_id)
```

### 랭킹

```python
from bserpy import Client, RegionServer

with Client(api_key="...") as client:
    top = client.ranking.get_top(season_id=39)
    for r in top[:5]:
        print(f"{r.rank}위  {r.nickname}  {r.mmr}")

    # 서버별 랭킹
    asia = client.ranking.get_top_by_server(season_id=39, server=RegionServer.ASIA)
```

### 경기 상세

```python
with Client(api_key="...") as client:
    players = client.matches.get(game_id=60903118)
    players.sort(key=lambda p: p.game_rank)
    for p in players:
        print(f"{p.game_rank}위  {p.nickname}  킬:{p.player_kill}")
```

### 현지화 & 메타 데이터

```python
with Client(api_key="...") as client:
    # 현지화 파일을 다운로드·파싱, 같은 언어는 재요청 없이 캐시에서 반환
    l10n = client.meta.get_l10n_parsed("Korean")
    print(l10n.get_character_name(1))  # "재키"

    # "Season", "Character", "ItemWeapon" 등 게임 메타 테이블을 dict 목록으로 반환
    seasons = client.meta.get_data("Season")
    current = next(s for s in seasons if s.get("isCurrent") == 1)
    print(current["seasonName"])
```

### 비동기

```python
import asyncio
from bserpy import AsyncClient

async def main():
    async with AsyncClient(api_key="...") as client:
        user = await client.users.get_uid("oracle1")
        rank = await client.users.get_rank(user.user_id, season_id=39)
        print(rank.rank, rank.mmr)

asyncio.run(main())
```

## utils 헬퍼

### CharacterHelper — 레벨별 스탯

```python
from bserpy import Client, CharacterHelper

with Client(api_key="...") as client:
    chars = CharacterHelper(client)
    char_id = 1  # 재키

    # 레벨 15 스탯 계산: 기본 스탯 + 레벨업 증가치 × (레벨 - 1) 공식으로 산출
    lv15 = chars.stats_at_level(char_id, level=15)
    print(lv15.max_hp, lv15.attack_power)

    # 레벨 1 상승 시 더해지는 증가치 원본
    # (매 레벨업마다 이 수치가 기본 스탯에 누적됨)
    growth = chars.level_up_stat(char_id)

    # 캐릭터 분류 정보: 직업 유형(전사/암살자 등), 공격 사거리(근거리/원거리),
    # 게임 시작 시 보유하는 스킬 코드 목록
    info = chars.info(char_id)

    # 게임에서 고를 수 있는 숙련도 종류 목록 조회
    # opts.weapon_types   → ["OneHandSword", "TwoHandSword", "Axe", "DualSword"]
    # opts.combat_types   → ["Defense", "Hunt"]
    # opts.survival_types → ["Craft", "Search", "Move"]
    opts = chars.mastery_options(char_id)

    # 재키가 한손검(OneHandSword) 무기 숙련도를 선택했을 때 부여되는 보너스 스탯 목록
    # 해당 캐릭터가 선택할 수 없는 무기 타입이면 None 반환
    bonus = chars.mastery_stat(char_id, "OneHandSword")
    if bonus:
        for stat in bonus.bonuses:  # 최대 3개, "None" 항목 제외
            print(stat.name, stat.value)
            # 예) AttackSpeedRatio 0.041
            #     IncreaseBasicAttackDamageRatio 0.03
```

### CharacterSimulator — 아이템 장착 스탯 계산

```python
from bserpy import Client, CharacterSimulator

with Client(api_key="...") as client:
    stats = (
        CharacterSimulator(client, character_code=1, level=20)
        .add_weapon(101405)
        .add_armor(201501)   # 머리 슬롯
        .add_armor(202501)   # 옷 슬롯 (같은 슬롯 재장착 시 교체)
        .get_stats()
    )
    print(f"HP {stats.max_hp:.0f}  ATK {stats.attack_power:.1f}")
    # effective_attack_speed: 기본 공속 × (1 + 공속비율 합산), 캐릭터 상한값 자동 클리핑
    print(f"공속 {stats.effective_attack_speed:.3f}")
```

### ItemHelper — 아이템 검색 & 제작

```python
from bserpy import Client
from bserpy.utils import ItemHelper

with Client(api_key="...") as client:
    items = ItemHelper(client)

    sword = items.get(101405)                                    # 아이템 코드로 단일 아이템 조회
    ep    = items.get_weapons(grade="Epic", completed_only=True) # 완성 에픽 무기만 필터링
    mats  = items.craft_tree(101405)                             # 최종 재료까지 재귀 분해한 기본 재료 목록
    r1, r2 = items.recipe(101405) or (0, 0)                     # 직접 조합 재료 2개 (조합 불가 시 None)
```

### SeasonHelper — 시즌 정보

```python
from bserpy import Client
from bserpy.utils import SeasonHelper

with Client(api_key="...") as client:
    seasons = SeasonHelper(client)
    cur = seasons.current_season()  # 진행 중인 시즌이 없으면 None 반환
    if cur:
        print(cur["seasonName"], cur["seasonID"])
```

## 에러 처리

```python
from bserpy import (
    Client, NotFoundError, RateLimitError,
    AuthenticationError, ServerError, TransportError,
)
import time

with Client(api_key="...") as client:
    try:
        user = client.users.get_uid("없는닉네임")
    except NotFoundError:
        print("유저 없음")
    except RateLimitError as e:
        time.sleep(e.retry_after or 1.0)
    except AuthenticationError:
        print("API 키 오류")
    except ServerError as e:
        print(f"서버 오류 {e.status_code}")
    except TransportError as e:
        print(f"네트워크 오류 {e}")
```

## 예외 목록

| 예외                  | 원인                                               |
| --------------------- | -------------------------------------------------- |
| `ConfigurationError`  | `api_key` 누락 또는 빈 값                          |
| `TransportError`      | DNS, TLS, 타임아웃 등 네트워크 오류                |
| `AuthenticationError` | 403 — API 키 인증 실패                             |
| `RateLimitError`      | 403(레이트리밋) 또는 429 — `retry_after` 속성 포함 |
| `NotFoundError`       | 404                                                |
| `ServerError`         | 5xx — `status_code` 속성 포함                      |
