**Languages:** English | [简体中文](README.zh-CN.md)

# agent-doc-skills

**Stop paying your coding agent to rediscover your repository every session.**

A lightweight set of Agent Skills (`doc-init`, `doc-update`, `doc-compact`) for **Claude Code**, **Codex CLI**, **Cursor**, and **OpenCode** that builds and maintains a navigable, token-efficient project knowledge base.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Why `agent-doc-skills`?

When working with AI coding agents on a growing codebase, two things usually happen:
1. **Cold-start amnesia:** Every new session starts from zero. The agent burns time and tokens running `grep` and reading dozens of files just to understand your architecture.
2. **Instruction bloat:** You dump everything into `CLAUDE.md` or `AGENTS.md`. Soon it hits 50k+ tokens, polluting the context window and causing the model to ignore critical rules.

**`agent-doc-skills` solves both with progressive disclosure:**
Instead of loading every document into every conversation, it keeps your root `AGENTS.md` / `CLAUDE.md` as a **compact routing map** pointing to domain-specific docs (`docs/`). The agent only reads the exact document it needs for the current task.

```text
Your Project
├── AGENTS.md / CLAUDE.md       <-- Small entrypoint & routing table (always loaded)
└── docs/
    ├── architecture.md         <-- Loaded on-demand when changing system design
    ├── api-contracts.md        <-- Loaded on-demand when touching endpoints
    └── testing-standards.md    <-- Loaded on-demand when writing tests
```

---

## Install

Requires **Node.js** (for the `skills` CLI) and **Python 3** (for the bundled local inventory/link-checking helpers).

```bash
npx skills add x0c/agent-doc-skills -g
```

Start a new agent conversation after installation so your host picks up `doc-init`, `doc-update`, and `doc-compact`.

> **Tip:** Managing skills across multiple coding agents? Use **[agentsync](https://github.com/x0c/agentsync)** to sync `~/.config/agentsync/skills/` across Claude Code, Cursor, Codex, and 15+ other tools automatically.

---

## Quick Start & Workflows

You invoke these skills in plain language inside your coding agent session:

| Skill | When to use it | Example prompt to type in your agent |
| :--- | :--- | :--- |
| **`doc-init`** | **Day 1 / New repo:** Bootstrap navigable project docs from existing code, READMEs, and configs, or upgrade the global documentation contract. | `Use doc-init to establish documentation for this project from its existing authorities.` |
| **`doc-update`** | **Daily dev:** After finishing a feature or bugfix, persist reusable findings and architectural decisions into the right owning doc. | `Use doc-update to record this task's reusable findings in their owning documents.` |
| **`doc-compact`** | **Cleanup / Audit:** Compress bloated docs without losing hard rules, numbers, or exceptions, and repair broken Markdown links. | `Use doc-compact to audit and compress this project's documentation.` |

### Read-Only Audit Mode

Want to see what `doc-compact` finds before it touches any file? Ask for a read-only audit:

```text
Use doc-compact to audit this project's documentation without changing files.
```

---

## How It Works & Safety Guarantees

Unlike generic "summarize this repo" prompts, `agent-doc-skills` pairs structured agent procedures with deterministic Python helper scripts:

- **Evidence-based, no hallucinated specs:** Bundled helpers scan your repo inventory, Git history, code signals, and Markdown links first. If evidence is missing, the skill reports the gap instead of inventing documentation.
- **Lossless compression (`doc-compact`):** Preserves exact scopes, exceptions, numeric thresholds, evidence, and machine-parsed markers while stripping fluff.
- **Safe global preset injection:** `doc-init` discovers real global instruction files and preserves your existing custom instructions and neighboring managed blocks.
- **No unauthorized background subagents:** Skills execute directly in your main session by default and respect your host's permission and model policies.

---

## 🧩 Related Tools in the AI Coding Suite

If you run multiple AI coding agents daily, check out the rest of the local-first toolkit:

| Repository | Description |
| :--- | :--- |
| **[corral](https://github.com/corral-dev/corral)** | Run Claude Code, Codex, OpenCode, Cursor & Pi side-by-side in a terminal session manager, then continue from iPhone or Mac. |
| **[subswap](https://github.com/x0c/subswap)** | Check remaining quota and switch Claude Code, Codex, Cursor, Kimi Code & OpenCode accounts without logging out. |
| **[agentsync](https://github.com/x0c/agentsync)** | Sync `AGENTS.md`, `CLAUDE.md`, skills, and MCP configs across coding agents from one local source of truth. |
| **[sesskit](https://github.com/x0c/sesskit)** | Parse and export local Claude Code, Codex CLI, and Cursor session transcript files from disk. |

## License

[MIT](LICENSE)
