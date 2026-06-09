"""Toxicity filter that combines local rules and optional model detectors."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

from toxicity_detection.local_rules import LocalRuleToxicityDetector
from toxicity_detection.schemas import ToxicityResult


class ToxicityDetector(Protocol):
    def check(self, text: str) -> ToxicityResult:
        """Return a toxicity result for ``text``."""


@dataclass
class ToxicityFilter:
    """Run toxicity detectors in priority order."""

    detectors: list[ToxicityDetector] = field(default_factory=list)

    @classmethod
    def default(cls) -> "ToxicityFilter":
        return cls(detectors=[LocalRuleToxicityDetector.from_package_data()])

    def check(self, text: str) -> ToxicityResult:
        for detector in self.detectors:
            result = detector.check(text)
            if result.flagged:
                return result
        return ToxicityResult.safe()

    def filter_candidates(self, candidates: Iterable[str]) -> list[str]:
        return [candidate for candidate in candidates if not self.check(candidate).flagged]


SafetyDetector = ToxicityDetector
SafetyFilter = ToxicityFilter

