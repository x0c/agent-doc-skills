#!/usr/bin/env python3
"""
Insert the Project Documentation Management standard into the real global AI
instruction file, with version detection and automatic upgrade.

Usage: python3 insert_doc_governance.py <real-path>

Idempotent behavior:
- If the file already has the current version → skip.
- If the file has an older version (or an unversioned old section) → replace with the new version.
- If there is no Project Documentation Management section → insert.

New-install position (upgrades replace the existing section in place):
1) Before "## 附：外部托管区块" (agentsync canonical Chinese marker)
2) Before agentsync:begin / external-managed markers
3) Before the first @ reference line (@RTK.md, etc.)
4) Append at end of file

Version upgrades: after changing STANDARD, bump CURRENT_VERSION by 1;
the next doc-init run will detect and upgrade already-deployed older versions.
"""

import sys
import re

CURRENT_VERSION = 21

# Heading used in the injectable STANDARD (English for open-source inject).
SECTION_TITLE = "Project Documentation Management"
# Legacy Chinese heading still present in older deployments; must be removable on upgrade.
LEGACY_SECTION_TITLE = "项目文档管理"

STANDARD = f"""## {SECTION_TITLE}
<!-- doc-governance-version: {CURRENT_VERSION} -->

### Ownership and entry points

This preset owns documentation capture, selection, placement, navigation, correction, promotion and verification. Maintain its source in doc-init; installed blocks are generated copies. Skills supply procedures. User/environment instructions own language, memory, permissions, Git/release, models and actual paths; documentation work does not authorize unrelated implementation or policy changes.

Root `AGENTS.md` is the only top-level documentation entry; project-root `CLAUDE.md` defaults to `@AGENTS.md`. Long-lived docs are reachable in one or two hops. On creation/takeover, link declared matching language/stack standards near the root's top; never invent a shared location.

### Capture and selection

- Record-first is a gate: draft adopted durable requirements, corrections and user-visible bug-fix behavior in the owning document and make it reachable before touching code, config, or other docs for that decision. When placement is uncertain, draft at the nearest reachable doc and relocate in the same turn. Temporary scope, examples and unadopted suggestions are excluded; a wording veto records the usefulness test rather than a permanent word ban.
- Persist reusable findings when established, including Q&A without code changes, through `doc-update` when available; check omissions at closure. Search existing authorities first. No new durable knowledge means no forced update.
- Preserve non-obvious business rules, hidden constraints, validated workflows, causes/remedies and material risks. Record relevant symptoms, applicability and verification; distinguish facts, hypotheses and pending decisions. Existing mechanism coverage does not establish coverage of a new symptom or failed remedy. Do not duplicate code structure, Git history, policy or session narrative.
- Repair missing/misleading coverage or routing in the same bounded update. Preserve valid task coverage while consolidating repetition and obsolete triggers. A recurring obstacle despite correct docs needs an actionable environment-improvement item alongside its workaround; recording it does not authorize implementation.

### Placement

| Information | Authority |
|---|---|
| Project-wide operating rules | Project-root `AGENTS.md` |
| Product behavior, domain knowledge and architecture | Matching project `docs/` document |
| Reusable procedure, checklist or executable helper | Matching skill |
| Cross-project platform facts, constraints and troubleshooting | Declared shared guide/standards |
| Recurring implementation obstacle | Existing backlog or indexed design/troubleshooting document |

Promote reusable cross-project knowledge during updates/cleanup, retaining local product details and pointers. Report missing shared bindings instead of inventing paths. Use registered domain KB, guide, design and troubleshooting types; register a new type's purpose/placement at root and avoid competing bare `INDEX.md`/`OVERVIEW.md` entry points.

### Navigation and indexes

- Describe the document's actual content precisely and concisely in its root or registered secondary-index entry. Add one shared instruction to the `AGENTS.md` document navigation to read relevant documents before governed decisions. Entries are content summaries, not trigger lists or duplicate rules; ordinary implementation must find requirements even when the request omits their keywords.
- Use the dedicated `agents-md-edit` skill for deliberate root edits; report its absence rather than bypass it. Documentation skills retain lifecycle ownership and verify the integrated result.
- Prefer direct root links. Use a named `<DOMAIN>_INDEX.md` only when a group is hard to scan; counts/line limits are signals, not commands. Root → index → document is the deepest index chain. Reading relevance has no arbitrary document quota.
- Register documents immediately, check orphans and update summaries/links after expansion, moves, renames or deletion. A pointer beside a supported rule may coexist with the canonical navigation entry; multiple useful routes do not duplicate the authority's body.

### Corrections and verification

Maintain one authoritative home per fact/rule/mechanism, with resolvable pointers elsewhere. Correct superseded conclusions and affected references together, using adopted requirements and evidence; a user-confirmed requirement may supersede implementation. Mark unresolved contradictions and the needed decision. Keep updates bounded; a small change is not a full census.

Re-read changes and navigation; verify reachability, links, content summaries, contradictions and representative behavior. Compression preserves scope, timing, exceptions, evidence and machine-parsed markers. A structural pass or review stamp is not semantic proof. Report changed document paths/purpose and remaining limits; when no update was needed, say so.
"""

VERSION_RE = re.compile(r"<!--\s*doc-governance-version:\s*(\d+)\s*-->")
def _section_bounds(content: str) -> tuple[int, int] | None:
    """Find the real managed section, ignoring headings inside fenced examples."""
    start = None
    offset = 0
    fence = None
    for line in content.splitlines(keepends=True):
        stripped = line.strip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and stripped == token:
                fence = None
        elif fence is None:
            if start is not None and re.match(r"<!--\s*(?:agentsync:begin\b|[\w:-]+:(?:begin|start)\b)", stripped):
                return start, offset
            heading = re.match(r"^(#{1,2})[ \t]+(.+?)\s*$", line)
            if heading:
                title = heading.group(2).rstrip("#").rstrip()
                if start is not None:
                    return start, offset
                if heading.group(1) == "##" and title in (SECTION_TITLE, LEGACY_SECTION_TITLE):
                    start = offset
        offset += len(line)
    return (start, len(content)) if start is not None else None


def _get_installed_version(content: str) -> int | None:
    bounds = _section_bounds(content)
    if bounds is None:
        return None
    m = VERSION_RE.search(content[bounds[0]:bounds[1]])
    return int(m.group(1)) if m else None


def _has_section(content: str) -> bool:
    return _section_bounds(content) is not None


def _remove_section(content: str) -> str:
    bounds = _section_bounds(content)
    return content[:bounds[0]] + content[bounds[1]:] if bounds else content


def insert(path: str) -> None:
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    installed = _get_installed_version(content)

    if installed is not None and installed >= CURRENT_VERSION:
        print(f"[skip] {SECTION_TITLE} already latest (v{installed}): {path}")
        return

    if _has_section(content):
        if installed is None:
            print(
                f"[upgrade] Unversioned old section detected; replacing with v{CURRENT_VERSION}: {path}"
            )
        else:
            print(f"[upgrade] v{installed} → v{CURRENT_VERSION}: {path}")
        bounds = _section_bounds(content)
        assert bounds is not None
        # Replace in place so surrounding user rules and external blocks are unchanged.
        old = content[bounds[0]:bounds[1]]
        trailing = old[len(old.rstrip("\r\n")):]
        new_content = content[:bounds[0]] + STANDARD.rstrip("\n") + trailing + content[bounds[1]:]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        print(f"[done] Wrote successfully: {path}")
        return
    else:
        print(f"[added] Inserting {SECTION_TITLE} v{CURRENT_VERSION}: {path}")

    # Insert position (priority order):
    # 1) Before "## 附：外部托管区块" (agentsync canonical Chinese marker)
    # 2) Before agentsync:begin / external-managed markers
    # 3) Before the first @ reference line (@RTK.md, etc.)
    # 4) End of file
    insert_pos = None
    for pat in (
        r"\n## 附：外部托管区块\b",
        r"\n<!--\s*agentsync:begin",
        r"\n(@\S+.*)",
    ):
        m = re.search(pat, content)
        if m:
            insert_pos = m.start()
            break
    if insert_pos is not None:
        before = content[:insert_pos]
        after = content[insert_pos:]
        new_content = (
            before.rstrip("\n") + "\n\n" + STANDARD.rstrip("\n") + "\n\n" + after.lstrip("\n")
        )
    else:
        new_content = content.rstrip("\n") + "\n\n" + STANDARD.rstrip("\n") + "\n"

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)

    print(f"[done] Wrote successfully: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {sys.argv[0]} <real path of AI instruction file>",
            file=sys.stderr,
        )
        sys.exit(1)
    insert(sys.argv[1])
