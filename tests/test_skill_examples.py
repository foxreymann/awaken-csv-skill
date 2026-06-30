"""Validate SKILL.md CSV examples: parse correctly, conform to template headers."""
import csv
import io
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

ASSETS_DIR = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "plugins",
    "awaken-csv",
    "skills",
    "awaken-csv",
    "assets",
)


def _load_template_headers(filename):
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return next(reader)


def _extract_csv_blocks(skill_path):
    """Extract CSV code blocks from SKILL.md, returning (label, header, data_rows)."""
    with open(skill_path) as f:
        text = f.read()
    blocks = []
    # Find labeled examples: **Label — ...**\n```\n...\n```
    pattern = re.compile(
        r"\*\*([^*]+)\*\*[^\n]*\n```\n(.*?)```", re.DOTALL
    )
    for match in pattern.finditer(text):
        label = match.group(1).strip()
        block_text = match.group(2).strip()
        lines = list(csv.reader(io.StringIO(block_text)))
        if len(lines) >= 2:
            blocks.append((label, lines[0], lines[1:]))
    return blocks


class TestSkillExamplesParseable(unittest.TestCase):
    def setUp(self):
        self.blocks = _extract_csv_blocks(SKILL_PATH)

    def test_examples_found(self):
        self.assertGreater(len(self.blocks), 0, "No CSV examples found in SKILL.md")

    def test_each_example_has_header_and_data(self):
        for label, header, data_rows in self.blocks:
            self.assertGreater(len(header), 0, f"Empty header in example '{label}'")
            self.assertGreater(
                len(data_rows), 0, f"No data rows in example '{label}'"
            )


class TestStandardExamples(unittest.TestCase):
    def setUp(self):
        self.template_header = _load_template_headers("template_standard.csv")
        self.blocks = _extract_csv_blocks(SKILL_PATH)
        self.standard_blocks = [
            (label, header, rows)
            for label, header, rows in self.blocks
            if "Standard" in label and "Multi" not in label and "Futures" not in label
        ]

    def test_standard_examples_exist(self):
        self.assertGreater(len(self.standard_blocks), 0)

    def test_standard_headers_match_template(self):
        for label, header, _ in self.standard_blocks:
            self.assertEqual(
                header,
                self.template_header,
                f"Standard example '{label}' header mismatch",
            )

    def test_standard_data_column_count(self):
        expected_cols = len(self.template_header)
        for label, _, rows in self.standard_blocks:
            for i, row in enumerate(rows):
                self.assertEqual(
                    len(row),
                    expected_cols,
                    f"Standard example '{label}' row {i+1}: "
                    f"expected {expected_cols} cols, got {len(row)}",
                )

    def test_standard_date_not_empty(self):
        for label, _, rows in self.standard_blocks:
            for row in rows:
                self.assertTrue(
                    row[0].strip(), f"Empty date in standard example '{label}'"
                )


class TestMultiAssetExamples(unittest.TestCase):
    def setUp(self):
        self.template_header = _load_template_headers("template_multi_asset.csv")
        self.blocks = _extract_csv_blocks(SKILL_PATH)
        self.ma_blocks = [
            (label, header, rows)
            for label, header, rows in self.blocks
            if "Multi-asset" in label or "Multi asset" in label
        ]

    def test_multi_asset_examples_exist(self):
        self.assertGreater(len(self.ma_blocks), 0)

    def test_multi_asset_headers_match_template(self):
        for label, header, _ in self.ma_blocks:
            self.assertEqual(
                header,
                self.template_header,
                f"Multi-asset example '{label}' header mismatch",
            )

    def test_multi_asset_data_column_count(self):
        expected_cols = len(self.template_header)
        for label, _, rows in self.ma_blocks:
            for i, row in enumerate(rows):
                self.assertEqual(
                    len(row),
                    expected_cols,
                    f"Multi-asset example '{label}' row {i+1}: "
                    f"expected {expected_cols} cols, got {len(row)}",
                )


class TestFuturesExamples(unittest.TestCase):
    def setUp(self):
        self.template_header = _load_template_headers("template_futures.csv")
        self.blocks = _extract_csv_blocks(SKILL_PATH)
        self.futures_blocks = [
            (label, header, rows)
            for label, header, rows in self.blocks
            if "Futures" in label or "futures" in label
        ]

    def test_futures_examples_exist(self):
        self.assertGreater(len(self.futures_blocks), 0)

    def test_futures_headers_match_template(self):
        for label, header, _ in self.futures_blocks:
            self.assertEqual(
                header,
                self.template_header,
                f"Futures example '{label}' header mismatch",
            )

    def test_futures_data_column_count(self):
        expected_cols = len(self.template_header)
        for label, _, rows in self.futures_blocks:
            for i, row in enumerate(rows):
                self.assertEqual(
                    len(row),
                    expected_cols,
                    f"Futures example '{label}' row {i+1}: "
                    f"expected {expected_cols} cols, got {len(row)}",
                )


class TestExampleDateFormats(unittest.TestCase):
    """Dates in examples should be in a valid Awaken format."""

    AWAKEN_DATE_RE = re.compile(
        r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$"  # MM/DD/YYYY HH:MM:SS
    )
    ISO_DATE_RE = re.compile(
        r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z?)?$"
    )

    def setUp(self):
        self.blocks = _extract_csv_blocks(SKILL_PATH)

    def test_dates_are_valid_format(self):
        for label, header, rows in self.blocks:
            for row in rows:
                date_val = row[0].strip()
                valid = (
                    self.AWAKEN_DATE_RE.match(date_val)
                    or self.ISO_DATE_RE.match(date_val)
                )
                self.assertTrue(
                    valid,
                    f"Invalid date '{date_val}' in example '{label}'",
                )


class TestExampleNoNegativeQuantities(unittest.TestCase):
    """Standard and multi-asset examples must not have negative quantities (except P&L)."""

    QUANTITY_COLS_STANDARD = [
        "Received Quantity",
        "Sent Quantity",
        "Fee Amount",
    ]

    def setUp(self):
        self.blocks = _extract_csv_blocks(SKILL_PATH)

    def test_no_negatives_in_standard(self):
        for label, header, rows in self.blocks:
            if "Futures" in label or "futures" in label:
                continue
            for col_name in self.QUANTITY_COLS_STANDARD:
                if col_name not in header:
                    continue
                idx = header.index(col_name)
                for row in rows:
                    val = row[idx].strip()
                    if val:
                        self.assertFalse(
                            val.startswith("-"),
                            f"Negative {col_name} '{val}' in example '{label}'",
                        )


if __name__ == "__main__":
    unittest.main()
