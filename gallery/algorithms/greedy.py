from __future__ import annotations

from math import inf

from gallery.base import Algorithm
from gallery.models import Gallery, LayoutState, Show
from gallery.evaluator import Evaluator


class GreedyAlgorithm(Algorithm):
    def solve(self, gallery: Gallery, show: Show, evaluator: Evaluator) -> LayoutState:
        state = LayoutState(len(show.artworks))
        state.algorithm_name = self.name()

        for i in range(len(show.artworks)):
            best_score = -inf
            best_zone = -1

            for z in range(len(gallery.zones)):
                trial = LayoutState(len(show.artworks))
                trial.placement = state.placement.copy()
                trial.placement[i] = z
                trial.algorithm_name = state.algorithm_name
                score = evaluator.evaluate(trial, gallery, show)
                if score > best_score:
                    best_score = score
                    best_zone = z

            state.placement[i] = best_zone
            evaluator.evaluate(state, gallery, show)

        evaluator.evaluate(state, gallery, show)
        return state

    def name(self) -> str:
        return "greedy"
