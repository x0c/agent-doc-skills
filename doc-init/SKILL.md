---
name: doc-init
description: Establish or refresh project documentation coverage and install the global documentation lifecycle preset. Use for missing documentation structure, stale domain coverage, or a missing/outdated global documentation contract.
---

# Documentation initialization

Establish missing project documentation or refresh stale coverage. Follow the installed documentation lifecycle; environment instructions own language, memory, permissions, release, model selection and paths. Use `agents-md-edit` for deliberate AGENTS.md changes. Delegate only under current user authorization.

## Choose the work

- **Global preset installation/upgrade:** read the global-file discovery and upgrade sections of [maintenance workflow](references/maintenance-workflow.md#phase-1-validate-and-repair-global-ai-instruction-files). Discover real global targets and use `scripts/insert_doc_governance.py`; never inject into a product AGENTS.md.
- **Project creation or takeover:** read the project workflow in [maintenance workflow](references/maintenance-workflow.md#phase-2-initialize-the-current-projects-documentation-system). Discover declared standards, existing docs and real domain boundaries before generating material. Record durable decisions before implementation.
- **Existing project coverage refresh:** use the affected-domain sections of that workflow. Prefer current authoritative documents; do not regenerate unrelated coverage.

Read workflow references only when the selected phase needs them. Code, logs, database evidence, Git history and user decisions serve different questions; apply the workflow's evidence and data-safety boundaries rather than reading every source by default.

## Completion

Verify product truth, doc reachability, portable paths, content-summary navigation, conflicts and the actual runtime path when applicable. Report covered domains, remaining limits and any source changes. No unverified requirement is adopted merely because it appears in a template.
