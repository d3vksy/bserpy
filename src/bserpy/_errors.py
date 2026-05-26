from __future__ import annotations


class BserError(Exception):
    """bserpy 기본 예외."""


class ConfigurationError(BserError):
    """API 키 누락 등 설정 오류."""


class TransportError(BserError):
    """DNS, TLS, 연결 실패, 타임아웃."""


class AuthenticationError(BserError):
    """403 — 유효하지 않은 API 키."""

    def __init__(self, message: str, status_code: int = 403) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(BserError):
    """403(레이트 리미트) 또는 429 — 요청 초과."""

    def __init__(
        self, message: str, status_code: int = 429, retry_after: float | None = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.retry_after = retry_after


class NotFoundError(BserError):
    """404 — 리소스를 찾을 수 없음."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.status_code = 404


class ServerError(BserError):
    """5xx — 서버 내부 오류."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.status_code = status_code
