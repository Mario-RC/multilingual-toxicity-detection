import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

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


if __name__ == "__main__":
    unittest.main()
