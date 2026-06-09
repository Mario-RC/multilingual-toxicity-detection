import unittest
from tempfile import NamedTemporaryFile

from toxicity_detection import LocalRuleToxicityDetector, ToxicityCategory


class LocalRulesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = LocalRuleToxicityDetector.from_package_data()

    def test_default_detector_does_not_require_packaged_word_lists(self) -> None:
        self.assertIsInstance(self.detector.prohibited_terms, set)
        self.assertIsInstance(self.detector.offensive_phrases, set)

    def test_custom_prohibited_terms_file_is_loaded(self) -> None:
        with NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write("customblockedphrase\n")
            handle.flush()
            detector = LocalRuleToxicityDetector.from_files(prohibited_terms_path=handle.name)

        result = detector.check("This contains customblockedphrase.")

        self.assertTrue(result.flagged)
        self.assertEqual(result.category, ToxicityCategory.PROHIBITED_TERM)
        self.assertEqual(result.matched_text, "customblockedphrase")

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
