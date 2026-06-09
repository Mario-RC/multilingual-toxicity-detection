"""Minimal API example."""

from toxicity_detection import ToxicityFilter, toxicity_response


def main() -> None:
    detector = ToxicityFilter.default()
    result = detector.check("Por favor, callate.")
    print(result.to_dict())
    if result.flagged:
        print(toxicity_response(result.category, language="es"))


if __name__ == "__main__":
    main()
