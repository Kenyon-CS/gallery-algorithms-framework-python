from __future__ import annotations

from dataclasses import dataclass, field

from gallery.types import ArtworkType, ZoneType


@dataclass
class Zone:
    id: str = ""
    room: str = ""
    type: ZoneType = ZoneType.UNKNOWN
    capacity: float = 0.0
    light: float = 0.5
    supports_video: bool = False


@dataclass
class Artwork:
    id: str = ""
    title: str = ""
    type: ArtworkType = ArtworkType.UNKNOWN
    size: float = 0.0
    light_sensitivity: float = 0.5
    preferred_room: str = ""


@dataclass
class Gallery:
    name: str = ""
    zones: list[Zone] = field(default_factory=list)


@dataclass
class Show:
    title: str = ""
    artworks: list[Artwork] = field(default_factory=list)


@dataclass
class ScoringConfig:
    type_match_reward: float = 15.0
    type_mismatch_penalty: float = -50.0
    capacity_overflow_penalty: float = -80.0
    unplaced_penalty: float = -120.0
    room_preference_reward: float = 10.0
    duplicate_zone_penalty: float = -100.0
    light_penalty_multiplier: float = 40.0


@dataclass
class ScoreBreakdown:
    compatibility: float = 0.0
    capacity: float = 0.0
    light: float = 0.0
    room_preference: float = 0.0
    unplaced: float = 0.0
    duplicate_use: float = 0.0

    def total(self) -> float:
        return (
            self.compatibility
            + self.capacity
            + self.light
            + self.room_preference
            + self.unplaced
            + self.duplicate_use
        )


@dataclass
class LayoutState:
    artwork_count: int = 0
    placement: list[int] = field(init=False)
    breakdown: ScoreBreakdown = field(default_factory=ScoreBreakdown)
    score: float = 0.0
    algorithm_name: str = ""

    def __post_init__(self) -> None:
        self.placement = [-1] * self.artwork_count
