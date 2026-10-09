# doc-compact

Apply the installed `Project Documentation Management` lifecycle contract. Environment instructions own language, permissions, model selection and shared-document locations. Route deliberate `AGENTS.md` edits, including navigation and compression, through the dedicated `agents-md-edit` skill as one bounded change set; the coordinator integrates and verifies the result. If unavailable, report the missing capability.

Before running, discover the files that are actually in effect—do not hardcode paths.
`<DOC_INIT_DIR>` defaults to a sibling of this skill: `<directory of this SKILL.md>/../doc-init`

## Flow

**Step 1 validate global rules → Step 2 read-only audit → Step 3 decide secondary indexes → Step 4 fix structure → Step 5 compress (core, non-skippable) → Step 6 verify**

---

## Step 1 — Global rules (may write)

For an explicitly read-only audit, inspect the installed contract and run Step 2 only. Report proposed changes; do not run the injector, stamp files, or execute repair/compression steps.

**Target files are global AI instruction files only**—never pass a project `AGENTS.md`:

```bash
python3 <DOC_INIT_DIR>/scripts/discover_global_instruction_files.py
```

Exit `0` prints unique real paths (one per line). Exit `3` means none of the candidates exist — report that and ask the user for their global instruction file. Do not hand-roll a bash `readlink` loop (breaks on Windows).

For each printed path, run: `python3 <DOC_INIT_DIR>/scripts/insert_doc_governance.py <global-file-path>`.
The script prints `[skip]` = already current; `[added]` / `[upgrade]` = written—then migrate only explicitly reviewed duplicate clauses. Preserve unrelated non-managed text; no theme-based deletion.
If `<DOC_INIT_DIR>` is missing, use the installed lifecycle contract for project work and report that preset installation could not be verified. Do not inject `references/standard.md`; it is an operational checklist, not the preset.

**Do not** pass the current project’s `AGENTS.md` to `insert_doc_governance.py`—project `AGENTS.md` holds project rules, not global AI instructions; writing into it pollutes project docs.

## Step 2 — Read-only audit

**Multi-component monorepo (no root `docs/`; docs live in sub-repos):** first find subdirectories that contain `docs/` or `specs/` and also `AGENTS.md` (skip `worktrees` / `node_modules` / `.git`), and run `audit.py` on **each** doc host; at the root only check CLAUDE/`AGENTS` size and navigation pointers. Do not audit only the repo root and miss `backend/docs`, `client-web/docs`, etc.

Run `python3 scripts/audit.py [project-root or sub-repo root]` to finish machine-checkable items in one pass:

- **A** Every CLAUDE.md is a single `@*.md` line
- **B** No dangling `@AGENTS.md`
- **C** No bare `OVERVIEW.md`/`INDEX.md`; named `<DOMAIN>_INDEX.md` is valid
- **D** AGENTS.md line count (> 500 lines → Step 3)
- **E** No orphan docs (under docs/specs not referenced by root AGENTS.md ∪ README ∪ `*_INDEX.md`)
- **F** File naming compliance (troubleshooting `YYYY-MM-DD-*`, review `*-review.md`)
- **G** Preset fold suggestions (troubleshooting / Review ledgers ≥3 docs, advisory; includes `operations/` incident candidates—see Step 3)
- **H** doc-init linkage: reverse global refs, domain-map section presence → **affects Step 4/5 protection boundaries**
- **I** Compact-stamp hard gate — Step 6 only; needs `--compact-date`, so the read-only Step 2 pass reports `⏭ skip`
- **J** AGENTS.md bloat metrics (chars / estimated tokens / rule count / emphasis density) and managed-block detection: paired `<!-- name:begin/end -->` markers are listed as 🔒 managed blocks (preserve verbatim on Step 4 index rebuild—do not compress or delete); unpaired markers report ❌. Only this markdown HTML-comment convention is recognized; other styles are left to agent judgment

In Step 2 also pass `--save-metrics <baseline-path>` to save the AGENTS.md metrics baseline; Step 6 uses `--compare-metrics` for before/after (estimated token increases get ⚠ and must be explained in the close-out report).

Human follow-ups (not scripted in `audit.py`):

- **§2.5 path liveness:** for every KB that contains a `§2.5 物理路径速查` / physical path quick-lookup section, `ls` each listed path; STALE paths go into Step 5 cleanup (command in `compression-guide.md` → “§2.5 path liveness”)
- Misplaced docs, redundant bloat, volatile facts restated across docs (`grep -rn "concrete number" docs/`; >2 hits is suspicious)

### Protected sections

When H shows `domain_map_present=True`, keep the root AGENTS.md sections `## 领域地图（doc-init）` / Domain map (doc-init) and `## 待补充知识库（doc-init backlog）` / Knowledge-base backlog (doc-init) **verbatim**—do not compress, fold, or delete them.

## Step 3 — Decide secondary indexes

Default is a single flat layer. **Prefer not to add levels**—each extra hop multiplies miss-read risk.

Fold only when a group makes navigation hard to scan. A large navigation share, >500 root lines, or ≥3 related incident/review records are audit signals, not automatic triggers. Keep direct links when they remain clear.

When folding, root links a named `<DOMAIN>_INDEX.md`, which links original docs with concise content summaries. Keep one shared relevance instruction in root `AGENTS.md` document navigation. No third hop. Incidents in `operations/` also count as candidates; prefer a pointer index over moving files and changing every reference.

## Step 4 — Fix structure

- **CLAUDE.md:** not a single line → restore `@AGENTS.md`; only an injection block with no content → delete the dangling CLAUDE.md too
- **Doc naming/placement:** align with rules (knowledge bases/guides `SCREAMING_SNAKE_CASE`, design/review `kebab-case`, troubleshooting `YYYY-MM-DD-*`); review moves/renames against task authorization, then sync whole-repo references
- **Navigation summaries:** describe each document's actual content precisely and concisely; keep one shared relevance instruction in root `AGENTS.md` document navigation and remove trigger lists or duplicated policy
- **Index rebuild:** list only real docs, cluster by domain, high-frequency first; drop dead links/empty placeholders; skip protected sections; preserve 🔒 managed blocks from J verbatim
- **Unmanaged legacy injection / bare indexes:** identify rules, check existing coverage, then merge uncovered valid content and remove only authorized redundant material. This does not apply to the generated `Project Documentation Management` section or any managed block: preserve those and fix their source instead.
- **Inherited instructions:** identify their generating source and any reinjection hook. Fix broken routes in the source; do not erase a managed block or edit only its generated copy. Without a generating mechanism, remove a redundant block only after its still-valid rules remain reachable and the removal is authorized.

## Step 5 — Compress (core deliverable, non-skippable)

Full compression criteria and playbook: [`references/compression-guide.md`](compression-guide.md)—required reading before execution (read when compressing; pass to external workers only when delegation is authorized).

**Non-negotiable constraints:**

- Review every document in the authorized scope; whole-project cleanup covers `docs/` and `specs/`, while a bounded cleanup covers its affected documents and references. Report each document's before/after size or the reason no compression was appropriate. Do not silently skip scoped documents.
- The primary agent executes directly by default. External workers are optional only after explicit authorization under the current environment's delegation and model policy; do not start native subagents.
- For authorized workers, provide the full compression guide, the project's protected-section list, and the review-required items below. Protect root `## 领域地图（doc-init）` and `## 待补充知识库（doc-init backlog）`, KB §0/§1.5/§2.5 content, method-name anchors and managed blocks. Workers return high-risk decisions to the primary agent.
- Authorized workers touch only assigned bodies under `docs/` and `specs/`; the primary agent owns root instructions, navigation, indexes and cross-document reference integration.
- After any parallel work, run the guide's cross-shard consistency checks, reconcile criteria and facts, and verify protected sections before accepting results.

**Shard plan:** use the script to pack source plus expected output within the active model budget; override `--budget` for the current window.

```bash
# Must exclude .worktrees / build caches; do not count worktree copies as product docs (script already prunes)
python3 scripts/plan_shards.py <project-root>                          # per-doc token estimate + large-KB list + directory draft groups
python3 scripts/plan_shards.py <project-root> --domain-map <map.json> # final packing: main agent clusters by domain, writes map, passes it in
```

- Group work by domain, not physical directory, so related terms, state machines and constraints are reviewed consistently. Split only when the active context budget requires it. These groups are serial work batches unless delegation is authorized.
- The script detects large KBs (>20k estimated tokens); review each in a separate batch when needed. File size does not authorize a worker.
- On a new project’s first run, sample 3–5 docs to calibrate chars→token coefficient (script defaults adaptively pick 0.40/0.47/0.55 by content mix; override with `--coef` when far off)

Token coefficients and budget assumptions live in `plan_shards.py`; calibrate against representative docs and the actual model window rather than assuming a universal capacity.

**Execution tiers:**
- **Low risk, do directly:** restatement / dead links / historical narrative / empty placeholders / duplicate reminders / line-number refs (“line N” / “Line N” / “第 N 行” → Read first to confirm the method name, then replace with `ClassName.method()` anchors) / form conversion (narrative → call chains / tables / decision tables; information unchanged, form only) (list in the report)
- **Review scope and evidence before editing; follow active permission rules:** delete whole docs, rewrite large sections, split/merge index structure, edit body text that contains numbers/boundary conditions, delete §0/§1.5/§2.5 sections
- **On anomaly, fix now (no deferral):** repair skipped/duplicated numbering, repeated titles, broken tables, dangling references, disorder, incorrect names and cross-document duplication in the scoped update. Verify factual doubts against source. The primary agent owns changes affecting external references; an authorized worker may repair isolated defects inside its assignment. See the guide's “Fix anomalies on discovery” criteria.

**Delegation fallback:** when an explicitly authorized worker cannot start, follow the allowed retry/model policy and then continue serially if necessary. Report the actual execution and any unfinished scope; do not claim parallel completion.

**Second-pass compression is normal:** for architecture KBs / specs / playbooks last compressed >30 days ago, many “reviewed, nothing compressible” results are a **valid conclusion**, not laziness. Do not delete field tables, curls, or thresholds just to inflate a compression ratio. Incident docs still use the troubleshooting intensity scale—not the same scale as KBs.

**Docs compressed within the last 30 days** (trailing compact stamp < 30 days old) are skipped by default; report as “recently compressed.” Drift protection when re-compressing is still needed (new content from code changes): see the guide.

**Compact stamp:** after each doc is processed, append `<!-- 该文档整理/压缩于 YYYY-MM-DD -->` at the true end of the file—this exact Chinese marker is what `audit.py` matches, so do not translate it. Batch script is in the guide.

## Step 6 — Verify

```bash
# Step 2 baseline: audit.py <project-root> --save-metrics /tmp/dc-metrics.json
# Step 6 verify:
python3 scripts/audit.py <project-root> --compact-date <today YYYY-MM-DD> --compare-metrics /tmp/dc-metrics.json
```

Check I (compact-stamp hard gate) **must report `missing compact stamp=0`** in the summary line before close-out. Any unstamped doc = missed this round—finish stamping and re-run. If the last full compact was < 30 days ago (most docs skipped in Step 5), the script’s “today’s stamp” criterion can false-alarm—the real gate is: every doc either has today’s stamp or a stamp from the last 30 days (i.e. “today’s stamps ∪ last-30-day stamps = full set”; the main agent checks this), and only docs with neither are misses (established 2026-08-28 on mc-mdcrm).
If check J comparison shows AGENTS.md estimated tokens above baseline, explain why in the close-out report (e.g. user explicitly asked to add content this round)—silent growth is not allowed.
The 🔒 managed-block list must be confirmed still present verbatim in the close-out report, one by one.
H’s `domain_map_present` / `backlog_present` must not flip True → False because of this audit.
If the §2.5 liveness follow-up from Step 2 found STALE paths and they were cleaned in Step 5, re-running the liveness command must now report none; anything left means something was missed.

**§0 TOC completeness:** docs using the KB template (`*_KNOWLEDGE_BASE.md`) should have a `§0 目录索引` / TOC section. Missing ones are **filled this round** (mechanically from headings—low risk, do directly); list them in the close-out report; do not defer.

## Step 6.5 — Promote cross-project knowledge

Apply the preset's destination rules while reviewing product docs: shared platform facts and constraints go to declared shared guides; reusable task procedures go to matching skills. Compare existing authorities, update missing knowledge, and retain local product details plus pointers. Do not hardcode another user's paths or install unrelated global policies.

Report promoted items, existing coverage, unresolved factual conflicts and missing destination bindings. A missing shared destination is a reported limitation, not permission to invent one.

## Safety boundaries

- **Do not adjudicate content truth:** when two docs contradict and code evidence cannot decide, do not pick a winner—record in the report and ask the user. This is the only allowed “leave unfixed for the close-out report.” Difference from “fix on discovery”: anomalies verifiable via code/refs get fixed; contradictions that need a human call are escalated to the user
- **Do not touch:** third-party/vendored projects, build artifacts, backup dirs, git worktrees

## Reference files

| File | When to read |
|------|----------------|
| [`references/compression-guide.md`](compression-guide.md) | Before Step 5: compression criteria, per-doc-type intensity table, common traps and fix scripts |
| [`references/standard.md`](standard.md) | When a Step 2 judgment call is unclear: doc-compact’s own audit checklist—eleven standards in full, plus volatile-fact handling. Not the injectable STANDARD (that lives in doc-init’s `insert_doc_governance.py`) |
| [`scripts/audit.py`](../scripts/audit.py) | Step 2 / Step 6 automated audit (includes check J and metrics baseline compare) |
| [`scripts/plan_shards.py`](../scripts/plan_shards.py) | Step 5 shard planning: per-doc token estimate, large-KB detection, budget packing (coefficients and budget constants in script header) |
