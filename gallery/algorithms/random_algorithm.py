from __future__ import annotations

import random

from gallery.base import Algorithm
from gallery.models import LayoutState


class RandomAlgorithm(Algorithm):
    def solve(self, gallery, show, evaluator):
        state = LayoutState(len(show.artworks))
        state.algorithm_name = self.name()

        if not gallery.zones:
            evaluator.evaluate(state, gallery, show)
            return state

        for artwork_index, _artwork in enumerate(show.artworks):
            state.placement[artwork_index] = random.randint(0, len(gallery.zones) - 1)

        evaluator.evaluate(state, gallery, show)
        return state

    def name(self) -> str:
        return "random"
