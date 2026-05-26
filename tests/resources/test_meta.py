from __future__ import annotations

import httpx
import pytest
import respx

from bserpy import Client
from bserpy.models import L10nData, WeaponRouteBundle

ROUTE_FIXTURE = {
    "code": 200,
    "message": "Success",
    "result": [
        {
            "recommendWeaponRoute": {
                "id": 16998,
                "title": "테스트",
                "userNum": 5968045,
                "userNickname": "테스터",
                "characterCode": 79,
                "slotId": 0,
                "weaponType": 8,
                "weaponCodes": "[115403,202307]",
                "traitCodes": "[7300201,7310401]",
                "lateGameItemCodes": '{"0":[115504,202511]}',
                "remoteTransferItemCodes": "[]",
                "tacticalSkillGroupCode": 30,
                "paths": "[90,10]",
                "count": 0,
                "version": "11.1.0",
                "teamMode": 0,
                "languageCode": "ko",
                "routeVersion": 5,
                "share": True,
                "updateDtm": 1778343557000,
                "v2Like": 0,
                "v2WinRate": 0.0,
                "v2SeasonId": 0,
                "v2AccumulateLike": 0,
                "v2AccumulateWinRate": 0.0,
                "v2AccumulateSeasonId": 0,
            },
            "recommendWeaponRouteDesc": {"recommendWeaponRouteId": 16998, "skillPath": "e,q,w,q"},
        }
    ],
}

L10N_FIXTURE = {
    "code": 200,
    "message": "Success",
    "data": {"l10Path": "https://example.com/l10n.txt"},
}

L10N_CONTENT = "Character/Name/1┃재키\nCharacter/Name/2┃아야\nArea/Name/Harbor┃항구\n"


@pytest.fixture
def client():
    with Client(api_key="test-key") as c:
        yield c


@respx.mock
def test_get_weapon_routes(client):
    respx.get("https://open-api.bser.io/v1/weaponRoutes/recommend").mock(
        return_value=httpx.Response(200, json=ROUTE_FIXTURE)
    )
    routes = client.meta.get_weapon_routes()
    assert len(routes) == 1
    bundle = routes[0]
    assert isinstance(bundle, WeaponRouteBundle)
    assert bundle.route.id == 16998
    # JSON 문자열 자동 파싱 확인
    assert bundle.route.weapon_codes == [115403, 202307]
    assert bundle.route.paths == [90, 10]
    assert bundle.route.late_game_item_codes["0"] == [115504, 202511]
    assert bundle.desc.skill_path == "e,q,w,q"


@respx.mock
def test_get_l10n_url_only(client):
    respx.get("https://open-api.bser.io/v1/l10n/Korean").mock(
        return_value=httpx.Response(200, json=L10N_FIXTURE)
    )
    url = client.meta.get_l10n("Korean")
    assert url == "https://example.com/l10n.txt"


@respx.mock
def test_get_l10n_parsed(client):
    respx.get("https://open-api.bser.io/v1/l10n/Korean").mock(
        return_value=httpx.Response(200, json=L10N_FIXTURE)
    )
    respx.get("https://example.com/l10n.txt").mock(
        return_value=httpx.Response(200, content=L10N_CONTENT.encode("utf-8"))
    )
    l10n = client.meta.get_l10n_parsed("Korean")
    assert isinstance(l10n, L10nData)
    assert l10n.get_character_name(1) == "재키"
    assert l10n.get_character_name(2) == "아야"
    assert l10n.get_area_name("Harbor") == "항구"
    assert l10n.get("Character/Name/1") == "재키"
    assert len(l10n) == 3
