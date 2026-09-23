# agent-doc-skills

The `doc-init` / `doc-compact` / `doc-update` skills published in this repository.

## Repository layout and source of truth

- `doc-init/`, `doc-compact/`, `doc-update/` — the three skills. Each directory is a self-contained skill (`SKILL.md` + `references/` + `scripts/`).
- `README.md` — bilingual (English + Chinese) introduction and install instructions.
- These published copies are **not** the source of truth. The authoritative source lives in the maintainer's local agentsync skills directory; changes are made there and synced here. Do not maintain divergent edits in this repository.

## Hard constraints for contributors

- **Identity**: all commits must use the anonymous `x0c <x0c@users.noreply.github.com>` identity for both author and committer. Never commit with a personal or corporate git identity — the history is public.
- **Privacy**: never push company names, internal platform names, personal names, phone numbers, or internal hostnames/URLs. Keep all content generic.
- **Verification**: after changing any `scripts/` file, run the skill's own verification (e.g. `python3 scripts/doc_nav_lint.py` smoke test on a fixture) before pushing. After changing `SKILL.md`, re-read the full file to confirm structure is intact.
- **Language**: skill bodies are English-only. The README is bilingual.

## Documentation map

- `README.md` — what each skill does, how they cooperate, install methods.
- `doc-init/references/` — document templates, knowledge-network design, scan report format.
- `doc-compact/references/standard.md` — the documentation-governance standard the skill audits against.
- `doc-update/SKILL.md` — self-contained; no extra references.
