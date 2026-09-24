#!/usr/bin/env python3
"""Regression checks for summary-based document-index updates."""

from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("upsert_agents_nav.py")
SPEC = importlib.util.spec_from_file_location("upsert_agents_nav", SCRIPT)
assert SPEC and SPEC.loader
NAV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NAV)
LINT_SPEC = importlib.util.spec_from_file_location(
    "doc_nav_lint", SCRIPT.with_name("doc_nav_lint.py")
)
assert LINT_SPEC and LINT_SPEC.loader
LINT = importlib.util.module_from_spec(LINT_SPEC)
LINT_SPEC.loader.exec_module(LINT)


class UpsertAgentsNavTests(unittest.TestCase):
    def test_existing_table_row_and_current_task_rule_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            original = (
                "# Global\n\n## Document index\n\n"
                "Read documents whose contents cover the current task before deciding or changing behavior.\n\n"
                "| Document | Contents |\n|---|---|\n"
                "| [A guide](docs/A.md) | Existing summary. |\n\n"
                "## Other\nKeep.\n"
            )
            agents.write_text(original, encoding="utf-8")

            NAV.upsert(root, "docs/A.md", "Existing summary")
            self.assertEqual(agents.read_text(encoding="utf-8"), original)
            NAV.upsert(root, "docs/A.md", "Updated summary")
            updated = agents.read_text(encoding="utf-8")
            NAV.upsert(root, "docs/A.md", "Updated summary")

            self.assertEqual(agents.read_text(encoding="utf-8"), updated)
            self.assertIn("| [A guide](docs/A.md) | Updated summary. |", updated)
            self.assertEqual(updated.count("docs/A.md"), 1)
            self.assertNotIn(NAV.SHARED_INDEX_INSTRUCTION, updated)
            codes = [issue["code"] for issue in LINT.lint(root)["issues"]]
            self.assertNotIn("missing-index-relevance-rule", codes)
            self.assertNotIn("duplicate-index-relevance-rule", codes)

    def test_new_document_joins_existing_table_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text(
                "## Document index\n\n"
                "Read documents whose contents cover the current task.\n\n"
                "| Document | Contents |\n|---|---|\n"
                "| [A.md](docs/A.md) | A summary. |\n\n"
                "## Other\nKeep.\n",
                encoding="utf-8",
            )

            NAV.upsert(root, "docs/B.md", "B summary")
            first = agents.read_text(encoding="utf-8")
            NAV.upsert(root, "docs/B.md", "B summary")

            self.assertEqual(agents.read_text(encoding="utf-8"), first)
            self.assertIn(
                "| [A.md](docs/A.md) | A summary. |\n| [B.md](docs/B.md) | B summary. |",
                first,
            )
            self.assertEqual(first.count("docs/B.md"), 1)
            self.assertNotIn("- `docs/B.md`", first)
            self.assertNotIn(NAV.SHARED_INDEX_INSTRUCTION, first)

    def test_project_document_navigation_is_idempotent_and_updates_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text("# Project\n\n## 文档导航\n\n## Other\nKeep this.\n", encoding="utf-8")

            NAV.upsert(root, "docs/DOMAIN.md", "State transitions and recovery rules")
            first = agents.read_text(encoding="utf-8")
            NAV.upsert(root, "docs/DOMAIN.md", "State transitions, recovery, and retry rules")
            second = agents.read_text(encoding="utf-8")

            self.assertIn("## 文档导航", second)
            self.assertEqual(second.count("## 文档导航"), 1)
            self.assertEqual(second.count(NAV.SHARED_INDEX_INSTRUCTION), 1)
            self.assertIn("- `docs/DOMAIN.md`: State transitions, recovery, and retry rules.", second)
            self.assertNotIn("State transitions and recovery rules", second)
            self.assertTrue(second.endswith("## Other\nKeep this.\n"))
            self.assertNotEqual(first, second)

    def test_existing_rule_index_is_reused_without_competing_doc_nav(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text(
                "# User rules\n\n## 规则索引\n\n- Existing policy summary.\n\n## Other\nKeep.\n",
                encoding="utf-8",
            )

            NAV.upsert(root, "docs/POLICY.md", "Policy ownership and deployment behavior")
            result = agents.read_text(encoding="utf-8")

            self.assertEqual(result.count("## 规则索引"), 1)
            self.assertNotIn("## 文档导航", result)
            self.assertEqual(result.count(NAV.SHARED_INDEX_INSTRUCTION), 1)
            self.assertIn("- `docs/POLICY.md`: Policy ownership and deployment behavior.", result)
            self.assertIn("- Existing policy summary.", result)
            self.assertTrue(result.endswith("## Other\nKeep.\n"))

    def test_duplicate_shared_instruction_is_reduced_to_one(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            rule = NAV.SHARED_INDEX_INSTRUCTION
            agents.write_text(
                f"## 文档导航\n\n- {rule}\n- `docs/A.md`: A summary.\n- {rule}\n",
                encoding="utf-8",
            )

            NAV.upsert(root, "docs/B.md", "B summary")
            result = agents.read_text(encoding="utf-8")
            self.assertEqual(result.count(rule), 1)

    def test_existing_chinese_relevance_instruction_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            chinese_rule = "请阅读与当前任务相关的文档。"
            agents.write_text(
                f"## 文档导航\n\n- {chinese_rule}\n- `docs/A.md`: Existing summary.\n",
                encoding="utf-8",
            )

            NAV.upsert(root, "docs/B.md", "Additional document coverage")
            first = agents.read_text(encoding="utf-8")
            NAV.upsert(root, "docs/B.md", "Additional document coverage")
            second = agents.read_text(encoding="utf-8")

            self.assertEqual(second.count(chinese_rule), 1)
            self.assertNotIn(NAV.SHARED_INDEX_INSTRUCTION, second)
            self.assertEqual(second.count("docs/B.md"), 1)
            self.assertEqual(first, second)

    def test_english_document_index_and_current_work_rule_are_preserved(self):
        existing_rule = "Read the documents that cover the current work using their content summaries."
        for heading in ("Document index", "Documentation index"):
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                agents = root / "AGENTS.md"
                agents.write_text(
                    f"## {heading}\n\n- {existing_rule}\n- `docs/A.md`: Existing summary.\n",
                    encoding="utf-8",
                )

                NAV.upsert(root, "docs/B.md", "Additional document coverage")
                first = agents.read_text(encoding="utf-8")
                NAV.upsert(root, "docs/B.md", "Additional document coverage")
                second = agents.read_text(encoding="utf-8")

                self.assertEqual(second.count(existing_rule), 1)
                self.assertNotIn(NAV.SHARED_INDEX_INSTRUCTION, second)
                self.assertNotIn("## 文档导航", second)
                self.assertEqual(first, second)

                issue_codes = [issue["code"] for issue in LINT.lint(root)["issues"]]
                self.assertNotIn("missing-doc-nav", issue_codes)
                self.assertNotIn("missing-index-relevance-rule", issue_codes)

    def test_cli_legacy_alias_and_explicit_root_work_from_other_cwd(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            (root / "AGENTS.md").write_text("# Project\n\n## 文档导航\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "--path", "docs/OLD.md",
                 "--when-to-read", "Old callers still supply a concise content summary"],
                cwd=directory,
                check=True,
                capture_output=True,
                text=True,
            )
            text = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("updated doc nav", result.stdout)
            self.assertIn("- `docs/OLD.md`: Old callers still supply a concise content summary.", text)
            self.assertEqual(text.count(NAV.SHARED_INDEX_INSTRUCTION), 1)

    def test_new_file_gets_one_index_and_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            NAV.upsert(root, "docs/NEW.md", "New document coverage")
            result = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(result.count("## 文档导航"), 1)
            self.assertEqual(result.count(NAV.SHARED_INDEX_INSTRUCTION), 1)
            self.assertIn("- `docs/NEW.md`: New document coverage.", result)

    def test_lint_accepts_chinese_shared_relevance_wording_and_rule_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "## 规则索引\n\n- 请阅读与当前任务相关的文档。\n- `docs/A.md`: A summary.\n",
                encoding="utf-8",
            )
            issues = LINT.lint(root)["issues"]
            self.assertNotIn("missing-doc-nav", [item["code"] for item in issues])
            self.assertNotIn("missing-index-relevance-rule", [item["code"] for item in issues])

    def test_lint_detects_repeated_shared_rule_across_indexes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rule = NAV.SHARED_INDEX_INSTRUCTION
            (root / "AGENTS.md").write_text(
                f"## 规则索引\n\n- {rule}\n\n## 文档导航\n\n- {rule}\n",
                encoding="utf-8",
            )
            issues = LINT.lint(root)["issues"]
            self.assertIn("duplicate-index-relevance-rule", [item["code"] for item in issues])


if __name__ == "__main__":
    unittest.main()
