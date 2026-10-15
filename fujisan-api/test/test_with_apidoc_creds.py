import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "with-apidoc-creds.sh"
CREDS = "APIDOC_BASIC_USERNAME=user\nAPIDOC_BASIC_PASSWORD=secret\n"


class WithApidocCreds(unittest.TestCase):
    def run_wrapper(self, mode, body):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / "apidoc.env"
            env_file.write_text(body, encoding="utf-8")
            os.chmod(env_file, mode)
            return subprocess.run(
                [SCRIPT, "true"],
                env={**os.environ, "APIDOC_ENV_FILE": str(env_file)},
                capture_output=True,
                text=True,
                check=False,
            )

    def test_owner_only_modes_are_accepted(self):
        for mode in (0o600, 0o400):
            with self.subTest(oct(mode)):
                result = self.run_wrapper(mode, CREDS)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_group_or_other_read_is_rejected_with_the_mode_alone(self):
        # Not valid shell. Sourcing it would fail before the mode error.
        result = self.run_wrapper(0o644, "this is not shell\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("is mode 644 and is readable beyond its owner", result.stderr)
        self.assertNotIn("File:", result.stderr)
        self.assertNotIn("Block size", result.stderr)


if __name__ == "__main__":
    unittest.main()
