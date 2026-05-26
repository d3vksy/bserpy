from __future__ import annotations

import random
import time
from typing import Any

import httpx

from ._errors import (
    AuthenticationError,
    BserError,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TransportError,
)

_BASE_URL = "https://open-api.bser.io"
_RETRY_STATUSES = {429, 502, 503, 504}
_DEFAULT_CONNECT_TIMEOUT = 5.0
_DEFAULT_READ_TIMEOUT = 10.0


def _parse_error(response: httpx.Response) -> BserError:
    """HTTP 응답을 적절한 BserError 서브클래스로 변환."""
    status = response.status_code
    try:
        body = response.json()
        code = body.get("code", status)
        message = body.get("message", response.text)
    except Exception:
        code = status
        message = response.text or f"HTTP {status}"

    if status == 404:
        return NotFoundError(message)

    if status in (403, 429):
        # BSER는 403을 레이트 리미트와 인증 실패 두 가지로 사용
        # code == 429 또는 429 상태코드 → RateLimitError
        if status == 429 or code == 429:
            retry_after_raw = response.headers.get("Retry-After")
            retry_after = float(retry_after_raw) if retry_after_raw else None
            return RateLimitError(message, status_code=status, retry_after=retry_after)
        return AuthenticationError(message, status_code=status)

    if status >= 500:
        return ServerError(message, status_code=status)

    return BserError(f"HTTP {status}: {message}")


class SyncTransport:
    """httpx.Client 기반 동기 HTTP 트랜스포트."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout: httpx.Timeout | None = None,
        max_retries: int = 3,
        http_client: httpx.Client | None = None,
    ) -> None:
        if not api_key:
            raise ConfigurationError("api_key가 필요합니다.")
        self._api_key = api_key
        self._max_retries = max_retries
        self._timeout = timeout or httpx.Timeout(
            connect=_DEFAULT_CONNECT_TIMEOUT,
            read=_DEFAULT_READ_TIMEOUT,
            write=_DEFAULT_READ_TIMEOUT,
            pool=_DEFAULT_CONNECT_TIMEOUT,
        )
        self._client = http_client or httpx.Client(
            base_url=_BASE_URL,
            timeout=self._timeout,
            headers={"x-api-key": self._api_key},
        )

    def get(self, path: str, **params: Any) -> Any:
        """GET 요청. 재시도 포함. 파싱된 JSON을 반환."""
        query = {k: v for k, v in params.items() if v is not None}
        attempt = 0
        while True:
            try:
                response = self._client.get(path, params=query)
            except httpx.TransportError as exc:
                raise TransportError(str(exc)) from exc

            if response.status_code == 200:
                return response.json()

            err = _parse_error(response)
            if isinstance(err, (RateLimitError, ServerError)) and attempt < self._max_retries:
                delay = _backoff(attempt, getattr(err, "retry_after", None))
                time.sleep(delay)
                attempt += 1
                continue

            raise err

    def get_raw(self, url: str) -> bytes:
        """절대 URL에서 원시 바이트를 가져옴 (l10n 파일 다운로드용)."""
        try:
            response = httpx.get(url, timeout=self._timeout)
            response.raise_for_status()
            return response.content
        except httpx.TransportError as exc:
            raise TransportError(str(exc)) from exc

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncTransport:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncTransport:
    """httpx.AsyncClient 기반 비동기 HTTP 트랜스포트."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout: httpx.Timeout | None = None,
        max_retries: int = 3,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key:
            raise ConfigurationError("api_key가 필요합니다.")
        self._api_key = api_key
        self._max_retries = max_retries
        self._timeout = timeout or httpx.Timeout(
            connect=_DEFAULT_CONNECT_TIMEOUT,
            read=_DEFAULT_READ_TIMEOUT,
            write=_DEFAULT_READ_TIMEOUT,
            pool=_DEFAULT_CONNECT_TIMEOUT,
        )
        self._client = http_client or httpx.AsyncClient(
            base_url=_BASE_URL,
            timeout=self._timeout,
            headers={"x-api-key": self._api_key},
        )

    async def get(self, path: str, **params: Any) -> Any:
        """GET 요청 (비동기). 재시도 포함."""
        import asyncio

        query = {k: v for k, v in params.items() if v is not None}
        attempt = 0
        while True:
            try:
                response = await self._client.get(path, params=query)
            except httpx.TransportError as exc:
                raise TransportError(str(exc)) from exc

            if response.status_code == 200:
                return response.json()

            err = _parse_error(response)
            if isinstance(err, (RateLimitError, ServerError)) and attempt < self._max_retries:
                delay = _backoff(attempt, getattr(err, "retry_after", None))
                await asyncio.sleep(delay)
                attempt += 1
                continue

            raise err

    async def get_raw(self, url: str) -> bytes:
        """절대 URL에서 원시 바이트를 가져옴 (l10n 파일 다운로드용)."""
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except httpx.TransportError as exc:
            raise TransportError(str(exc)) from exc

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTransport:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()


def _backoff(attempt: int, retry_after: float | None) -> float:
    """서버 Retry-After 우선, 없으면 exponential backoff + jitter."""
    if retry_after is not None:
        return retry_after
    base = 2**attempt
    jitter = random.uniform(0, base * 0.1)
    return base + jitter
