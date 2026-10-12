---
name: doc-update
description: Promote cross-project knowledge to shared authorities, persist product decisions, repair stale documentation and navigation, and review session omissions. Use during work when durable knowledge emerges, including investigation-only Q&A, and at task closure.
---

# Documentation updates

Apply the documentation lifecycle contract in the installed `Project Documentation Management` block. This skill supplies the bounded update procedure; environment instructions own language, permissions and shared-document locations. When `AGENTS.md` needs a deliberate edit, route one bounded change set through the dedicated `agents-md-edit` skill; the coordinator integrates and verifies it. If unavailable, report the missing capability.

## 1. Gather and filter

Review the available session for knowledge that would otherwise disappear:

- Replay user requirements, corrections and vetoes. Check redirects, confusion, repeated requests, better-default expectations, surface-only fixes, unused available resources and inefficient paths. Separate durable intent from temporary scope, examples and unadopted suggestions.
- Replay task-level detours: failed approach, cause, successful remedy and verification. Do not record repetitive tool failures that taught nothing.
- Look inside incident fixes, environment/tool integration, configuration and release acceptance, design research, and repeated failures for reusable mechanisms hidden among product details. An existing project write-up does not establish project ownership of the knowledge.
- Identify docs invalidated by changes, newly exposed contradictions, and cases where the right doc was missing, misleading or not found.
- Ask whether the workaround would still be necessary with perfect docs. If yes, record an environment-improvement item alongside the documented workaround; do not implement unrelated improvements automatically.

Then apply the precision test: would this spare a new Agent a non-obvious mistake or rediscovery? Preserve relevant business rules, hidden constraints, verified workflows, applicability and evidence. Skip code/Git restatement, duplicates and session-only narrative. Search existing docs before deciding nothing needs updating. Pure Q&A is not a skip condition.

If no new durable knowledge remains, report that no update is needed. If documentation changes are explicitly forbidden, report the unpersisted findings without writing.

## 2. Locate the authority

Read the effective global and project `AGENTS.md` entry points and follow their relevant navigation and declared shared standards.

Before writing, separate product-specific facts from reusable causes, constraints, procedures and verification methods. Would another product under the same conditions benefit without this product's particular contracts or values? If so, locate the shared owner; a second occurrence is not required. Preserve applicability, exceptions and confidence rather than turning a product default or observed workaround into a universal rule.

For a reusable or mixed finding, search the relevant shared and project authorities and read their actual bodies. A related title or existing mechanism does not prove coverage of this finding, symptom or failed remedy. Link to sufficient coverage; enrich the authority when the session establishes a missing variant or correction.

| Finding | Destination |
|---|---|
| Project-wide operating requirement | Matching root `AGENTS.md` section |
| Product behavior, architecture or domain knowledge | Existing matching project doc |
| Reusable task procedure or helper | Matching skill; no product-specific names or paths |
| Cross-project platform/language facts, runtime constraints, troubleshooting or verification knowledge | Declared shared guide/standards; product doc retains local details and a pointer |
| Recurring environment obstacle | Existing backlog, or an indexed design/troubleshooting entry |

Prefer updating an existing authority. If a new document is needed, select its owner first, then use that location's registered doc types and navigation. Project doc types are not the default fallback for shared knowledge. If the shared destination binding is missing, report it explicitly; a nearest reachable temporary record remains provisional, not completed promotion. Do not invent a shared filesystem location. Register a new type's purpose and placement when needed.

## 3. Update and reconcile

1. Write current requirements and reusable knowledge, not a session diary. Label hypotheses and unverified steps; distinguish pending decisions from confirmed facts.
   Persist the reusable layer in its shared authority while retaining product contracts, parameters and incident evidence locally. Before replacing generic local prose with a pointer, confirm that the shared body preserves its useful meaning and scope. Do not create a project copy merely to mirror a shared finding.
2. Check affected code/path/method anchors against the source. For KBs using the doc-init template, update the physical-path table and affected flow/validation sections after renames, deletions or entry changes; do not maintain source file counts merely to duplicate the code.
3. Correct old conclusions within the concepts touched this session. Verify against authoritative requirements and implementation; a confirmed new product decision may supersede stale implementation. Keep implementation aliases when changing business terminology.
4. When a user explicitly overrides an old source, record the current ruling, rationale and scope so the old source cannot silently reverse it. Mark unresolved contradictions with the decision required.
5. Propagate approved corrections and synchronize affected references under the current task authorization. Do not use a retrospective to overhaul unrelated docs or change unrelated global rules.

## 4. Repair navigation

For each added, moved, renamed, expanded or previously missed doc:

- Ensure exactly one navigation entry at the root or a registered secondary index. Nearby rule pointers may coexist with that entry.
- Describe each document's actual content precisely and concisely. Keep one shared index instruction to read documents whose described content is relevant to the current task; do not turn entries into trigger lists or duplicate policy.
- Update the content summary when document contents change. Preserve valid entries while merging duplicates or removing stale summaries.
- Synchronize old references after moves/deletions and add nearby pointers where the doc supports a rule.
- Keep direct links unless a group makes navigation difficult to scan. Three records alone do not require a secondary index; use doc-compact for large-scale restructuring.

Mechanical link checks can use doc-init's `scripts/doc_nav_lint.py` or doc-compact's `scripts/audit.py`. Their output does not replace checking task coverage and factual consistency.

## 5. Verify and report

Re-read changed passages and navigation; verify links, current conclusions and recorded limitations. Check that a new Agent could perform the affected task from the docs without repeating the discovered detour.

Review the documents written or directly affected this session for established reusable knowledge still left only in a project doc. Promote a missed shared layer within the bounded update, or report the missing binding/evidence and provisional location. This check does not require a workspace-wide census.

Report changed authorities, what was promoted or corrected, and which product details remain local. Name any unpersisted, unverified or unpromoted item and why. If the session produced no durable change, say so without forcing a document edit.
