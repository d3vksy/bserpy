from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.models import RegionServer, TopRank

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_get_top(client):
    fixture = json.loads((FIXTURES / "top_ranks.json").read_text(encoding="utf-8"))
    respx.get("https://open-api.bser.io/v1/rank/top/39/3").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    ranks = client.ranking.get_top(season_id=39)
    assert len(ranks) == 2
    assert isinstance(ranks[0], TopRank)
    assert ranks[0].nickname == "oracle1"
    assert ranks[0].rank == 1
    assert ranks[0].mmr == 9569
    # 실제 응답에 uid 없음 (문서 오류)
    assert not hasattr(ranks[0], "uid")


@respx.mock
def test_get_top_by_server(client):
    fixture = json.loads((FIXTURES / "top_ranks.json").read_text(encoding="utf-8"))
    respx.get("https://open-api.bser.io/v1/rank/top/39/3/10").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    ranks = client.ranking.get_top_by_server(season_id=39, server=RegionServer.ASIA)
    assert len(ranks) == 2
