# doc-compact judgment baseline: document management model (full explanation)

Long-form expansion of doc-compact’s judgment baseline. Read on demand when an audit or compression call in `SKILL.md` is unclear.

**Role:** This is **doc-compact’s own compact audit checklist**—an operational supplement to the installed documentation lifecycle contract. **It is not the injectable STANDARD** and must not be treated as “content to paste into global files.”

**Injectable authority:** the only source of text that should be installed into / compared against global AI instruction files is doc-init’s `<DOC_INIT_DIR>/scripts/insert_doc_governance.py`. Keep this checklist compatible with that script’s STANDARD; if this file contains a rule that ought to apply globally and the script’s STANDARD lacks it, update the preset and version under an authorized skill-maintenance task—do not write global files from doc-compact yourself.

**Mental model:** document structure is two-dimensional—**three vertical layers** (rules layer `AGENTS.md` always resident → index layer `<DOMAIN>_INDEX.md` on demand by task → content layer concrete docs on demand) + **horizontal types** (open set; five common types as defaults; new types may be added and registered). Audits must not fail a type merely because it is outside the common five—only check “registered in the doc-type table + placed on the correct path.”

## Eleven standards

1. **Single primary entry:** every project’s full doc navigation lives in the root `AGENTS.md` “文档导航” / Document navigation section; bare `OVERVIEW.md` / `INDEX.md` must not compete as scattered indexes; legal secondary indexes must be named `<DOMAIN>_INDEX.md` and reachable only via root `AGENTS.md` (two-level-index special case: SKILL.md Step 3).
2. **At most two hops:** core docs one hop from root; secondary docs two hops via task-domain `<DOMAIN>_INDEX.md` (`AGENTS.md → <DOMAIN>_INDEX.md → doc`); no nesting beyond two levels (special case: SKILL.md Step 3).
3. **List only real docs:** navigation lists only documents that exist—one line each with a one-sentence purpose; no empty placeholders, no “none yet,” no “formerly called X” historical/meta notes.
4. **Describe “when to read”:** purpose answers “with what question / when changing which code should I read this”—models route on that sentence.
5. **Inline pointers primary, bottom table fallback:** place doc pointers next to the rule/invariant they support; the bottom “文档导航” / Document navigation table is the complete fallback set.
6. **CLAUDE.md content is only one `@*.md` line:** carries no content; only pulls in sibling AGENTS.md; modules without independent conventions do not get their own AGENTS.md/CLAUDE.md.
7. **Placement and naming:** each type has a fixed directory (`docs/`, `docs/design/`, `docs/troubleshooting/YYYY-MM-DD-*`, etc.); `.md` files do not live in source trees (`AGENTS.md` is an exception but must be excluded from builds). **The documentation lifecycle preset owns placement categories; the project registers its concrete doc types**; this skill only checks “is it in place.”
8. **Add/remove/move a doc → sync indexes:** any add, delete, or relocate syncs root `AGENTS.md` navigation and whole-repo relative links.
9. **Secondary-index review:** navigation share, >500 root lines and ≥3 related records are signals to inspect readability, not mandatory folding thresholds. Keep direct links unless a group makes navigation hard to scan. If folded, keep root → named index → doc within two hops.
10. **Normative and compact** (see SKILL.md Steps 4 / 5): naming / link format / language follow the rules; navigation is ordered by domain clusters; body text drops redundancy that does not change reader behavior and keeps content that changes action / judgment.
11. **Volatile facts are not restated across docs (single source):** concrete numbers / states that change with external conditions (API credit tiers, rate limits, balances, version numbers, key expiry, etc.) are maintained in exactly one “authoritative source” doc; other docs split into two treatments:
    - **Authority-adjacent docs** (e.g. source profile, policy doc): may link to the authority; do not restate the number.
    - **Other docs** (research notes, specs, evals): write only **conclusions that do not change when the fact changes** (e.g. “realtime requires a separate enablement,” “this API is a generic credit-gated class”); no concrete numbers, and no forced links.
    - **Anti-pattern:** rewriting every doc that had the number into “→ link to the authority”—that over-couples everything into satellite docs of the authority and gets harder to maintain the more you do it. Correct fix: authority maintains the fact; other docs write stable principles.

If the target environment already expresses equivalent rules in other wording, treat it as compliant—do not rewrite for style alone.
