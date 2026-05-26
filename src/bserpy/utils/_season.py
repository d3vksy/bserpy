from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bserpy._client import Client


class SeasonHelper:
    """Helper for season information.

    Example::

        with Client(api_key="...") as client:
            seasons = SeasonHelper(client)
            current = seasons.current_season()
            print(current["seasonName"], current["seasonID"])
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._seasons: list[dict[str, Any]] | None = None

    def _load(self) -> None:
        if self._seasons is None:
            self._seasons = self._client.meta.get_data("Season")

    def all_seasons(self) -> list[dict[str, Any]]:
        """Return all seasons sorted by seasonID."""
        self._load()
        assert self._seasons is not None
        return sorted(self._seasons, key=lambda s: s.get("seasonID", 0))

    def current_season(self) -> dict[str, Any] | None:
        """Return the currently active season, or None if none is marked current."""
        self._load()
        assert self._seasons is not None
        return next((s for s in self._seasons if s.get("isCurrent") == 1), None)

    def get_season(self, season_id: int) -> dict[str, Any] | None:
        """Find a season by its ID."""
        self._load()
        assert self._seasons is not None
        return next((s for s in self._seasons if s.get("seasonID") == season_id), None)

    def ranked_seasons(self) -> list[dict[str, Any]]:
        """Return only ranked (non-normal) seasons."""
        self._load()
        assert self._seasons is not None
        return [s for s in self._seasons if s.get("seasonType", 0) != 0]
