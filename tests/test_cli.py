import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from tempfile import NamedTemporaryFile

from toxicity_detection.cli import main


class CliTest(unittest.TestCase):
    def test_json_output_for_safe_text(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["hola", "--json"])

        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertFalse(payload["flagged"])
        self.assertEqual(payload["category"], "safe")

    def test_fail_on_unsafe_returns_two(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["Por favor, callate.", "--fail-on-unsafe"])

        self.assertEqual(exit_code, 2)
        self.assertIn("unsafe", output.getvalue())

    def test_custom_prohibited_terms_file(self) -> None:
        output = StringIO()
        with NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write("customblockedphrase\n")
            handle.flush()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "customblockedphrase",
                        "--prohibited-terms-file",
                        handle.name,
                        "--json",
                    ]
                )

        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertTrue(payload["flagged"])
        self.assertEqual(payload["matched_text"], "customblockedphrase")


if __name__ == "__main__":
    unittest.main()
