from __future__ import annotations

from dataclasses import dataclass

_SEP = "┃"  # U+2503 HEAVY VERTICAL (┃)


@dataclass
class L10nData:
    """파싱된 현지화 데이터."""

    _data: dict[str, str]

    def get(self, key: str) -> str | None:
        return self._data.get(key)

    def get_character_name(self, code: int) -> str | None:
        return self._data.get(f"Character/Name/{code}")

    def get_monster_name(self, code: int) -> str | None:
        return self._data.get(f"Monster/Name/{code}")

    def get_area_name(self, area_key: str) -> str | None:
        """area_key 예: 'Harbor', 'Hospital' (Area/Name/ 접두어 자동 추가)."""
        return self._data.get(f"Area/Name/{area_key}")

    def get_skill_name(self, skill_code: int) -> str | None:
        return self._data.get(f"Skill/Group/Name/{skill_code}")

    def __len__(self) -> int:
        return len(self._data)

    @classmethod
    def from_bytes(cls, raw: bytes) -> L10nData:
        """서버 응답 바이트를 UTF-8로 파싱. Content-Type charset 미명시 대응."""
        text = raw.decode("utf-8")
        data: dict[str, str] = {}
        for line in text.splitlines():
            if _SEP in line:
                key, value = line.split(_SEP, 1)
                data[key] = value
        return cls(_data=data)
