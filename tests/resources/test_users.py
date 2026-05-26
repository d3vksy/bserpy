from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from bserpy import AuthenticationError, Client, ConfigurationError, NotFoundError, RateLimitError
from bserpy.models import UserInfo, UserRank, UserStats

FIXTURES = Path(__file__).parent.parent / "fixtures"
USER_ID = "AMRZxZuiwOtgeZ6h9TYbJBOGpuVUpdDtRGtJW9SFcWZ2zyg1WcaTzD7pTw"


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


def test_config_error_no_key():
    with pytest.raises(ConfigurationError):
        Client(api_key="")


def test_client_repr_masks_key():
    c = Client(api_key="super-secret")
    assert "super-secret" not in repr(c)
    assert "****" in repr(c)
    c.close()


@respx.mock
def test_get_uid(client):
    fixture = json.loads((FIXTURES / "user_nickname.json").read_text(encoding="utf-8"))
    respx.get("https://open-api.bser.io/v1/user/nickname").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    user = client.users.get_uid("oracle1")
    assert isinstance(user, UserInfo)
    assert user.user_id == USER_ID
    assert user.nickname == "oracle1"


@respx.mock
def test_get_rank(client):
    fixture = json.loads((FIXTURES / "user_rank.json").read_text(encoding="utf-8"))
    respx.get(f"https://open-api.bser.io/v1/rank/uid/{USER_ID}/39/3").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    rank = client.users.get_rank(USER_ID, season_id=39)
    assert isinstance(rank, UserRank)
    assert rank.rank == 1
    assert rank.mmr == 9569
    assert rank.server_code == 10
    assert rank.reward_server_code == 10  # 문서 미기재 필드


@respx.mock
def test_get_stats(client):
    fixture = json.loads((FIXTURES / "user_stats.json").read_text(encoding="utf-8"))
    respx.get(f"https://open-api.bser.io/v2/user/stats/uid/{USER_ID}/39/3").mock(
        return_value=httpx.Response(200, json=fixture)
    )
    stats = client.users.get_stats(USER_ID, season_id=39)
    assert len(stats) == 1
    s = stats[0]
    assert isinstance(s, UserStats)
    assert s.total_games == 194
    assert len(s.character_stats) == 1
    cs = s.character_stats[0]
    assert cs.character_code == 67
    assert cs.most_used_skin_code == 1067003  # 문서 미기재 필드


@respx.mock
def test_get_uid_404(client):
    respx.get("https://open-api.bser.io/v1/user/nickname").mock(
        return_value=httpx.Response(404, json={"code": 404, "message": "Not Found"})
    )
    with pytest.raises(NotFoundError):
        client.users.get_uid("없는닉네임")


@respx.mock
def test_get_uid_rate_limit_429(client):
    respx.get("https://open-api.bser.io/v1/user/nickname").mock(
        return_value=httpx.Response(429, json={"code": 429, "message": "Too Many Requests"})
    )
    with pytest.raises(RateLimitError):
        client.users.get_uid("oracle1")


@respx.mock
def test_get_uid_403_auth(client):
    respx.get("https://open-api.bser.io/v1/user/nickname").mock(
        return_value=httpx.Response(403, json={"code": 403, "message": "Forbidden"})
    )
    with pytest.raises(AuthenticationError):
        client.users.get_uid("oracle1")
