"""Validate tag enum consistency across SKILL.md and labels-and-spec.md."""
import os
import re
import unittest

REFS_DIR = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "plugins",
    "awaken-csv",
    "skills",
    "awaken-csv",
    "references",
)

SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "plugins",
    "awaken-csv",
    "skills",
    "awaken-csv",
    "SKILL.md",
)

LABELS_PATH = os.path.join(REFS_DIR, "labels-and-spec.md")


def _extract_enum_tags(labels_path):
    """Extract tag enum values from the code block in labels-and-spec.md."""
    with open(labels_path) as f:
        text = f.read()
    pattern = re.compile(r'"(\w+)"\s*$', re.MULTILINE)
    block_match = re.search(
        r"```\n(.*?)```", text, re.DOTALL
    )
    if not block_match:
        return set()
    block = block_match.group(1)
    return set(pattern.findall(block))


def _extract_tags_from_skill_examples(skill_path):
    """Extract tags used in SKILL.md CSV examples."""
    with open(skill_path) as f:
        text = f.read()
    tags = set()
    csv_blocks = re.findall(r"```\n(.*?)```", text, re.DOTALL)
    for block in csv_blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        header = lines[0].split(",")
        try:
            tag_idx = header.index("Tag")
        except ValueError:
            continue
        for data_line in lines[1:]:
            cols = data_line.split(",")
            if tag_idx < len(cols) and cols[tag_idx].strip():
                tags.add(cols[tag_idx].strip())
    return tags


def _extract_tags_from_skill_prose(skill_path):
    """Extract tags mentioned in backtick-quoted references in SKILL.md."""
    with open(skill_path) as f:
        text = f.read()
    return set(re.findall(r"`(\w+(?:_\w+)+)`", text))


class TestTagEnumValues(unittest.TestCase):
    def setUp(self):
        self.enum_tags = _extract_enum_tags(LABELS_PATH)

    def test_enum_tags_not_empty(self):
        self.assertGreater(len(self.enum_tags), 0, "No tags parsed from labels-and-spec.md")

    def test_known_tags_present(self):
        expected = {
            "swap",
            "coin_buy",
            "coin_sell",
            "airdrop",
            "income",
            "staking",
            "add_liquidity",
            "remove_liquidity",
            "open_position",
            "close_position",
            "funding_payment",
            "internal_transfer",
            "non_taxable",
            "spam",
        }
        for tag in expected:
            self.assertIn(tag, self.enum_tags, f"Expected tag '{tag}' missing from enum")

    def test_no_duplicate_display_names(self):
        with open(LABELS_PATH) as f:
            text = f.read()
        block_match = re.search(r"```\n(.*?)```", text, re.DOTALL)
        self.assertIsNotNone(block_match)
        lines = [
            line.strip()
            for line in block_match.group(1).strip().split("\n")
            if line.strip()
        ]
        display_names = []
        for line in lines:
            m = re.match(r'^"([^"]+)"\s*=', line)
            if m:
                display_names.append(m.group(1))
        self.assertEqual(
            len(display_names),
            len(set(display_names)),
            f"Duplicate display names: {[n for n in display_names if display_names.count(n) > 1]}",
        )

    def test_no_duplicate_enum_values(self):
        with open(LABELS_PATH) as f:
            text = f.read()
        block_match = re.search(r"```\n(.*?)```", text, re.DOTALL)
        self.assertIsNotNone(block_match)
        enum_values = re.findall(r'=\s*"(\w+)"', block_match.group(1))
        self.assertEqual(
            len(enum_values),
            len(set(enum_values)),
            f"Duplicate enum values: {[v for v in enum_values if enum_values.count(v) > 1]}",
        )


class TestSkillExampleTags(unittest.TestCase):
    def setUp(self):
        self.enum_tags = _extract_enum_tags(LABELS_PATH)
        self.example_tags = _extract_tags_from_skill_examples(SKILL_PATH)

    def test_example_tags_not_empty(self):
        self.assertGreater(len(self.example_tags), 0, "No tags found in SKILL.md examples")

    def test_all_example_tags_in_enum(self):
        for tag in self.example_tags:
            self.assertIn(
                tag,
                self.enum_tags,
                f"Tag '{tag}' used in SKILL.md example but not in enum",
            )


class TestFuturesTagSubset(unittest.TestCase):
    """The futures format only accepts a specific subset of tags."""

    FUTURES_TAGS = {"open_position", "close_position", "funding_payment", "liquidation"}

    def test_futures_tags_in_enum(self):
        enum_tags = _extract_enum_tags(LABELS_PATH)
        for tag in self.FUTURES_TAGS:
            self.assertIn(tag, enum_tags, f"Futures tag '{tag}' missing from enum")

    def test_skill_futures_example_uses_valid_tags(self):
        example_tags = _extract_tags_from_skill_examples(SKILL_PATH)
        futures_used = example_tags & self.FUTURES_TAGS
        self.assertGreater(len(futures_used), 0, "No futures tags found in examples")
        for tag in futures_used:
            self.assertIn(tag, self.FUTURES_TAGS)


if __name__ == "__main__":
    unittest.main()
