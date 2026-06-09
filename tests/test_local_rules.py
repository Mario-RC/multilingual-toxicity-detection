import unittest

from toxicity_detection import LocalRuleToxicityDetector, ToxicityCategory


class LocalRulesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = LocalRuleToxicityDetector.from_package_data()

    def test_prohibited_terms_are_loaded_from_package_data(self) -> None:
        self.assertGreater(len(self.detector.prohibited_terms), 100)
        self.assertGreater(len(self.detector.offensive_phrases), 100)

    def test_punctuation_variant_is_detected(self) -> None:
        result = self.detector.check("Por favor, callate!!!")

        self.assertTrue(result.flagged)
        self.assertEqual(result.category, ToxicityCategory.INSULT)

    def test_whitelisted_movie_title_is_not_flagged(self) -> None:
        result = self.detector.check("I watched Kill Bill yesterday.")

        self.assertFalse(result.flagged)

    def test_result_serializes_to_plain_values(self) -> None:
        result = self.detector.check("Voy a atacarte.")

        payload = result.to_dict()

        self.assertTrue(payload["flagged"])
        self.assertEqual(payload["category"], "threat")


if __name__ == "__main__":
    unittest.main()
