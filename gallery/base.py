from __future__ import annotations

from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def solve(self, gallery, show, evaluator):
        raise NotImplementedError

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
