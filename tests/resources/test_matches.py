from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.models import BattleUserResult

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_get_match(client):
    fixture = json.loads((FIXTURES / "match.json").read_text(encoding="utf-8"))
    respx.get("https://open-api.bser.io/v1/games/60903118").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    results = client.matches.get(game_id=60903118)
    assert len(results) == 1
    r = results[0]
    assert isinstance(r, BattleUserResult)
    assert r.game_id == 60903118
    assert r.nickname == "oracle1"
    assert r.victory == 1
    assert r.player_kill == 11
    # 실제 응답 키: totalVFCredits (배열)
    assert isinstance(r.total_vf_credits, list)
    assert r.total_vf_credits[0] == 53
    # 실측 신규 필드: equipmentGrade
    assert r.equipment_grade == {"0": 6}


@respx.mock
def test_get_match_500(client):
    from bserpy import ServerError

    respx.get("https://open-api.bser.io/v1/games/99999").mock(
        return_value=httpx.Response(500, json={"code": 500, "message": "Internal Server Error"})
    )
    with pytest.raises(ServerError):
        client.matches.get(game_id=99999)
