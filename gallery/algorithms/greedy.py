from __future__ import annotations

from copy import deepcopy

from gallery.base import Algorithm
from gallery.models import LayoutState


class GreedyAlgorithm(Algorithm):
    def solve(self, gallery, show, evaluator):
        state = LayoutState(len(show.artworks))
        state.algorithm_name = self.name()

        for artwork_index, _artwork in enumerate(show.artworks):
            best_score = float("-inf")
            best_zone = -1

            for zone_index, _zone in enumerate(gallery.zones):
                trial = deepcopy(state)
                trial.placement[artwork_index] = zone_index
                score = evaluator.evaluate(trial, gallery, show)
                if score > best_score:
                    best_score = score
                    best_zone = zone_index

            state.placement[artwork_index] = best_zone
            evaluator.evaluate(state, gallery, show)

        evaluator.evaluate(state, gallery, show)
        return state

    def name(self) -> str:
        return "greedy"
