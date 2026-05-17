# Skill: Matrix Sync

> Regenerates the cross-domain permission matrix from the current state of all ac-corpus files. Step 6 — runs at the close of every run, after AC is merged into the corpus.

---

## How to invoke

```
Run Skill matrix-sync
```

No run name needed. This skill reads across all domains, not a single run. It is idempotent — safe to run at any time; the output is always a full regeneration from the current corpus state.

---

## When to invoke

**Standard trigger:** after every run close, as step 4 of the post-run housekeeping:

1. Append approved AC into `domains/<domain>/ac-corpus.md`
2. Flip use case status to `Approved`
3. Update `00-run-card.md` status to `merged`
4. **Run Skill matrix-sync** ← this step

**Also valid standalone** — invoke at any time to verify the matrix reflects current corpus state (e.g. after a manual corpus correction, after onboarding a new domain, or before a stakeholder review).

---

## Pre-conditions

- At least one `domains/<domain>/ac-corpus.md` contains at least one `status: approved` AC.

---

## What matrix-sync does (agent instructions)

When invoked, read the following automatically:

- All `domains/*/ac-corpus.md` files — the source of truth for every cell in the matrix; only `status: approved` ACs are used
- All `domains/*/schema-fragment.zed` files — cross-check that every `action.permission` named in an approved AC exists in the corresponding schema fragment; flag mismatches
- `schema/permission-matrix.md` — if it already exists, read it first; the diff between old and new is the QA signal for regression detection
- `forms/matrix-template.md` — the output shape, cell conventions, and open issues format

Produce the following:

**OUTPUT — Permission matrix:**

Write `schema/permission-matrix.md` against `forms/matrix-template.md`.

Rules:

**Sources:**
- Use only `status: approved` ACs. Proposed and deprecated ACs are invisible to this skill.
- Every cell value must be traceable to a specific AC ID. Add an HTML comment after the cell value: `<!-- AC-A-001 -->`. If multiple ACs support the same cell, cite the most specific one.

**Rows:**
- One row per domain-action pair, using the `action.permission` field from the AC.
- Group rows by domain in this order: Accounts → Payments → Cards → Communications → Customer Management.
- Within a domain, group by use case (matching the corpus section headings), then list actions in the order they appear in the corpus.
- If an action appears in ACs for multiple subject types within the same domain, it is one row — not one row per AC.

**Columns:**
- Standard subject type columns: `owner`, `joint_holder`, `view_delegate`, `poa_attorney`, `ops_internal`.
- Add a column only if the corpus introduces a subject relation not in the standard set (e.g. `appointee`, `trustee`, `guardian`). Document new columns in the subject key.
- Never remove a column once added — mark cells as `—` for domains where that subject type has no ACs.

**Cell values:**
- `✓` — an approved AC asserts `expected: allow` for this subject×action pair, with no contradicting deny.
- `✗` — an approved AC asserts `expected: deny`.
- `~` — an approved AC asserts `expected: conditional` (caveat-gated). Pull the caveat condition into the Notes column.
- `—` — no approved AC exists for this pair. Do not infer; leave it blank.
- `?` — two or more approved ACs contradict each other for this pair (one allow, one deny). Flag in open issues.

**Schema cross-check:**
- If a permission name in an AC does not appear in the corresponding `schema-fragment.zed`, append `⚠️` to the cell value and log it in the open issues section.

**Notes column:**
- For `~` cells: state the caveat condition in plain English (one clause, no YAML).
- For `⚠️` cells: note "permission not in schema fragment — check TL".
- For `?` cells: note the conflicting AC IDs.
- Otherwise: copy the `notes:` field from the AC if it adds meaningful context for the reader; omit if it duplicates what the cell already says.

**Open issues section:**
- List every `?` cell with the conflicting AC IDs and a one-line description of the conflict.
- List every `⚠️` cell with the AC ID and the permission name that could not be found in the fragment.
- List meaningful coverage gaps: subject types that appear prominently in the corpus but have no AC for a given action (i.e. the gap is a design decision waiting to be made, not just out-of-scope). Do not list every `—` cell — only the ones where the absence is notable.

**Header block:**
- Update `last_synced` to today's date.
- Update `approved_ac_count` to the total count of approved ACs across all domains.
- Update `source_runs` to list all runs that contributed at least one approved AC currently in the corpus.

Do not invent permissions. Do not infer cell values. Every non-`—` cell must have a cited AC.

---

## Human gate

Review the diff against the previous matrix:

- Any previously `✓` cell now showing `—` or `✗`? A run may have introduced a regression or the corpus may have been edited incorrectly — investigate before accepting.
- Any new `?` cells? Conflicting ACs require resolution before the matrix is clean. Add a decision to the relevant domain's open issues or escalate to the next run.
- Any `⚠️` cells? The schema fragment may be stale, or the AC used an incorrect permission name. One of the two is wrong — check both before deciding.
- Does the domain/action grouping still make sense as coverage grows? Reorder within a domain if the use case grouping has shifted.

No run-card flip needed — matrix sync has no corresponding pipeline step number. Once you're satisfied, the matrix is live. Commit it alongside the ac-corpus update in the same git change.
