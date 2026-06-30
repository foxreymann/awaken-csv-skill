"""Validate SKILL.md structure: frontmatter, required sections, internal references."""
import os
import re
import unittest

SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "plugins",
    "awaken-csv",
    "skills",
    "awaken-csv",
    "SKILL.md",
)

SKILL_DIR = os.path.dirname(SKILL_PATH)


class TestSkillMdExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(os.path.isfile(SKILL_PATH))


class TestSkillMdFrontmatter(unittest.TestCase):
    def setUp(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_has_frontmatter(self):
        self.assertTrue(
            self.content.startswith("---"),
            "SKILL.md should start with YAML frontmatter",
        )

    def test_frontmatter_has_name(self):
        fm_match = re.match(r"---\n(.*?)---", self.content, re.DOTALL)
        self.assertIsNotNone(fm_match, "Could not parse frontmatter")
        fm = fm_match.group(1)
        self.assertIn("name:", fm)

    def test_frontmatter_has_description(self):
        fm_match = re.match(r"---\n(.*?)---", self.content, re.DOTALL)
        self.assertIsNotNone(fm_match)
        fm = fm_match.group(1)
        self.assertIn("description:", fm)


class TestSkillMdSections(unittest.TestCase):
    def setUp(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_has_format_table(self):
        self.assertIn(
            "Standard",
            self.content,
            "SKILL.md should mention Standard format",
        )
        self.assertIn(
            "Multi-asset",
            self.content,
            "SKILL.md should mention Multi-asset format",
        )
        self.assertIn(
            "Futures",
            self.content,
            "SKILL.md should mention Futures format",
        )

    def test_has_rules_section(self):
        self.assertIn("## Rules", self.content)

    def test_has_workflow_section(self):
        self.assertIn("## Workflow", self.content)

    def test_has_examples_section(self):
        self.assertIn("## Examples", self.content)

    def test_has_companion_findings_section(self):
        self.assertIn("## Companion findings", self.content)


class TestSkillMdInternalReferences(unittest.TestCase):
    """Verify that file paths referenced in SKILL.md actually exist."""

    def setUp(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_template_references_exist(self):
        template_refs = re.findall(r"`(assets/template_\w+\.csv)`", self.content)
        self.assertGreater(len(template_refs), 0, "No template references found")
        for ref in template_refs:
            path = os.path.join(SKILL_DIR, ref)
            self.assertTrue(
                os.path.isfile(path), f"Referenced template not found: {ref}"
            )

    def test_reference_doc_refs_exist(self):
        ref_refs = re.findall(r"`(references/[\w-]+\.md)`", self.content)
        self.assertGreater(len(ref_refs), 0, "No reference doc references found")
        for ref in ref_refs:
            path = os.path.join(SKILL_DIR, ref)
            self.assertTrue(
                os.path.isfile(path), f"Referenced doc not found: {ref}"
            )


class TestSkillMdDateRules(unittest.TestCase):
    """Verify the date format rules are documented."""

    def setUp(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_mentions_utc(self):
        self.assertIn("UTC", self.content)

    def test_mentions_date_format(self):
        self.assertTrue(
            "MM/DD/YYYY" in self.content or "ISO 8601" in self.content,
            "SKILL.md should document the date format",
        )


class TestSkillMdNegativeNumberRule(unittest.TestCase):
    def setUp(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_mentions_no_negatives(self):
        self.assertTrue(
            "negative" in self.content.lower() or "No negative" in self.content,
            "SKILL.md should mention the no-negative-numbers rule",
        )

    def test_mentions_pl_exception(self):
        self.assertIn(
            "P&L",
            self.content,
            "SKILL.md should mention P&L as an exception to the no-negatives rule",
        )


if __name__ == "__main__":
    unittest.main()
