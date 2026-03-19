from __future__ import annotations

from gallery.models import Gallery, LayoutState, ScoreBreakdown, ScoringConfig, Show
from gallery.types import is_compatible


class Evaluator:
    def __init__(self, config: ScoringConfig | None = None) -> None:
        self._config = config or ScoringConfig()

    @property
    def config(self) -> ScoringConfig:
        return self._config

    def evaluate(self, state: LayoutState, gallery: Gallery, show: Show) -> float:
        state.breakdown = ScoreBreakdown()
        zone_use_count = [0] * len(gallery.zones)

        for index, art in enumerate(show.artworks):
            zone_index = state.placement[index]

            if zone_index < 0 or zone_index >= len(gallery.zones):
                state.breakdown.unplaced += self._config.unplaced_penalty
                continue

            zone = gallery.zones[zone_index]
            zone_use_count[zone_index] += 1

            if is_compatible(art.type, zone.type):
                state.breakdown.compatibility += self._config.type_match_reward
            else:
                state.breakdown.compatibility += self._config.type_mismatch_penalty

            if art.size > zone.capacity:
                state.breakdown.capacity += self._config.capacity_overflow_penalty

            excess_light = max(0.0, zone.light - art.light_sensitivity)
            state.breakdown.light -= excess_light * self._config.light_penalty_multiplier

            if art.preferred_room and art.preferred_room == zone.room:
                state.breakdown.room_preference += self._config.room_preference_reward

        for count in zone_use_count:
            if count > 1:
                state.breakdown.duplicate_use += (count - 1) * self._config.duplicate_zone_penalty

        state.score = state.breakdown.total()
        return state.score
