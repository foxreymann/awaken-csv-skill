"""Validate CSV template files: headers, column order, and basic format."""
import csv
import os
import unittest

ASSETS_DIR = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "plugins",
    "awaken-csv",
    "skills",
    "awaken-csv",
    "assets",
)

EXPECTED_STANDARD_HEADERS = [
    "Date",
    "Received Quantity",
    "Received Currency",
    "Received Fiat Amount",
    "Sent Quantity",
    "Sent Currency",
    "Sent Fiat Amount",
    "Fee Amount",
    "Fee Currency",
    "Transaction Hash",
    "Notes",
    "Tag",
]

EXPECTED_MULTI_ASSET_HEADERS = [
    "Date",
    "Received Quantity",
    "Received Currency",
    "Received Fiat Amount",
    "Sent Quantity",
    "Sent Currency",
    "Sent Fiat Amount",
    "Received Quantity 2",
    "Received Currency 2",
    "Sent Quantity 2",
    "Sent Currency 2",
    "Fee Amount",
    "Fee Currency",
    "Notes",
    "Tag",
]

EXPECTED_FUTURES_HEADERS = [
    "Date",
    "Asset",
    "Amount",
    "Fee",
    "P&L",
    "Payment Token",
    "ID",
    "Notes",
    "Tag",
    "Transaction Hash",
]


class TestTemplateFilesExist(unittest.TestCase):
    def test_standard_template_exists(self):
        path = os.path.join(ASSETS_DIR, "template_standard.csv")
        self.assertTrue(os.path.isfile(path), f"Missing {path}")

    def test_multi_asset_template_exists(self):
        path = os.path.join(ASSETS_DIR, "template_multi_asset.csv")
        self.assertTrue(os.path.isfile(path), f"Missing {path}")

    def test_futures_template_exists(self):
        path = os.path.join(ASSETS_DIR, "template_futures.csv")
        self.assertTrue(os.path.isfile(path), f"Missing {path}")


class TestStandardTemplate(unittest.TestCase):
    def setUp(self):
        path = os.path.join(ASSETS_DIR, "template_standard.csv")
        with open(path, newline="") as f:
            reader = csv.reader(f)
            self.rows = list(reader)

    def test_header_row_present(self):
        self.assertGreaterEqual(len(self.rows), 1, "Template must have a header row")

    def test_header_columns_match(self):
        self.assertEqual(self.rows[0], EXPECTED_STANDARD_HEADERS)

    def test_no_data_rows(self):
        non_empty = [r for r in self.rows[1:] if any(cell.strip() for cell in r)]
        self.assertEqual(len(non_empty), 0, "Standard template should be header-only")


class TestMultiAssetTemplate(unittest.TestCase):
    def setUp(self):
        path = os.path.join(ASSETS_DIR, "template_multi_asset.csv")
        with open(path, newline="") as f:
            reader = csv.reader(f)
            self.rows = list(reader)

    def test_header_row_present(self):
        self.assertGreaterEqual(len(self.rows), 1)

    def test_header_columns_match(self):
        self.assertEqual(self.rows[0], EXPECTED_MULTI_ASSET_HEADERS)

    def test_multi_asset_has_extended_columns(self):
        header = self.rows[0]
        self.assertIn("Received Quantity 2", header)
        self.assertIn("Received Currency 2", header)
        self.assertIn("Sent Quantity 2", header)
        self.assertIn("Sent Currency 2", header)

    def test_standard_subset_present(self):
        header = self.rows[0]
        for col in ["Date", "Received Quantity", "Sent Quantity", "Fee Amount", "Tag"]:
            self.assertIn(col, header)


class TestFuturesTemplate(unittest.TestCase):
    def setUp(self):
        path = os.path.join(ASSETS_DIR, "template_futures.csv")
        with open(path, newline="") as f:
            reader = csv.reader(f)
            self.rows = list(reader)

    def test_header_row_present(self):
        self.assertGreaterEqual(len(self.rows), 1)

    def test_header_columns_match(self):
        self.assertEqual(self.rows[0], EXPECTED_FUTURES_HEADERS)

    def test_futures_specific_columns(self):
        header = self.rows[0]
        for col in ["Asset", "Amount", "Fee", "P&L", "Payment Token"]:
            self.assertIn(col, header)

    def test_sample_rows_valid(self):
        for row in self.rows[1:]:
            if not any(cell.strip() for cell in row):
                continue
            self.assertEqual(
                len(row),
                len(EXPECTED_FUTURES_HEADERS),
                f"Row column count mismatch: {row}",
            )


class TestTemplateColumnCounts(unittest.TestCase):
    """Every non-empty row must have the same number of columns as the header."""

    def _check_template(self, filename):
        path = os.path.join(ASSETS_DIR, filename)
        with open(path, newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        header_len = len(rows[0])
        for i, row in enumerate(rows[1:], start=2):
            if any(cell.strip() for cell in row):
                self.assertEqual(
                    len(row),
                    header_len,
                    f"{filename} line {i}: expected {header_len} cols, got {len(row)}",
                )

    def test_standard(self):
        self._check_template("template_standard.csv")

    def test_multi_asset(self):
        self._check_template("template_multi_asset.csv")

    def test_futures(self):
        self._check_template("template_futures.csv")


if __name__ == "__main__":
    unittest.main()
