---
id: MATRIX-SYNC
version: v1
status: drafted
owner: Laksh (v1, solo)
last_updated: 2026-05-13
tooling: Cowork
---

# Matrix Sync — Specialist Contract

**Job:** Read every approved AC across all domain corpora and regenerate the cross-domain permission matrix as a single, traceable, version-controlled artefact. Not a per-run output — a standing view of the whole system's permissions at a given point in time.

---

## Purpose

Every other specialist produces run-scoped output: a PRD, a set of ACs, a set of scenarios. Matrix Sync is the only step that synthesises across all runs, all domains, and all subject types. Its output — `schema/permission-matrix.md` — is the answer to the question any stakeholder will eventually ask: "Which subjects can do what, across the whole platform?"

The matrix is a view, not a source. The source is `ac-corpus.md`. If the matrix and the corpus disagree, the corpus wins.

The Matrix Sync specialist is the *lowest-judgment* specialist in the fleet — it doesn't interpret, it translates. No inference. No interpolation. A cell is `—` until an AC says otherwise.

---

## Inputs

1. **All `domains/*/ac-corpus.md` files.** Required. Only `status: approved` ACs are used. Proposed and deprecated ACs are invisible to this step.
2. **All `domains/*/schema-fragment.zed` files.** Required. Used to verify that every `action.permission` named in an approved AC exists in the schema. Mismatches are flagged with `⚠️`, not silently dropped.
3. **`schema/permission-matrix.md`** (previous version, if it exists). Read before overwriting. The diff between old and new is the QA signal — regressions surface here.
4. **`forms/matrix-template.md`.** Required. Output shape, cell conventions, column set, header block fields.

---

## Output

- **File:** `schema/permission-matrix.md`
- **Form:** `forms/matrix-template.md`
- **Format:** Markdown table, one table per domain section, open issues section at the end.
- **Trigger:** Post-run-close (step 4 of housekeeping). Also: standalone on demand.

---

## Trust posture

**Auto-suggest.** Matrix Sync produces a draft for PM review, not a live update. The PM reviews the diff before committing. The specialist never self-approves.

The matrix contains no design decisions — only what the ACs say. If a cell should exist but no AC covers it, it stays `—`. The gap is the signal; the Matrix Sync specialist surfaces it, it does not fill it.

---

## Quality bar — what good looks like

A pass-grade matrix:

- Every non-`—` cell cites exactly one AC in an HTML comment (`<!-- AC-A-001 -->`).
- Cell values match the `expected` field of the cited AC exactly: `allow` → `✓`, `deny` → `✗`, `conditional` → `~`.
- No cell is `✓` or `✗` without a cited AC. No inference.
- `~` cells have a plain-English caveat condition in the Notes column (one clause, not YAML).
- `⚠️` cells are logged in the open issues section with the permission name that failed the schema cross-check.
- `?` cells are logged with the conflicting AC IDs.
- Domain sections appear in the correct order (Accounts, Payments, Cards, Communications, Customer Management).
- Header block is current: `last_synced`, `approved_ac_count`, and `source_runs` all updated.
- Open issues section is present even if empty ("No open issues.").

A fail-grade matrix:

- Cells without AC citations.
- `—` cells replaced with inferred values ("it's probably allow because the owner can do everything").
- Proposed or deprecated ACs contributing cells.
- Missing `⚠️` flag when a permission name doesn't exist in the schema fragment.
- Domain sections out of order, or a new subject column added without a corresponding entry in the subject key.
- `last_synced` not updated.

---

## Human gate

PM reviews by diffing the new matrix against the previous version:

1. **Regression check.** Any cell that was `✓` and is now `—` or `✗` is a potential regression. Investigate the corpus change that caused it before accepting.
2. **Conflict check.** Any `?` cell is a data quality problem. Two approved ACs contradict each other — one of them is wrong. Resolve at the corpus level, then re-run.
3. **Schema gap check.** Any `⚠️` cell means either the schema fragment is stale or the AC used a wrong permission name. Check both. This is a signal that schema and AC have drifted.
4. **Coverage read.** Scan the `—` cells for meaningful gaps — subject×action pairs that should exist but don't. These are candidates for the next run's scope.

Matrix Sync has no run-card flip. Once the PM is satisfied, the matrix is committed alongside the corpus update.

---

## Known limitations

- The matrix flattens caveats to `~`. The actual caveat logic lives in the AC. Readers who need the full condition must go to the corpus. This is a deliberate trade-off — the matrix is for overview, not deep evaluation.
- The matrix cannot represent permission derivation chains (e.g. "owner can do X because owner has relation Y which has permission Z"). It shows the end-state check result, not the traversal path. Full derivation lives in the schema.
- Cross-domain ACs: the matrix places the row in the domain that owns the resource (the primary domain). The cross-domain aspect is noted in the AC corpus but not explicitly shown in the matrix.
- As the corpus grows, the matrix will grow too. When it exceeds ~80 rows, consider splitting by domain into separate files. Until then, one file is more useful than five.

---

## Invocation pattern

```
Run Skill matrix-sync
```

No arguments. The skill reads everything it needs from the corpus and fragment files.

---

## Evaluation rubric

Test against the accounts corpus after the first run closes:

1. Every AC-A-xxx entry with `status: approved` appears in at least one cell.
2. No cell exists for a subject×action pair with no approved AC.
3. The open issues section correctly lists any `?` or `⚠️` cells.
4. `last_synced` is today. `approved_ac_count` matches the count of approved ACs in the corpus.

---

## Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-05-13 | Initial draft. |
