"""Command-line interface for toxicity detection."""

from __future__ import annotations

import argparse
import json
import sys

from toxicity_detection.detoxify_adapter import DetoxifyToxicityDetector
from toxicity_detection.filter import ToxicityFilter
from toxicity_detection.llama_guard_adapter import LlamaGuardToxicityDetector
from toxicity_detection.local_rules import LocalRuleToxicityDetector
from toxicity_detection.responses import toxicity_response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toxicity-detect",
        description="Detect toxic or unsafe text with local rules and optional model adapters.",
    )
    parser.add_argument("text", nargs="*", help="Text to analyze. Reads stdin when omitted.")
    parser.add_argument("--language", choices=["en", "es"], default="en")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output.")
    parser.add_argument(
        "--response",
        action="store_true",
        help="Include a deterministic response when unsafe text is detected.",
    )
    parser.add_argument(
        "--fail-on-unsafe",
        action="store_true",
        help="Return exit code 2 when the input is flagged.",
    )
    parser.add_argument(
        "--no-local-rules",
        action="store_true",
        help="Disable the packaged local rule detector.",
    )
    parser.add_argument(
        "--detoxify",
        action="store_true",
        help="Add the optional Detoxify detector.",
    )
    parser.add_argument("--detoxify-model-type", default="multilingual")
    parser.add_argument("--detoxify-checkpoint", default=None)
    parser.add_argument(
        "--llama-guard-model",
        default=None,
        help="Add a Llama Guard-style Hugging Face model by model id or local path.",
    )
    parser.add_argument("--device", default=None, help="Torch device for Llama Guard, e.g. cpu.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    text = _read_text(args.text)
    if not text:
        parser.error("provide text as an argument or through stdin")

    detectors = []
    if not args.no_local_rules:
        detectors.append(LocalRuleToxicityDetector.from_package_data())
    if args.detoxify:
        try:
            detectors.append(
                DetoxifyToxicityDetector(
                    model_type=args.detoxify_model_type,
                    checkpoint=args.detoxify_checkpoint,
                )
            )
        except ImportError as exc:
            parser.error(str(exc))
    if args.llama_guard_model:
        try:
            detectors.append(
                LlamaGuardToxicityDetector(
                    model_id=args.llama_guard_model,
                    device=args.device,
                )
            )
        except ImportError as exc:
            parser.error(str(exc))
    if not detectors:
        parser.error("enable at least one detector")

    result = ToxicityFilter(detectors=detectors).check(text)
    _print_result(result, language=args.language, as_json=args.as_json, include_response=args.response)
    return 2 if args.fail_on_unsafe and result.flagged else 0


def _read_text(parts: list[str]) -> str:
    if parts:
        return " ".join(parts).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def _print_result(result, *, language: str, as_json: bool, include_response: bool) -> None:
    response = None
    if include_response and result.flagged:
        response = toxicity_response(result.category, language=language)

    if as_json:
        payload = result.to_dict()
        if response is not None:
            payload["response"] = response
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return

    if not result.flagged:
        print("safe")
        return

    fields = [
        "unsafe",
        result.category.value,
        result.source,
        f"score={result.score:.4f}",
    ]
    if result.matched_text:
        fields.append(f"match={result.matched_text}")
    print("\t".join(fields))
    if response is not None:
        print(response)


if __name__ == "__main__":
    raise SystemExit(main())
