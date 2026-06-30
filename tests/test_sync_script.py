"""Validate sync.sh: bash syntax, expected variables, and structure."""
import os
import subprocess
import unittest

REPO_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
SYNC_PATH = os.path.join(REPO_ROOT, "sync.sh")


class TestSyncScriptExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(os.path.isfile(SYNC_PATH))

    def test_is_executable_or_has_shebang(self):
        with open(SYNC_PATH) as f:
            first_line = f.readline().strip()
        self.assertTrue(
            first_line.startswith("#!"),
            f"sync.sh should start with a shebang, got: {first_line}",
        )

    def test_shebang_is_bash(self):
        with open(SYNC_PATH) as f:
            first_line = f.readline().strip()
        self.assertIn("bash", first_line, "sync.sh shebang should reference bash")


class TestSyncScriptSyntax(unittest.TestCase):
    def test_bash_syntax_check(self):
        result = subprocess.run(
            ["bash", "-n", SYNC_PATH],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"Bash syntax error in sync.sh: {result.stderr}",
        )


class TestSyncScriptContent(unittest.TestCase):
    def setUp(self):
        with open(SYNC_PATH) as f:
            self.content = f.read()

    def test_uses_set_euo_pipefail(self):
        self.assertIn("set -euo pipefail", self.content)

    def test_references_source_variable(self):
        self.assertIn("SOURCE", self.content)

    def test_references_dest_variable(self):
        self.assertIn("DEST", self.content)

    def test_uses_rsync(self):
        self.assertIn("rsync", self.content)

    def test_dest_points_to_plugin_skill_dir(self):
        self.assertIn(
            "plugins/awaken-csv/skills/awaken-csv",
            self.content,
            "DEST should point to the plugin skill directory",
        )

    def test_checks_source_exists(self):
        self.assertIn(
            '[ -d "$SOURCE" ]',
            self.content,
            "Script should check that SOURCE directory exists",
        )


if __name__ == "__main__":
    unittest.main()
