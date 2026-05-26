from __future__ import annotations

import json
from pathlib import Path

import pytest
import respx
import httpx

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def mock_api():
    """respx 기반 API 모킹 컨텍스트."""
    with respx.mock(base_url="https://open-api.bser.io", assert_all_called=False) as mock:
        yield mock
