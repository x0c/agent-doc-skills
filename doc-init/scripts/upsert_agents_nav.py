#!/usr/bin/env python3
"""
Idempotently add/update root AGENTS.md doc-nav entries, or register backlog items.

Normal doc-nav mode (default):
  upsert_agents_nav.py --root . --path docs/CUSTOMER_KNOWLEDGE_BASE.md --summary "Customer records, account lifecycle, and retention rules"

Backlog mode (--backlog):
  upsert_agents_nav.py --root . --backlog --name "channel system KB" --anchor "src/channels/" --summary "Channel configuration, routing behavior, and delivery failures"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


INDEX_HEADING_RE = re.compile(r"^(#{1,4})\s*(?:文档导航|规则索引|Document(?:ation)? index)\s*$", re.I | re.M)
BACKLOG_HEADING_RE = re.compile(r"^(#{1,4})\s*待补充知识库（doc-init backlog）\s*$", re.M)
SHARED_INDEX_INSTRUCTION = "Read the documents whose described content is relevant to the current task."
SHARED_INDEX_RULE_RE = re.compile(
    r"^\s*(?:[-*]\s+)?(?:please\s+)?(?:read|consult)\b(?=.*\b(?:documents?|docs?)\b)(?=.*\b(?:relevant|applicable)\b).*$|"
    r"^\s*(?:[-*]\s+)?(?:please\s+)?read\b(?=.*\bdocuments?\b)(?=.*\bcover\b)(?=.*\bcurrent\s+(?:work|task)\b).*$|"
    r"^\s*(?:[-*]\s+)?(?:请)?(?:阅读|读取|查阅)(?=.*(?:文档|文件))(?=.*(?:相关|适用)).*$",
    re.I,
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def normalize_path(path: str) -> str:
    value = path.strip().replace("\\", "/")
    if value.startswith("./"):
        value = value[2:]
    return value


def ensure_sentence_end(text: str) -> str:
    text = text.strip()
    if text and text[-1] not in "。.!！?？":
        text += "."
    return text


def make_nav_line(doc_path: str, summary: str) -> str:
    return f"- `{doc_path}`: {ensure_sentence_end(summary)}"


def make_backlog_line(name: str, anchor: str, summary: str) -> str:
    return f"- [待补充] {name} — Entry anchor: {anchor}; Content summary: {ensure_sentence_end(summary)}"


def two_column_cells(line: str) -> list[str] | None:
    value = line.strip()
    if not (value.startswith("|") and value.endswith("|")):
        return None
    cells = [cell.strip() for cell in value[1:-1].split("|")]
    return cells if len(cells) == 2 else None


def upsert_two_column_table(section: str, doc_path: str, summary: str) -> tuple[str, str] | None:
    """Keep a document index that already uses a two-column Markdown table."""
    lines = section.splitlines(keepends=True)
    for start in range(len(lines) - 1):
        header = two_column_cells(lines[start])
        separator = two_column_cells(lines[start + 1])
        if header is None or separator is None or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            continue
        end = start + 2
        while end < len(lines) and two_column_cells(lines[end]) is not None:
            cells = two_column_cells(lines[end])
            assert cells is not None
            link = MARKDOWN_LINK_RE.search(cells[0])
            if link and normalize_path(link.group(1).split("#", 1)[0]) == doc_path:
                row = f"| {cells[0]} | {ensure_sentence_end(summary)} |"
                lines[end] = row + ("\n" if lines[end].endswith("\n") else "")
                return "".join(lines), row
            end += 1
        row = f"| [{Path(doc_path).name}]({doc_path}) | {ensure_sentence_end(summary)} |"
        if end and not lines[end - 1].endswith("\n"):
            lines[end - 1] += "\n"
        lines.insert(end, row + "\n")
        return "".join(lines), row
    return None


def ensure_shared_index_instruction(text: str) -> str:
    """Keep one shared relevance instruction in the existing document index."""
    headings = list(INDEX_HEADING_RE.finditer(text))
    if not headings:
        return text
    bounds = []
    for heading in headings:
        bounds.append((heading.start(), find_section_end(text, heading)))
    candidates: list[tuple[int, int]] = []
    for start, end in bounds:
        offset = start
        for line in text[start:end].splitlines(keepends=True):
            if SHARED_INDEX_RULE_RE.match(line.rstrip("\r\n")):
                candidates.append((offset, offset + len(line)))
            offset += len(line)
    candidates = sorted(set(candidates))
    if candidates:
        # Preserve the first existing equivalent instruction and remove only
        # additional standalone relevance instructions from AGENTS indexes.
        for start, end in reversed(candidates[1:]):
            text = text[:start] + text[end:]
        return text

    heading = INDEX_HEADING_RE.search(text)
    assert heading is not None
    section_end = find_section_end(text, heading)
    section = text[heading.start():section_end]
    split = heading.end() - heading.start()
    body = section[split:].strip("\n")
    section = section[:split] + "\n\n- " + SHARED_INDEX_INSTRUCTION + "\n"
    if body:
        section += "\n" + body.rstrip() + "\n"
    elif section_end == len(text):
        section += "\n"
    if section_end < len(text):
        section = section.rstrip("\n") + "\n\n"
    text = text[:heading.start()] + section + text[section_end:]
    return text


def find_section_end(text: str, heading_match: re.Match[str]) -> int:
    """Return end offset of the heading's section (start of next same-or-higher heading)."""
    heading_level = len(heading_match.group(1))
    rest = text[heading_match.end():]
    next_heading = re.search(rf"^#{{1,{heading_level}}}\s+\S.*$", rest, re.M)
    if next_heading:
        return heading_match.end() + next_heading.start()
    return len(text)


def upsert(root: Path, doc_path: str, summary: str) -> str:
    """Idempotently write one nav entry under the AGENTS.md 「文档导航」 section."""
    agents = root / "AGENTS.md"
    doc_path = normalize_path(doc_path)
    new_line = make_nav_line(doc_path, summary)

    if agents.exists():
        text = agents.read_text(encoding="utf-8", errors="ignore")
    else:
        text = "# Project overview\n\n## 文档导航\n\n"

    match = INDEX_HEADING_RE.search(text)
    if match:
        section_end = find_section_end(text, match)
        table_update = upsert_two_column_table(text[match.start():section_end], doc_path, summary)
        if table_update is not None:
            section, row = table_update
            text = text[:match.start()] + section + text[section_end:]
            text = ensure_shared_index_instruction(text)
            agents.write_text(text.rstrip() + "\n", encoding="utf-8")
            return row

    # Replace in place if present; otherwise append at end of nav section
    line_pattern = re.compile(
        rf"^[-*]\s+.*(?:`|\()\.?/?{re.escape(doc_path)}(?:`|\)).*$", re.M
    )
    if line_pattern.search(text):
        text = line_pattern.sub(new_line, text, count=1)
    else:
        match = INDEX_HEADING_RE.search(text)
        if not match:
            if not text.endswith("\n"):
                text += "\n"
            text += "\n## 文档导航\n\n" + new_line + "\n"
        else:
            section_end = find_section_end(text, match)
            before = text[:section_end].rstrip()
            after = text[section_end:]
            text = before + "\n\n" + new_line + "\n\n" + after.lstrip("\n")

    text = ensure_shared_index_instruction(text)
    agents.write_text(text.rstrip() + "\n", encoding="utf-8")
    return new_line


def upsert_backlog(root: Path, name: str, anchor: str, summary: str) -> str:
    """Idempotently write one backlog entry under 「待补充知识库（doc-init backlog）」."""
    agents = root / "AGENTS.md"
    new_line = make_backlog_line(name, anchor, summary)

    if agents.exists():
        text = agents.read_text(encoding="utf-8", errors="ignore")
    else:
        text = "# Project overview\n\n"

    # Replace in place if same-name entry exists (match by domain name)
    escaped_name = re.escape(name)
    line_pattern = re.compile(
        rf"^[-*]\s+\[待补充\]\s+{escaped_name}.*$", re.M
    )
    if line_pattern.search(text):
        text = line_pattern.sub(new_line, text, count=1)
    else:
        match = BACKLOG_HEADING_RE.search(text)
        if not match:
            # Create backlog section at end of file
            if not text.endswith("\n"):
                text += "\n"
            text += "\n## 待补充知识库（doc-init backlog）\n\n" + new_line + "\n"
        else:
            section_end = find_section_end(text, match)
            before = text[:section_end].rstrip()
            after = text[section_end:]
            text = before + "\n" + new_line + "\n" + after

    agents.write_text(text.rstrip() + "\n", encoding="utf-8")
    return new_line


def main() -> int:
    parser = argparse.ArgumentParser(description="Idempotently update root AGENTS.md document summaries or backlog entries")
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument(
        "--backlog",
        action="store_true",
        help="write the backlog section instead of doc nav",
    )
    # normal nav-mode args
    parser.add_argument("--path", help="doc path to register, e.g. docs/CUSTOMER_KNOWLEDGE_BASE.md")
    # backlog-mode args
    parser.add_argument("--name", help="(backlog mode) domain name, e.g. channel system KB")
    parser.add_argument("--anchor", help="(backlog mode) entry anchor, e.g. src/channels/")
    # shared by both modes
    parser.add_argument("--summary", "--when-to-read", dest="summary", required=True,
                        help="concise summary of document content (legacy --when-to-read alias)")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: project root does not exist or is not a directory: {root}")
        return 2

    if args.backlog:
        if not args.name or not args.anchor:
            print("error: --backlog mode requires both --name and --anchor")
            return 2
        line = upsert_backlog(root, args.name, args.anchor, args.summary)
        print(f"registered backlog: {line}")
    else:
        if not args.path:
            print("error: normal nav mode requires --path")
            return 2
        line = upsert(root, args.path, args.summary)
        print(f"updated doc nav: {line}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
