import unittest

from toxicity_detection import ToxicityCategory, ToxicityFilter, toxicity_response


class ToxicityFilterTest(unittest.TestCase):
    def test_safe_text_is_not_flagged(self) -> None:
        result = ToxicityFilter.default().check("Hola, me gustaria hablar de musica.")

        self.assertFalse(result.flagged)
        self.assertEqual(result.category, ToxicityCategory.SAFE)

    def test_spanish_insult_is_flagged(self) -> None:
        result = ToxicityFilter.default().check("Por favor, callate.")

        self.assertTrue(result.flagged)
        self.assertEqual(result.category, ToxicityCategory.INSULT)

    def test_threat_is_flagged(self) -> None:
        result = ToxicityFilter.default().check("Voy a atacarte.")

        self.assertTrue(result.flagged)
        self.assertEqual(result.category, ToxicityCategory.THREAT)

    def test_filter_candidates_keeps_only_safe_text(self) -> None:
        candidates = [
            "Hablemos de musica.",
            "Por favor, callate.",
            "Me gusta esta conversacion.",
        ]

        safe_candidates = ToxicityFilter.default().filter_candidates(candidates)

        self.assertEqual(safe_candidates, ["Hablemos de musica.", "Me gusta esta conversacion."])

    def test_response_rejects_safe_category(self) -> None:
        with self.assertRaises(ValueError):
            toxicity_response(ToxicityCategory.SAFE)


if __name__ == "__main__":
    unittest.main()
