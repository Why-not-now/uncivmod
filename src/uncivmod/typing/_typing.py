from __future__ import annotations

from enum import StrEnum


class _StrEnum(StrEnum):
    """Enum where members are also (and must be) strings."""

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]  # noqa: ARG004
    ) -> str:
        return name
