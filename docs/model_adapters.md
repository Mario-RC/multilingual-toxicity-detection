# Model Adapters

The default package has no heavyweight runtime dependencies. Model-backed detectors live behind optional extras.

## Detoxify

Install:

```bash
python -m pip install -e ".[detoxify]"
```

Usage:

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

Thresholds can be overridden by passing a dictionary to `DetoxifyToxicityDetector(thresholds=...)`.

## Llama Guard

Install:

```bash
python -m pip install -e ".[llama-guard]"
```

Usage:

```python
from toxicity_detection.llama_guard_adapter import LlamaGuardToxicityDetector

detector = LlamaGuardToxicityDetector(
    model_id="meta-llama/Meta-Llama-Guard-2-8B",
    device="cuda:0",
)
```

The model is loaded during detector construction, not at package import time.

