"""Minimal API example."""

from toxicity_detection import ToxicityFilter, toxicity_response


def main() -> None:
    detector = ToxicityFilter.default()
    examples = [
        ("es", "Por favor, callate."),
        ("en", "Please shut up."),
    ]

    for language, text in examples:
        result = detector.check(text)
        print(f"[{language}] {text}")
        print(result.to_dict())
        if result.flagged:
            print(toxicity_response(result.category, language=language))
        print()


if __name__ == "__main__":
    main()
