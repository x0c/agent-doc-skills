#!/usr/bin/env python3
"""Discover user-level AI instruction files that doc-init / doc-compact may upgrade.

Prints unique real paths, one per line. Follows symlinks and de-duplicates.
Never includes a project-root AGENTS.md — only the candidate user-level files below.

Exit codes:
  0  one or more files found
  3  none of the candidate paths exist
"""

from __future__ import annotations

import sys
from pathlib import Path

CANDIDATES = (
    Path.home() / ".claude" / "CLAUDE.md",
    Path.home() / ".codex" / "AGENTS.md",
    Path.home() / ".codex" / "instructions.md",
    Path.home() / ".config" / "opencode" / "AGENTS.md",
    Path.home() / ".agents" / "AGENTS.md",
    Path.home() / ".config" / "agentsync" / "AGENTS.md",
)


def discover() -> list[Path]:
    seen: set[Path] = set()
    found: list[Path] = []
    for candidate in CANDIDATES:
        try:
            if not candidate.is_file():
                continue
            real = candidate.resolve()
        except OSError:
            continue
        if real in seen:
            continue
        seen.add(real)
        found.append(real)
    return found


def main() -> int:
    found = discover()
    if not found:
        print("none", file=sys.stderr)
        return 3
    for path in found:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
