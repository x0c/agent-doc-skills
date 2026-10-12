# Sub-agent Deep-Write Prompt Template

Use this work-brief template only for explicitly authorized external workers. It does not authorize delegation or native subagents; runtime, model and UI ownership follow the current environment. Structured evidence and concrete boundaries reduce repeated exploration and improve deep-write quality.

---

## Core principles

1. **No re-exploration:** The main Agent finished project-level scanning in Step 8 (inventory + depth_scanner + git_history + DB catalog). Sub-agents must not re-grep known entries. The prompt must pass known signals directly; sub-agents only do **confirming reads** (verify signals are real) and **incremental discovery** (details the main Agent missed).
2. **Input determines depth:** Sub-agent output depth ≈ number of concrete signals in the prompt. “Deep-write the payment domain” yields skeleton docs; five status enums + three concurrency patterns + entry file lists yield usable docs.
3. **Constraints determine consistency:** When multiple sub-agents run in parallel, canonical terms, filename conventions, and quality-gate standards must be issued uniformly in the prompt—or each will diverge.

---

## Prompt structure template

Organize the sub-agent prompt as follows (in order; every item must exist or be explicitly marked “none”):

### 1. Task definition

```
You are a doc-init deep-write Worker. Your task is to produce a complete domain knowledge-base document for the "{domain name}" business domain.

Output file: `docs/{DOMAIN}_KNOWLEDGE_BASE.md`
Template: follow the doc-init KB template (§1–§9); adequacy follows document-templates.md evidence criteria. Sections with no applicable content state what was checked and why non-applicable (or record the concrete gap in §9) rather than inventing content.
```

### 2. Domain business scope

```
Business scope: {one-sentence definition}
Includes: {list of covered capabilities}
Excludes: {explicitly excluded capabilities}
```

**Why “Excludes” matters:** With parallel domains, unclear boundaries cause two sub-agents to duplicate content or both miss pieces.

### 3. Known entry inventory

File paths already determined by the main Agent from Step 8 inventory + manual exploration:

```
Known entries (do not re-search; read to confirm):

Controller:
- {absolute file path} — {responsibility}
- ...

Service/core classes:
- {file path} — {responsibility}
- ...

Entity/Model:
- {file path} — {main table name}
- ...

Repository/Mapper:
- {file path}
- ...
```

### 4. Depth Scanner signals

Signals filtered by domain from `.doc-init-depth-scan.json`:

```
Identified signals (read code to confirm; then write into the matching section):

Status enums (→ §2):
- {enum class path}: {summary of enum values}

Concurrency control (→ §6 AI pitfalls):
- {file + symbol}: {pattern description, e.g. "@Version optimistic lock"}

Idempotency (→ §6):
- {file + symbol}: {idempotency key source description}

Events/MQ (→ §5):
- {publisher file} → {topic/event} → {consumer file}

JSON fields (→ §6 format rules):
- {entity.field}: deserialize target {DTO class}

Hot files (→ §7 annotation):
- {file path}: {recent N changes concentrated here}
```

**Handling rule:** Signals are candidates, not conclusions. After confirming in code, write into body text; if false positive, discard and explain in §9.

### 5. Canonical-term table

```
Domain language (body text must use canonical terms; implementation names only in parentheses at first appearance and in entry indexes):

| Business concept | Canonical term | Implementation aliases (code/table/API) |
|---------|--------|------------------------|
| {concept} | {canonical} | {class, table, field} |
```

### 6. User Q&A results (if any)

```
User supplements (high weight; trust directly):
- {Q&A pairs}
- ...

If no user Q&A, mark in §9: “Missing user experience input”.
```

### 7. Known interfaces of related domains

```
Related-domain info (write into §8 related docs + §6 cross-domain constraints):
- {Domain A} interacts with this domain via {API/MQ/event}: {interaction description}
- Shared Guide candidates: {mechanism name} — {list of involved domains}
```

### 8. Quality gates

```
Quality gates (evidence-adequate per document-templates.md; backfill concrete gaps, never invent content):

- §2 Core flows/state machines: real enum values (code + meaning) evidenced; where no state machine exists, describe the actual request-handling or command flow
- §3 Code entry index: precise to file path or symbol (not package names only); cover the domain's real trigger → logic surface—do not invent controllers, repositories, tables, or state machines for library/CLI domains where absent
- §4 Table/field entries: real persistence evidenced (type + business meaning + change notes for fields the domain actually has); domains without tables say what was checked and why non-applicable
- §6 Hidden constraints: each confirmed finding with code evidence (file + symbol or inspected snippet); AI pitfalls must be tagged
- §7 Validation paths: real commands/queries against real entries; unavailable runtime evidence is honestly marked "pending" with a §9 gap, not filled with invented paths
```

### 9. Constraints and forbidden behavior

```
Hard constraints:
- Create/modify only `docs/{DOMAIN}_KNOWLEDGE_BASE.md`
- Do not modify AGENTS.md, other domains’ KBs, or shared Guides
- Code paths must be precise to file path or symbol—not package or directory only
- Hidden constraints must cite file + symbol or an inspected snippet—not “inferred”; report unavailable or non-applicable evidence honestly instead of inventing it
- Do not fabricate pitfalls or production incidents
- Comment/log language follows the global AGENTS “Coding” section; this template does not set a separate language default
```

---

## Example: main Agent assembling the prompt (pseudocode)

```
For each deep-write domain D:
  1. Extract D’s business scope and entry inventory from the knowledge-boundary report
  2. filter(domain == D) from .doc-init-depth-scan.json → signal list
  3. Take D’s canonical-term table from Step 8 domain-language normalization
  4. Take Q&A pairs related to D from Step 9
  5. Extract interfaces that interact with D from other domains’ boundary reports
  6. Assemble the full prompt from the template above
  7. If explicitly authorized, dispatch the external worker using the current permitted model policy; otherwise execute directly.
```

---

## Investigation and completion

Use document-templates.md “Deep-write standards” for the applicable investigation and adequacy checks; there is no fixed round count.

Read the supplied entries to confirm real flows and effects, then investigate the unresolved branches and relevant risks. Validate the resulting document against representative ordinary and exceptional changes. Return the final file once the assigned coverage is evidenced; report material gaps rather than padding the document or claiming complete coverage.

---

## Output acceptance

After a sub-agent finishes, the main Agent should check:

| Check | If failed |
|--------|-------------|
| §2 evidences real transitions or the actual command/request flow | Identify the missing branch from source and request a precise correction |
| §6 applicable risks checked and findings supported by evidence | Request the missing evidence; unresolved risks stay open in §9 |
| §7 has real paths or honestly-marked pending validation | Verify against actual entries; identify material validation gaps |
| Filenames / canonical terms aligned with other domains | Main Agent unifies |
| No cross-domain content intrusion | Main Agent removes out-of-scope content |
| No invented layers for library/CLI domains | Main Agent removes inventions; non-applicable sections state what was checked |
