# Document Templates

This document defines templates and root-entry rules used when doc-init generates project docs. Read it after the knowledge-boundary report and targeted Q&A.

## Contents

- Domain knowledge-base template
- Guide template
- [Feature intake brief (optional)](#feature-intake-brief-optional)
- Root AGENTS.md
- Project-root CLAUDE.md

## Domain knowledge-base template

Generate and write the file immediately after that domain’s Q&A—do not wait for other domains.

Use the applicable sections below. Where a domain has no persistence, state machine, or background jobs, say so briefly; do not invent content to fill the template. Keep actual coverage gaps distinct from non-applicable sections.

Before generating, finish domain-language normalization: pick one canonical term for core concepts and use it stably in body text; keep code class/enum/table/field/API parameter names verbatim in entry indexes or first-appearance parentheses. Do not default a “Glossary” section. Only homonyms, synonyms, or parameter mix-ups that would make AI write wrong code go into §6 `【Disambiguation】`.

```markdown
# [Domain] Knowledge Base

## §0 Contents

| § | Title | When |
|---|------|------|
| §1 | Business background and core concepts | First contact with this domain |
| §1.5 | Architecture overview | Quick layered mental model (mermaid) |
| §2 | Core business flows / state machines | Main flows and status enums |
| §2.5 | Physical path cheat sheet | Locate code dirs directly (glob/ls) |
| §3 | Code entry index | Find entries by task scenario |
| §4 | Table and field entry index | When changing tables/fields/queries |
| §5 | Flow / component / job / MQ entry index | When changing orchestration / cron / messaging |
| §6 | Core business rules and hidden constraints | AI pitfalls to scan before changing code |
| §7 | Validation paths | How to verify correctness after changes |
| §8 | Related docs | Cross-domain reading guides |
| §9 | Coverage and to-be-filled items | Doc confidence and gaps |

## §1 Business background and core concepts
[Business positioning, who it serves, role in the system, core concepts. Use unified canonical terms; on first appearance, parenthesize code entity / enum / main table aliases when needed]

## §1.5 Architecture overview

[Use a diagram when it clarifies actual relationships, transitions, or event ordering. A simple domain may need only a short flow description.]

**Diagram selection guide** (pick the type that most reduces cognitive cost for the domain):

| Domain trait | Recommended diagram | mermaid syntax |
|--------|---------|-------------|
| Clear layered calls (Controller→Service→Repository) | Layered call graph | `graph TD` |
| State transitions are core (order/approval/account) | State machine | `stateDiagram-v2` |
| Event-driven / async (MQ/Event/callbacks) | Sequence | `sequenceDiagram` |
| Complex entity relations (multi-table / aggregate roots) | ER | `erDiagram` |
| Inheritance / strategy (multiple implementations / plugins) | Class hierarchy | `classDiagram` |

- Prefer: choose from the table by domain trait; fill real project class names
- Label nodes with actual class/component names—no abstract placeholders
- Complex domains may combine two types (e.g. layered + state)

## §2 Core business flows / state machines
[Main flows, status enums, transitions, terminal states, idempotency semantics, key branches]

## §2.5 Physical path cheat sheet

| Directory (relative to project root) | Contents | Key classes / file count |
|------|------|--------|
| [full relative path; no `...` ellipsis] | [code kinds in this dir] | [representative class names or file count] |

Paths must start from the project root (e.g. `src/main/java/com/example/payment/service/`); do not omit middle segments with `...`. Agents should glob/Read the target without a second search for physical location.

## §3 This domain’s code entry index
| Scenario | Entry | Class/method/config | Notes |
|---|---|---|---|
| [when doing which task] | [API/service/component/job/MQ] | [path or symbol] | [responsibility] |

## §4 This domain’s table and field entry index
| Table/field | Entity/Mapper | Business meaning | Change notes |
|---|---|---|---|
| [table.field] | [class] | [field meaning] | [sharding/tenant/status/money/time notes] |

## §5 This domain’s flow / component / job / MQ entry index
| Type | Id | Code entry | When used |
|---|---|---|---|
| [Flow/Component/Job/MQ/Cache] | [flow_code/topic/key/id] | [class/method/config] | [when it applies] |

## §6 Core business rules and hidden constraints
- 【Forbidden】[practice] -> must [correct practice] (reason: [why])
- 【Hidden dependency】before [A] must first [B], else [consequence]
- 【Disambiguation】[concept A] vs [concept B]: [difference, interchangeable?, wrong-use consequence]
- 【Naming alignment】[canonical] may also appear as [alias] in code/tables/APIs; body text always uses [canonical]; when changing code, locate implementation names via the entry index (write only when aliases would cause misjudgment)
- 【Implicit semantics】[hidden mechanism] automatically runs [real logic] at [trigger entry]; when changing [scenario] also check [config/context/generated code/external contracts], else [AI pitfall consequence]
- 【Low confidence】[inference] (evidence: [code]; pending: [what user must fill])
- 【Ruling】[YYYY-MM-DD] User confirmed overturning [original authoritative conclusion]: [correct conclusion for this product/domain] (reason: [why source is outdated/inapplicable]). Future doc-init/doc-update that reads this must not reverse it unless the user changes their mind again; recommend syncing the source doc (e.g. backend PRD), but this repo must not edit across repos on its own.

**AI pitfall tag rule:** If a hidden-constraint item is a mistake AI would make without reading docs (forgetting context, forgetting versioned updates, wrong field names), prefix with `**AI pitfall**`. That lets later Agents scan for the most dangerous constraints immediately. Items tagged concurrency_patterns, idempotency_patterns, or soft_delete_patterns in depth_scanner.py output should default to AI pitfall tags.

## §7 Common easy-to-miss conditions and validation paths
- After changing [scenario]: run/call [command or API], check [logs/tables/flow records/cache]
- Note: [effect conditions common in this domain but not directly reminded by code]

**Validation paths evidence the domain’s real surface.** If real commands cannot come from runtime validation, generate template validation paths from code scan using the domain’s real entries:

- DB validation (persistence scenarios): `SELECT <key_fields> FROM <main_table> WHERE <condition> -- confirm <field> changed to expected value`
- Log validation (logging scenarios): `grep '<keyword|exception class>' <log_path> | tail -5`
- API validation (HTTP scenarios): `curl -s -X POST http://127.0.0.1:<port>/<path> -H 'Content-Type: application/json' -d '<minimal body>'`
- Cache/state refresh (caching scenarios): `curl -s -X POST http://127.0.0.1:<port>/<refresh_path>`
- Compile validation (compiled languages): `<build_command> && echo "build ok"`
- Unit-test validation (when tests exist): `<test_command> -t <TestClass>#<testMethod>`

Replace `<placeholder>` with this domain’s real entries. Low-confidence validation paths note “pending runtime validation”. Where the domain has no validatable runtime surface, say what was checked and record the gap in §9—do not invent executable commands.

## §8 Related docs
- [GUIDE doc]: covers [shared/specialized mechanism] details; read together when that mechanism is involved
- [Other domain KB]: read together for [cross-domain scenarios]

## §9 Coverage and to-be-filled items
- Code-inference coverage: [entities/status/entries/tables/flows coverage]
- Domain-language unification: [canonical confirmed?; aliases / conflicting names still pending]
- User / materials: [requirements, API docs, test cases, log entry points, veteran experience]
- Multi-source evidence enrichment: [tests/API contracts/frontend/config/migrations/logs/external contracts/permission dicts/generated metadata/runtime evidence actually read; only list evidence that truly reinforced this domain]
- Q&A supplements: [N hidden constraints / M disambiguations / K validation paths]
- To be filled: [business experience neither code nor current Q&A covers; unread test assertions, unverified runtime SQL, unconfirmed frontend menu names, unconnected config center, and other high-value gaps]

<!-- Generated by doc-init on YYYY-MM-DD; positioning: quick reference before AI changes this business domain -->
```

Do not fabricate historical incidents or real pitfalls. If the user volunteers past issues in Q&A, you may write “common easy-to-miss conditions” or “pending doc-update persistence”; without evidence, mark low confidence or to be filled.

Immediately after generating a doc, add a precise, concise content summary to root `AGENTS.md` (or the appropriate registered secondary index). Root `AGENTS.md` document navigation has one shared instruction to read documents whose described content is relevant to the current task. Do not turn individual entries into trigger lists or duplicate policy.

Example: `docs/PAYMENTS_KNOWLEDGE_BASE.md`: payment lifecycle, callback handling, refunds, idempotency, and failure recovery.

Use content summaries; the single shared relevance instruction handles task routing.

```bash
python3 <DOC_INIT_DIR>/scripts/upsert_agents_nav.py --root . --path docs/<DOMAIN>_KNOWLEDGE_BASE.md --summary "<concise summary of the document content>"
```

## Guide template

When a cross-domain shared mechanism or complex specialized mechanism is identified, generate `docs/<TOPIC>_GUIDE.md`. Guides extract complex mechanisms only—they do not replace domain KBs; related domain KBs must keep this domain’s entries and usage.

Granularity judgment before generating:

- If the mechanism affects multiple business domains and AI needs an independent runtime pipeline / real-effect model before changing code → Guide.
- If it only serves one business domain → write into that domain KB’s “Core business rules and hidden constraints”.
- If multiple hidden points belong to one pipeline → merge into one Guide; do not split by annotation, field, hook, or single config key into many tiny docs.
- Historical accidents or one-off failures → do not generate during doc-init.

```markdown
# [Mechanism] Guide

## Document positioning
[Mechanism boundaries this Guide covers, applicable modules/domains, main entries, and what it does not cover. Do not repeat the shared index relevance instruction.]

## Mechanism positioning
[What problem it solves; which business domains depend on it]

## Core entries
| Scenario | Entry | Code/config | Notes |
|---|---|---|---|

## Usage constraints
- 【Must】[mechanism rules that must be followed]
- 【Forbidden】[approaches that look reasonable but are not allowed in this project]
- 【Hidden dependency】[actions that must sync before/after using the mechanism]

## Domain references
- [DOMAIN_A_KNOWLEDGE_BASE.md]: [how this domain uses the mechanism]
- [DOMAIN_B_KNOWLEDGE_BASE.md]: [how this domain uses the mechanism]

## To be filled
- [Content code cannot reconstruct; needs user or later doc-update]
```

After generating a Guide, sync the “Related docs” sections of related domain KBs, and add a concise content summary to root `AGENTS.md`.

Guide root nav also uses `scripts/upsert_agents_nav.py`.

## Root AGENTS.md

Prefer creating/updating the root `AGENTS.md` frame first, then generating `docs/`; after each long-lived doc, immediately write nav so a mid-run failure does not leave orphan docs undiscoverable from the root entry.

Root `AGENTS.md` includes:

- Project intro: 2–3 sentences—what it is, whom it serves, core tech traits.
- Coding conventions: framework choices, must/forbidden coding patterns.
- Validation: how to start, how to validate typical changes.
- Doc navigation: summarize domain KBs and Guides accurately and concisely. Project files keep the literal key `## 文档导航`; the helper also recognizes `## 规则索引`, `## Document index`, and `## Documentation index` in existing instruction files, so it reuses their heading rather than creating a competing section.

### Ops cheat sheet (runnable projects only)

When `depth_scanner.py` `runnable_project.type` is not `library`/`cli`/`unknown`, generate this section in root AGENTS.md:

```markdown
## Ops cheat sheet

| Service | Port | Start command | Log path |
|------|------|---------|---------|
| [fill from depth_scanner output] | | | |

### Build commands
- [derive from inventory build_system]

### Common compile issues
- [extract from Git fix/revert history and code scan; may start empty]
```

Pure library/SDK/CLI tool projects skip this section; put “how to validate” into root AGENTS.md project behavior rules or the relevant Guide.

Project-root `AGENTS.md` must not reference user-level or global instruction files, e.g. do not write `@~/.claude/CLAUDE.md`. Global rules are loaded by the client automatically; project-root `AGENTS.md` only carries this project’s rules, validation methods, and doc nav.

Nav rules:

- Domain KBs first: cluster by business module / domain / line; high-frequency domains earlier.
- Shared Guides next: flow orchestration, sharding routing, permissions, plugin components, ops validation, and other horizontal mechanisms after domain KBs.
- Each entry summarizes the actual document content; one shared instruction tells Agents to read documents relevant to the current task.
- Do not flatten by tech resource: do not make tables/classes/APIs the main root-nav structure; those indexes live in the corresponding domain KB.

After generate/update, run:

```bash
python3 <DOC_INIT_DIR>/scripts/doc_nav_lint.py --root .
```

Fix errors before finishing; for warnings, either fix or explain in self-assessment why they are temporarily accepted.

## Root CLAUDE.md

Write or normalize to a single line:

```markdown
@AGENTS.md
```

`CLAUDE.md` is only Claude Code’s pointer into project-root `AGENTS.md`—no project rules, doc nav, or global rules.

## .gitignore

Check for `DRAFT_*.md` and `*-draft.md`; if missing, suggest adding them.

## Feature intake brief (optional)

When a data-backed or analytics feature request needs scoping before a formal spec,
an optional short brief may precede it. This is a scoping aid, not a required gate,
and its shape stays product-owned:

- Problem statement, target users, and decision/output form first — if the output
  cannot be named clearly, the request is not ready for a formal spec.
- Quantified freshness expectation with staleness tolerance: which dependencies may
  go stale and the upper bound (e.g. same-day vs next-day usefulness under T+0/T+1
  disclosure lag).
- Candidate capabilities mapped capability-before-vendor, known limits, reuse
  opportunities, directional success signals, open questions, and an explicit
  outcome (proceed to spec / research first / split / defer / reject).
- Normalize vague local terms as a step using the product's own vocabulary.

---

## Deep-write standards

### Investigation depth

Use the applicable checks below to establish useful coverage. Their order and repetition depend on what remains unknown; they are not compulsory rounds.

**Vertical trace:** Follow the domain's real trigger (API, CLI command, public library function, event, or job) through its logic and effects, including persistence where present. Record relevant symbols, branches, and full repository-relative paths in §2/§2.5/§3. Follow across module boundaries when the flow crosses them; do not invent absent layers.

**Cross-cutting checks:** Inspect applicable concurrency, idempotency, event ordering, scheduled work, and failure/recovery behavior. Write confirmed constraints with evidence in §6; record unresolved risks in §9. Continue investigation for a concrete gap, not to reach an item count.

**Field and format semantics:** Where data exists, verify key-field types and meanings: identity, ownership, NULL behavior, status/version fields, relations, money, and time. Follow JSON/DSL decoding when relevant signals identify it. Core or high-risk domains need deeper evidence for their consequential branches and related data; a table row count does not establish this.

**Architecture overview:** Use the diagram selection guide when a diagram improves understanding of the inspected structure; label actual components. Do not add a diagram solely to satisfy a template.

**§2.5 physical-path data source:** Prefer directories from `depth_scanner.py` `framework_components[].file_path` and `entity_fields[].file_path`; dedupe and fill the §2.5 table. Sub-agents need not re-walk the tree—the scanner already did.

**Forbidden:** using only a sub-agent’s module-level summary as generation basis—sub-agent scan is “candidate discovery”; deep-write must return to code to verify key assertions.

**Anchoring rule (hard):** When citing code locations, **do not use line numbers** (e.g. “line 535”, “Line 42”); use `ClassName.methodName()` or `ClassName.methodName() → CalledMethod()`. Method names are stable; line numbers drift and invalidate docs.

**Line-number replacement ops guide** (for doc-compact): when seeing line-number citations, Read that file at the line to confirm the current method name, then replace with `ClassName.methodName()`. Do not guess.

**Adequacy over length:** No per-KB line minimum. A short KB is complete when its entries, constraints, and validation paths evidence the domain’s real surface; a long KB with invented entries or an unresolved high-value gap is not. Investigate or backfill only for a concrete gap or unresolved risk.

### Deep-write quality gates (self-check immediately after each KB)

| section | Adequate when | If not |
|---------|---------------|--------|
| §2 Core flows/state machines | Real transitions and key branches evidenced (enum values + meanings where state exists); pure CRUD/library/CLI domains describe the actual request-handling or command flow | Supplement from `status_patterns`, or record the concrete gap in §9 |
| §3 Code entry index | Every entry resolves to a precise file path or symbol and covers the domain’s real trigger → logic surface | Supplement from `framework_components`; do not invent layers the domain lacks |
| §4 Table/field entries | Real persistence evidenced (types + business meaning + change notes for fields the domain actually has); domains without tables say so | Supplement from `entity_fields` + db_miner catalog, or mark non-applicable with reason |
| §6 Hidden constraints | Applicable risks checked; confirmed findings supported by source evidence and AI pitfalls tagged; no findings reported honestly | Follow relevant scanner signals; unresolved risks stay open in §9 |
| §7 Validation paths | Real commands/queries against real entries; template-level paths allowed only when marked “pending runtime validation” | Derive from actual entries; missing runtime evidence is a §9 gap, not a filled quota |
| §0 Contents | Accurately lists the sections present | Adjust the template to the actual document |
| §1.5 Architecture overview | Inspected relationships are understandable; diagram used where helpful | Choose a diagram or concise flow description suited to the domain |
| §2.5 Physical path cheat sheet | Full paths resolve to the relevant implementation | Summarize verified paths; row count follows the real surface |

**Completion:** Representative ordinary and exceptional change scenarios must find the needed entries, constraints, and validation paths. Give core/high-risk domains deeper evidence for consequential identity, concurrency, persistence, and field-semantics branches. Record evidence limits honestly; unresolved high-value gaps prevent a claim of complete coverage. No minimum length or number of rounds, constraints, paths, or commands applies.
