from __future__ import annotations

import random

from gallery.base import Algorithm
from gallery.evaluator import Evaluator
from gallery.models import Gallery, LayoutState, Show


class RandomAlgorithm(Algorithm):
    def solve(self, gallery: Gallery, show: Show, evaluator: Evaluator) -> LayoutState:
        state = LayoutState(len(show.artworks))
        state.algorithm_name = self.name()

        if not gallery.zones:
            evaluator.evaluate(state, gallery, show)
            return state

        for i in range(len(show.artworks)):
            state.placement[i] = random.randint(0, len(gallery.zones) - 1)

        evaluator.evaluate(state, gallery, show)
        return state

    def name(self) -> str:
        return "random"
