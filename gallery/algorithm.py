from __future__ import annotations

from gallery.algorithms.greedy import GreedyAlgorithm
from gallery.algorithms.random_algorithm import RandomAlgorithm
from gallery.base import Algorithm
from gallery.util import trim


def create_algorithm(name: str) -> Algorithm:
    lowered = trim(name).lower()
    if lowered == "greedy":
        return GreedyAlgorithm()
    if lowered == "random":
        return RandomAlgorithm()
    raise RuntimeError(f"Unknown algorithm: {name}. Supported: greedy, random")
