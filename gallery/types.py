from __future__ import annotations

from enum import Enum


class ZoneType(str, Enum):
    WALL = "wall"
    FLOOR = "floor"
    CEILING = "ceiling"
    VIDEO = "video"
    UNKNOWN = "unknown"


class ArtworkType(str, Enum):
    WALL = "wall"
    FLOOR = "floor"
    CEILING = "ceiling"
    VIDEO = "video"
    UNKNOWN = "unknown"


def parse_zone_type(raw: str) -> ZoneType:
    value = raw.strip().lower()
    for zone_type in ZoneType:
        if zone_type.value == value:
            return zone_type
    return ZoneType.UNKNOWN


def parse_artwork_type(raw: str) -> ArtworkType:
    value = raw.strip().lower()
    for art_type in ArtworkType:
        if art_type.value == value:
            return art_type
    return ArtworkType.UNKNOWN


def is_compatible(artwork_type: ArtworkType, zone_type: ZoneType) -> bool:
    return (
        (artwork_type == ArtworkType.WALL and zone_type == ZoneType.WALL)
        or (artwork_type == ArtworkType.FLOOR and zone_type == ZoneType.FLOOR)
        or (artwork_type == ArtworkType.CEILING and zone_type == ZoneType.CEILING)
        or (artwork_type == ArtworkType.VIDEO and zone_type == ZoneType.VIDEO)
    )
