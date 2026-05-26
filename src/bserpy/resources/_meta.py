from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models._l10n import L10nData
from ..models._route import WeaponRouteBundle

if TYPE_CHECKING:
    from .._http import SyncTransport


class MetaResource:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport
        self._l10n_cache: dict[str, L10nData] = {}

    def get_hash(self) -> dict[str, int]:
        """사용 가능한 메타 테이블 이름과 해시 코드 딕셔너리."""
        data = self._t.get("/v2/data/hash")
        result: dict[str, int] = data["data"]
        return result

    def get_data(self, meta_type: str) -> list[dict[str, Any]]:
        """특정 게임 데이터 테이블 조회. meta_type 예: 'Character', 'Monster'."""
        data = self._t.get(f"/v2/data/{meta_type}")
        result: list[dict[str, Any]] = data["data"]
        return result

    def get_l10n(self, language: str = "Korean") -> str:
        """현지화 데이터 다운로드 URL 반환."""
        data = self._t.get(f"/v1/l10n/{language}")
        result: str = data["data"]["l10Path"]
        return result

    def get_l10n_parsed(self, language: str = "Korean") -> L10nData:
        """현지화 데이터를 자동 파싱해서 L10nData로 반환.

        언어별로 캐시하므로 같은 언어 반복 호출 시 네트워크 요청 없음.
        서버가 Content-Type에 charset을 명시하지 않으므로 UTF-8로 강제 디코딩.
        """
        if language not in self._l10n_cache:
            url = self.get_l10n(language)
            raw = self._t.get_raw(url)
            self._l10n_cache[language] = L10nData.from_bytes(raw)
        return self._l10n_cache[language]

    def get_weapon_routes(self, route_id: int | None = None) -> list[WeaponRouteBundle]:
        """추천 무기 루트 목록 (최대 100개)."""
        data = self._t.get("/v1/weaponRoutes/recommend", routeId=route_id)
        return [WeaponRouteBundle.from_dict(r) for r in data.get("result", [])]
