from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models._l10n import L10nData
from ..models._route import WeaponRouteBundle

if TYPE_CHECKING:
    from .._http import AsyncTransport


class AsyncMetaResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport
        self._l10n_cache: dict[str, L10nData] = {}

    async def get_hash(self) -> dict[str, int]:
        data = await self._t.get("/v2/data/hash")
        result: dict[str, int] = data["data"]
        return result

    async def get_data(self, meta_type: str) -> list[dict[str, Any]]:
        data = await self._t.get(f"/v2/data/{meta_type}")
        result: list[dict[str, Any]] = data["data"]
        return result

    async def get_l10n(self, language: str = "Korean") -> str:
        data = await self._t.get(f"/v1/l10n/{language}")
        result: str = data["data"]["l10Path"]
        return result

    async def get_l10n_parsed(self, language: str = "Korean") -> L10nData:
        if language not in self._l10n_cache:
            url = await self.get_l10n(language)
            raw = await self._t.get_raw(url)
            self._l10n_cache[language] = L10nData.from_bytes(raw)
        return self._l10n_cache[language]

    async def get_weapon_routes(self, route_id: int | None = None) -> list[WeaponRouteBundle]:
        data = await self._t.get("/v1/weaponRoutes/recommend", routeId=route_id)
        return [WeaponRouteBundle.from_dict(r) for r in data.get("result", [])]
