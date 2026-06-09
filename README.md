# Toxicity Detection

Standalone multilingual toxicity detection package extracted from the affective dialogue system. It provides a fast local rule-based detector by default and optional adapters for heavier moderation models such as Detoxify and Llama Guard.

The package is designed to stay lightweight on import: local rules run without model downloads, and ML dependencies are loaded only when their adapters are instantiated.

## Features

- Local deterministic checks for insults, threats, self-harm, explicit sexual content, criminal planning, illegal weapons, regulated substances, and prohibited terms.
- Spanish and English canned safety responses.
- Optional Detoxify adapter with configurable thresholds.
- Optional Llama Guard-style adapter for Hugging Face causal language models.
- Python API, command-line interface, tests, and CI-ready project metadata.

## Installation

```bash
python -m pip install -e ".[dev]"
```

Install optional model adapters only when needed:

```bash
python -m pip install -e ".[detoxify]"
python -m pip install -e ".[llama-guard]"
```

## CLI

Run the default local detector:

Spanish:

```bash
toxicity-detect "Hola, me gustaria hablar de musica."
toxicity-detect "Por favor, callate." --language es --response
```

English:

```bash
toxicity-detect "I would like to talk about music." --language en
toxicity-detect "Please shut up." --language en --response
```

JSON output is available for integration:

```bash
toxicity-detect "Por favor, callate." --language es --json --response
toxicity-detect "Please shut up." --language en --json --response
```

The CLI also reads from standard input:

```bash
printf "texto a revisar" | toxicity-detect --json
printf "text to review" | toxicity-detect --language en --json
```

## Python API

Spanish:

```python
from toxicity_detection import ToxicityCategory, ToxicityFilter, toxicity_response

detector = ToxicityFilter.default()
result = detector.check("Por favor, callate.")

if result.flagged:
    print(result.category)
    print(toxicity_response(result.category, language="es"))
else:
    print(ToxicityCategory.SAFE)
```

English:

```python
from toxicity_detection import ToxicityCategory, ToxicityFilter, toxicity_response

detector = ToxicityFilter.default()
result = detector.check("Please shut up.")

if result.flagged:
    print(result.category)
    print(toxicity_response(result.category, language="en"))
else:
    print(ToxicityCategory.SAFE)
```

Compose detectors explicitly when using optional models:

```python
from toxicity_detection import LocalRuleToxicityDetector, ToxicityFilter
from toxicity_detection.detoxify_adapter import DetoxifyToxicityDetector

detector = ToxicityFilter(
    detectors=[
        LocalRuleToxicityDetector.from_package_data(),
        DetoxifyToxicityDetector(model_type="multilingual"),
    ]
)
```

## Repository Layout

```text
src/toxicity_detection/    importable Python package
src/toxicity_detection/data packaged rule lists
tests/                     unit tests
examples/                  minimal usage examples
docs/                      architecture and adapter notes
```

## Responsible Use

Toxicity detection is probabilistic and context-sensitive, even when local rules are deterministic. Use this package as a safety signal, not as the only authority for moderation decisions. Review false positives and false negatives for the domain where it will be deployed.

## License

See `LICENSE`.
