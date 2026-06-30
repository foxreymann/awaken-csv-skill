"""Validate JSON config files: syntax, required fields, consistency."""
import json
import os
import unittest

REPO_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)

MARKETPLACE_PATH = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")
PLUGIN_PATH = os.path.join(
    REPO_ROOT, "plugins", "awaken-csv", ".claude-plugin", "plugin.json"
)


class TestMarketplaceJson(unittest.TestCase):
    def setUp(self):
        with open(MARKETPLACE_PATH) as f:
            self.data = json.load(f)

    def test_valid_json(self):
        self.assertIsInstance(self.data, dict)

    def test_has_name(self):
        self.assertIn("name", self.data)
        self.assertIsInstance(self.data["name"], str)
        self.assertGreater(len(self.data["name"]), 0)

    def test_has_owner(self):
        self.assertIn("owner", self.data)
        self.assertIn("name", self.data["owner"])

    def test_has_plugins_list(self):
        self.assertIn("plugins", self.data)
        self.assertIsInstance(self.data["plugins"], list)
        self.assertGreater(len(self.data["plugins"]), 0)

    def test_plugin_entries_have_required_fields(self):
        for plugin in self.data["plugins"]:
            for field in ("name", "source", "description"):
                self.assertIn(
                    field, plugin, f"Plugin entry missing '{field}': {plugin}"
                )

    def test_plugin_source_paths_exist(self):
        for plugin in self.data["plugins"]:
            source_path = os.path.join(REPO_ROOT, plugin["source"])
            self.assertTrue(
                os.path.isdir(source_path),
                f"Plugin source directory not found: {source_path}",
            )


class TestPluginJson(unittest.TestCase):
    def setUp(self):
        with open(PLUGIN_PATH) as f:
            self.data = json.load(f)

    def test_valid_json(self):
        self.assertIsInstance(self.data, dict)

    def test_has_name(self):
        self.assertIn("name", self.data)
        self.assertEqual(self.data["name"], "awaken-csv")

    def test_has_display_name(self):
        self.assertIn("displayName", self.data)
        self.assertIsInstance(self.data["displayName"], str)

    def test_has_description(self):
        self.assertIn("description", self.data)
        self.assertGreater(len(self.data["description"]), 0)

    def test_has_version(self):
        self.assertIn("version", self.data)
        parts = self.data["version"].split(".")
        self.assertEqual(len(parts), 3, f"Version not semver: {self.data['version']}")
        for part in parts:
            self.assertTrue(part.isdigit(), f"Non-numeric version part: {part}")

    def test_has_author(self):
        self.assertIn("author", self.data)
        self.assertIn("name", self.data["author"])

    def test_has_license(self):
        self.assertIn("license", self.data)

    def test_has_keywords(self):
        self.assertIn("keywords", self.data)
        self.assertIsInstance(self.data["keywords"], list)
        self.assertGreater(len(self.data["keywords"]), 0)


class TestConfigConsistency(unittest.TestCase):
    def setUp(self):
        with open(MARKETPLACE_PATH) as f:
            self.marketplace = json.load(f)
        with open(PLUGIN_PATH) as f:
            self.plugin = json.load(f)

    def test_plugin_name_matches_marketplace(self):
        marketplace_names = {p["name"] for p in self.marketplace["plugins"]}
        self.assertIn(self.plugin["name"], marketplace_names)

    def test_owner_matches(self):
        self.assertEqual(
            self.marketplace["owner"]["name"], self.plugin["author"]["name"]
        )


if __name__ == "__main__":
    unittest.main()
