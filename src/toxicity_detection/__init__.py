"""Multilingual toxicity detection package."""

from toxicity_detection.detoxify_adapter import DetoxifyToxicityDetector
from toxicity_detection.filter import ToxicityDetector, ToxicityFilter
from toxicity_detection.llama_guard_adapter import LlamaGuardToxicityDetector
from toxicity_detection.local_rules import LocalRuleToxicityDetector
from toxicity_detection.responses import safety_response, toxicity_response
from toxicity_detection.schemas import ToxicityCategory, ToxicityResult

SafetyCategory = ToxicityCategory
SafetyResult = ToxicityResult
SafetyFilter = ToxicityFilter
LocalRuleSafetyDetector = LocalRuleToxicityDetector
DetoxifySafetyDetector = DetoxifyToxicityDetector
LlamaGuardSafetyDetector = LlamaGuardToxicityDetector

__all__ = [
    "DetoxifySafetyDetector",
    "DetoxifyToxicityDetector",
    "LlamaGuardSafetyDetector",
    "LlamaGuardToxicityDetector",
    "LocalRuleSafetyDetector",
    "LocalRuleToxicityDetector",
    "SafetyCategory",
    "SafetyFilter",
    "SafetyResult",
    "ToxicityCategory",
    "ToxicityDetector",
    "ToxicityFilter",
    "ToxicityResult",
    "safety_response",
    "toxicity_response",
]

__version__ = "0.1.0"

