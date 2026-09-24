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

CURRENT_VERSION = 19

# Heading used in the injectable STANDARD (English for open-source inject).
SECTION_TITLE = "Project Documentation Management"
# Legacy Chinese heading still present in older deployments; must be removable on upgrade.
LEGACY_SECTION_TITLE = "项目文档管理"

STANDARD = f"""## {SECTION_TITLE}
<!-- doc-governance-version: {CURRENT_VERSION} -->

### 1. Ownership and entry points

* This block owns the documentation lifecycle: capture, selection, organization, correction, cross-project promotion and verification. Its maintenance source is doc-init's injectable preset; the installed block is a generated copy. Skill bodies supply execution procedures, not competing policies.
* Language, memory facilities, permissions, Git/release behavior, model selection and actual shared-document locations belong to the user's environment instructions. Documentation improvement does not authorize unrelated implementation or rewriting other global policies.
* Root `AGENTS.md` is the project's only top-level documentation entry. Long-lived docs must be reachable in one or two hops. Project-root `CLAUDE.md` defaults to the single line `@AGENTS.md`.
* On project creation or takeover, discover any declared cross-project standards location and link matching language/stack standards near the top of root `AGENTS.md`. Do not invent a location if none is declared.

### 2. Capture and continuous improvement

* Before implementing durable product decisions, requirements or corrections, record the current requirement in the appropriate document and make its entry reachable. Exclude temporary task scope, illustrative examples and unadopted suggestions. For a wording veto, capture the usefulness test, not a permanent ban on the rejected words.
* Persist reusable investigation findings when established, including Q&A with no code changes. Use `doc-update` when available for incremental updates; at closure, check for omissions. No new durable knowledge means no forced update.
* Record relevant symptoms, applicability, causes, remedies and verification evidence. Distinguish verified facts, unverified hypotheses and decisions awaiting confirmation. Existing mechanism coverage does not imply that a newly observed symptom or failed remedy is already documented.
* Search existing authoritative docs before adding material. If a needed doc was missing, hard to find or misleading, repair its coverage, routing or wording in the same bounded update. Preserve valid task coverage while merging repetition and removing obsolete triggers.
* When correct documentation still leaves a recurring operational obstacle, record an actionable environment-improvement item alongside the workaround. Tracking the improvement does not authorize implementing it outside the task.

### 3. Placement and knowledge selection

| Information | Authoritative destination |
|---|---|
| Project-wide operating rules | Project-root `AGENTS.md` |
| Product behavior, domain knowledge, architecture | Matching document under project `docs/` |
| Reusable task procedure, checklist or executable helper | Matching skill |
| Cross-project platform facts, constraints and troubleshooting knowledge | Declared shared guide or standards location |
| Recurring environment obstacle requiring implementation | Existing project backlog or an indexed design/troubleshooting document |

* During updates and full document cleanup, promote reusable cross-project knowledge to the declared shared authority; keep product-specific details and pointers locally. If no destination is declared, report the missing binding instead of inventing a machine path.
* Keep knowledge that prevents rediscovery or mistakes: business rules, hidden constraints, validated workflows, failure causes, remedies and unresolved material risks. Do not duplicate code structure, Git history, existing rules or session-only narrative.
* Use domain knowledge bases, guides, design docs or troubleshooting records according to the project's registered types. Register a new long-lived type's purpose and placement at the root; do not create competing bare `INDEX.md` / `OVERVIEW.md` entry points.

### 4. Navigation and indexes

* Each long-lived doc has one navigation entry at the root or its registered secondary index. Describe the document's actual content precisely and concisely; do not turn entries into trigger lists or duplicate the document body.
* Add one shared instruction to the `AGENTS.md` document navigation: read documents whose described content is relevant to the current task. Keep individual entries descriptive rather than repeating this routing rule.
* When a deliberate `AGENTS.md` edit is needed, route the edit through the dedicated `agents-md-maintenance` skill; documentation skills retain lifecycle decisions and verify the result. If that capability is unavailable, report the limitation rather than editing around it.
* Put a pointer beside a rule it supports. This may coexist with the doc's single navigation entry.
* Default to direct root links. Add a named `<DOMAIN>_INDEX.md` only when a group makes navigation hard to scan; counts and line limits are audit signals, not automatic restructuring commands. Root then links the index and the index links the documents. No deeper index chain.
* Register new docs immediately and check for unregistered files. Remove entries when deleting docs; update all affected links after moves or renames. Expanded content requires updating its content summary too.

### 5. One authoritative source and corrections

* Maintain each fact, rule or mechanism in one authoritative source; use resolvable pointers where other documents need it. Do not copy changing facts across documents.
* When confirmed knowledge or terminology changes, correct affected old conclusions and references together. Verify against product decisions, requirements and implementation evidence as appropriate; user-confirmed new requirements can supersede outdated implementation.
* Mark unresolved contradictions explicitly with the decision needed. Do not present incompatible claims as simultaneously confirmed. Keep corrections bounded to the affected concepts; a small update is not a full-document census.

### 6. Verification and closure

* Re-read changed content, verify entry reachability and links, and check for conflicting statements or missing content summaries. Report unresolved verification limits accurately.
* Check that promised documentation and reference updates are complete. Report changed document paths and their purpose; if nothing changed, state that no documentation update was needed.
* Compression must preserve behavior, boundaries, exceptions, evidence and machine-parsed markers. A review stamp is a coverage receipt, not proof of semantic correctness.
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
