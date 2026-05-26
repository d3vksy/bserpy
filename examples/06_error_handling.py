"""
예제 06 — 에러 처리

각 예외 유형별 처리 패턴을 보여줍니다.
"""

import time

from bserpy import (
    AuthenticationError,
    Client,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TransportError,
)

API_KEY = "YOUR_API_KEY_HERE"


def safe_get_uid(client: Client, nickname: str) -> str | None:
    """에러 처리를 포함한 userId 조회 예시."""
    try:
        user = client.users.get_uid(nickname)
        return user.user_id
    except NotFoundError:
        print(f"  [404] '{nickname}' 닉네임을 찾을 수 없습니다.")
    except RateLimitError as e:
        wait = e.retry_after or 1.0
        print(f"  [레이트 리미트] {wait:.1f}초 후 재시도합니다.")
        time.sleep(wait)
    except AuthenticationError:
        print("  [403] API 키가 유효하지 않습니다.")
    except TransportError as e:
        print(f"  [네트워크 오류] {e}")
    except ServerError as e:
        print(f"  [서버 오류 {e.status_code}] 잠시 후 다시 시도하세요.")
    return None


def main() -> None:
    # API 키 없으면 즉시 ConfigurationError
    try:
        Client(api_key="")
    except ConfigurationError as e:
        print(f"설정 오류: {e}")

    with Client(api_key=API_KEY) as client:
        # 존재하지 않는 닉네임
        print("\n[존재하지 않는 닉네임 조회]")
        safe_get_uid(client, "절대없는닉네임xyzxyz999")

        # 정상 조회
        print("\n[정상 조회]")
        user_id = safe_get_uid(client, "oracle1")
        if user_id:
            print(f"  userId: {user_id}")


if __name__ == "__main__":
    main()
