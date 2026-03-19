from __future__ import annotations


def trim(value: str) -> str:
    return value.strip()


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")):
        return value[1:-1]
    return value


def starts_with(value: str, prefix: str) -> bool:
    return value.startswith(prefix)
