**Languages:** English | [简体中文](README.zh-CN.md)

# agent-doc-skills

Three Agent Skills keep project knowledge discoverable without loading every document into every conversation. Skills retain detailed procedures in linked references and use small task entrypoints.

## Install

On macOS, Linux or Windows, with Node.js installed:

```sh
npx skills add x0c/agent-doc-skills -g
```

The installer offers `doc-init`, `doc-compact` and `doc-update` for compatible Agent Skills hosts. Python 3 is required for the bundled helpers. Start a new conversation after installation.

## First use

```text
Use doc-init to establish documentation for this project from its existing authorities.
```

For an existing project, choose the skill matching the work:

| Skill | Purpose |
|---|---|
| [doc-init](doc-init/SKILL.md) | Install or upgrade the global documentation contract, establish missing project documentation, or refresh affected coverage. |
| [doc-compact](doc-compact/SKILL.md) | Audit or compress the authorized documentation scope, preserve adopted requirements and repair navigation. |
| [doc-update](doc-update/SKILL.md) | Persist reusable findings and product decisions, correct stale documentation, and check session omissions. |

For a read-only review, say `Use doc-compact to audit this project's documentation without changing files.` For routine maintenance, say `Use doc-update to record this task's reusable findings in their owning documents.`

## Operating boundaries

Record adopted durable decisions before implementing them. Use accurate content summaries so an ordinary task can discover its relevant standards before a design decision. Preserve scope, exceptions, evidence, numbers and machine-parsed markers during compression.

The current documentation preset is v21. Its injector discovers real global instruction files and preserves neighboring user and managed content. It does not inject the global preset into product instruction files. Root `AGENTS.md` edits use the separate `agents-md-edit` skill; report a missing capability instead of bypassing it.

Execute directly by default. External workers require explicit authorization and follow the current environment's model policy; these skills do not authorize native subagents. Read-only audits do not install presets or repair files. Bounded maintenance does not imply a full repository census. Permission, language, Git/release, memory, platform and model policies remain with the user and environment.

Helpers gather inventory, code signals, history and optional database evidence; the agent still determines domain ownership and business meaning. Link and coverage reports establish only what was actually checked. Home-relative Markdown targets are resolved as complete paths; a successful report does not prove semantic preservation or future model adherence.

## Maintenance

The maintained source is `~/.config/agentsync/skills/`. This repository is published from that source. Keep reusable project knowledge in its owning documents and report missing evidence rather than inventing it.

## License

[MIT](LICENSE).
