from __future__ import annotations

from gallery.models import Artwork, Gallery, ScoringConfig, Show, Zone
from gallery.types import parse_artwork_type, parse_zone_type
from gallery.util import starts_with, strip_quotes, trim


def read_meaningful_lines(path: str) -> list[str]:
    lines: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.split("#", 1)[0]
                line = trim(line)
                if line:
                    lines.append(line)
    except OSError as exc:
        raise RuntimeError(f"Could not open file: {path}") from exc
    return lines


def split_key_value(line: str) -> tuple[str, str]:
    if ":" not in line:
        return trim(line), ""
    key, value = line.split(":", 1)
    return trim(key), strip_quotes(trim(value))


def parse_float_or_raise(value: str, field: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid numeric value for '{field}': {value}") from exc


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def load_gallery(path: str) -> Gallery:
    lines = read_meaningful_lines(path)
    gallery = Gallery()

    in_zones = False
    current = Zone()
    have_current = False

    for line in lines:
        if line == "gallery:":
            continue
        if line == "zones:":
            in_zones = True
            continue

        key, value = split_key_value(line)
        if key == "name":
            gallery.name = value
            continue

        if in_zones and starts_with(line, "- "):
            if have_current:
                gallery.zones.append(current)
            current = Zone()
            have_current = True
            remainder = trim(line[2:])
            if remainder:
                sub_key, sub_value = split_key_value(remainder)
                if sub_key == "id":
                    current.id = sub_value
            continue

        if have_current:
            if key == "id":
                current.id = value
            elif key == "room":
                current.room = value
            elif key == "type":
                current.type = parse_zone_type(value)
            elif key == "capacity":
                current.capacity = parse_float_or_raise(value, "capacity")
            elif key == "light":
                current.light = parse_float_or_raise(value, "light")
            elif key == "supports_video":
                current.supports_video = parse_bool(value)

    if have_current:
        gallery.zones.append(current)

    if not gallery.zones:
        raise RuntimeError(f"Gallery file contains no zones: {path}")

    return gallery


def load_show(path: str) -> Show:
    lines = read_meaningful_lines(path)
    show = Show()

    in_artworks = False
    current = Artwork()
    have_current = False

    for line in lines:
        if line == "show:":
            continue
        if line == "artworks:":
            in_artworks = True
            continue

        key, value = split_key_value(line)
        if not in_artworks and key == "title":
            show.title = value
            continue

        if in_artworks and starts_with(line, "- "):
            if have_current:
                show.artworks.append(current)
            current = Artwork()
            have_current = True
            remainder = trim(line[2:])
            if remainder:
                sub_key, sub_value = split_key_value(remainder)
                if sub_key == "id":
                    current.id = sub_value
            continue

        if have_current:
            if key == "id":
                current.id = value
            elif key == "title":
                current.title = value
            elif key == "type":
                current.type = parse_artwork_type(value)
            elif key == "size":
                current.size = parse_float_or_raise(value, "size")
            elif key == "light_sensitivity":
                current.light_sensitivity = parse_float_or_raise(value, "light_sensitivity")
            elif key == "preferred_room":
                current.preferred_room = value

    if have_current:
        show.artworks.append(current)

    if not show.artworks:
        raise RuntimeError(f"Show file contains no artworks: {path}")

    return show


def load_scoring(path: str) -> ScoringConfig:
    lines = read_meaningful_lines(path)
    config = ScoringConfig()

    for line in lines:
        if line == "scoring:":
            continue

        key, value = split_key_value(line)
        if not value:
            continue

        if key == "type_match_reward":
            config.type_match_reward = parse_float_or_raise(value, key)
        elif key == "type_mismatch_penalty":
            config.type_mismatch_penalty = parse_float_or_raise(value, key)
        elif key == "capacity_overflow_penalty":
            config.capacity_overflow_penalty = parse_float_or_raise(value, key)
        elif key == "unplaced_penalty":
            config.unplaced_penalty = parse_float_or_raise(value, key)
        elif key == "room_preference_reward":
            config.room_preference_reward = parse_float_or_raise(value, key)
        elif key == "duplicate_zone_penalty":
            config.duplicate_zone_penalty = parse_float_or_raise(value, key)
        elif key == "light_penalty_multiplier":
            config.light_penalty_multiplier = parse_float_or_raise(value, key)

    return config
