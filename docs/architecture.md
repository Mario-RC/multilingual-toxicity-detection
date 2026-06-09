# Architecture

The package is intentionally small and split into independently testable modules:

- `schemas`: enum and result dataclass shared by every detector.
- `local_rules`: deterministic multilingual pattern checks plus optional user-provided phrase files.
- `filter`: priority-ordered composition of detectors.
- `responses`: deterministic Spanish and English responses for flagged categories.
- `detoxify_adapter`: optional Detoxify integration, loaded only when instantiated.
- `llama_guard_adapter`: optional Hugging Face Llama Guard-style integration, loaded only when instantiated.
- `cli`: command-line entry point for local usage and shell integration.

## Detection Flow

`ToxicityFilter` receives a list of detector objects. Each detector implements `check(text) -> ToxicityResult`.

The default filter uses only `LocalRuleToxicityDetector.from_package_data()`, so it does not download models or import torch. Optional model adapters can be appended after local rules to keep deterministic checks fast and use ML models only as a second pass.

## Packaging

Curated rule lists are not distributed with the repository. Projects that need broader lexical coverage should provide their own newline-delimited `.txt` files and load them with `LocalRuleToxicityDetector.from_files(...)` or the matching CLI flags.

## Stability Notes

The API favors plain dataclasses and enums. `ToxicityResult.to_dict()` returns JSON-safe primitive values for service boundaries, logs, and CLI output.
