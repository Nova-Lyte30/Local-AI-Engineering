"""Regression tests for the byte-precise Cline file quality gate."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "agent-file-guard.py"
EXPECTED = b'print("AGENT_P0_EDIT_OK")\n'


class AgentFileGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "isolated"
        self.root.mkdir()
        self.file = self.root / "probe.py"

    def check(self, *extra, target=None):
        return subprocess.run(
            [
                sys.executable, "-B", str(SCRIPT),
                "--root", str(self.root),
                "--file", str(target or self.file),
                "--expected-print", "AGENT_P0_EDIT_OK",
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_exact_file_passes_without_changes(self):
        self.file.write_bytes(EXPECTED)
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.file.read_bytes(), EXPECTED)

    def test_missing_final_lf_requires_explicit_repair(self):
        self.file.write_bytes(EXPECTED[:-1])
        self.assertEqual(self.check().returncode, 1)
        result = self.check("--normalize-newline")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.file.read_bytes(), EXPECTED)

    def test_wrong_source_is_not_overwritten(self):
        old = b'print("UNRELATED")'
        self.file.write_bytes(old)
        self.assertEqual(self.check("--normalize-newline").returncode, 1)
        self.assertEqual(self.file.read_bytes(), old)

    def test_outside_root_is_rejected(self):
        external = Path(self.temp.name) / "outside.py"
        original = b'print("OUTSIDE")'
        external.write_bytes(original)
        self.assertEqual(self.check("--normalize-newline", target=external).returncode, 2)
        self.assertEqual(external.read_bytes(), original)

    def test_utf8_bom_can_be_removed_when_body_matches(self):
        self.file.write_bytes(b"\xef\xbb\xbf" + EXPECTED)
        self.assertEqual(self.check("--normalize-newline").returncode, 0)
        self.assertEqual(self.file.read_bytes(), EXPECTED)


if __name__ == "__main__":
    unittest.main()
