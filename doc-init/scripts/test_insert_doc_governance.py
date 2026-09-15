#!/usr/bin/env python3
"""Regression checks for preserving user content during preset upgrades."""
import contextlib
import io
from pathlib import Path
import runpy
import tempfile
import unittest

NS = runpy.run_path(str(Path(__file__).with_name("insert_doc_governance.py")))
OLD = "## Project Documentation Management\n<!-- doc-governance-version: 16 -->\nOld rule.\n\n"

class UpgradeTests(unittest.TestCase):
    def upgrade(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            path.write_bytes(content.encode("utf-8"))
            with contextlib.redirect_stdout(io.StringIO()):
                NS["insert"](str(path))
            result = path.read_bytes().decode("utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                NS["insert"](str(path))
            self.assertEqual(result.encode("utf-8"), path.read_bytes())
            self.assertIn(NS["STANDARD"].strip(), result)
            return result

    def test_install_before_external_block(self):
        prefix = "# User policy\nKeep this.\n\n"
        suffix = "<!-- agentsync:begin example -->\nKeep external.\n<!-- agentsync:end example -->\n"
        result = self.upgrade(prefix + suffix)
        self.assertTrue(result.startswith(prefix))
        self.assertTrue(result.endswith(suffix))

    def test_upgrade_preserves_neighbors(self):
        prefix = "# User rules\nUnchanged.\n\n"
        suffix = "## Other policy\nKeep this.\n\n<!-- external -->\n"
        result = self.upgrade(prefix + OLD + suffix)
        self.assertTrue(result.startswith(prefix))
        self.assertTrue(result.endswith(suffix))
        self.assertNotIn("Old rule.", result)

    def test_external_block_without_heading(self):
        suffix = "<!-- agentsync:begin mcp -->\nExternal text.\n<!-- agentsync:end mcp -->\n"
        self.assertTrue(self.upgrade(OLD + suffix).endswith(suffix))

    def test_section_at_start(self):
        result = self.upgrade(OLD + "## Other\nKeep.\n")
        self.assertEqual(result.count("<!-- doc-governance-version:"), 1)
        self.assertTrue(result.endswith("## Other\nKeep.\n"))

    def test_following_level_one(self):
        suffix = "# Personal policy\nKEEP\n"
        self.assertTrue(self.upgrade("# Before\n\n" + OLD + suffix).endswith(suffix))

    def test_legacy_chinese_title(self):
        result = self.upgrade(OLD.replace("Project Documentation Management", "项目文档管理") + "## Other\nKEEP\n")
        self.assertNotIn("## 项目文档管理", result)
        self.assertTrue(result.endswith("## Other\nKEEP\n"))

    def test_fenced_headings_are_not_sections(self):
        example = "```md\n" + OLD + "```\n"
        result = self.upgrade(example)
        self.assertTrue(result.startswith(example))
        old_with_example = OLD + "```md\n# Example heading\n```\n\n"
        result = self.upgrade(old_with_example + "# User rules\nKEEP\n")
        self.assertNotIn("# Example heading", result)
        self.assertTrue(result.endswith("# User rules\nKEEP\n"))

    def test_preserves_crlf_outside_block(self):
        prefix = "# User\r\nKeep.\r\n\r\n"
        suffix = "## Other\r\nKEEP\r\n"
        result = self.upgrade(prefix + OLD.replace("\n", "\r\n") + suffix)
        self.assertTrue(result.startswith(prefix))
        self.assertTrue(result.endswith(suffix))

    def test_unrelated_version_marker_does_not_block_install(self):
        result = self.upgrade("# Other\n<!-- doc-governance-version: 99 -->\n")
        self.assertIn("<!-- doc-governance-version: 17 -->", result)

if __name__ == "__main__":
    unittest.main()
