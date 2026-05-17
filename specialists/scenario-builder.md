---
id: SCENARIO-BUILDER
version: v2
status: active
owner: Laksh (PM owns coverage; TL owns Studio loadability)
last_updated: 2026-05-10
tooling: Cowork (primary); Claude Code (when Studio verification is needed)
---

# Scenario Builder — Specialist Contract

**Job:** Turn an approved AC corpus into runnable scenarios that exercise every AC. Now runs at step 3 — before schema handoff — because scenarios define what must work, which in turn informs the TL's schema design.

---

## Purpose

Scenarios come before schema. The Scenario Builder produces the PM's clearest statement of what must be achievable: concrete WRITE/CHECK sequences that make each AC observable and testable. The TL reads these scenarios alongside the schema handoff brief to understand what the schema must enable.

Every AC in the run's `02-ac.md` must be exercised by at least one scenario.

---

## Inputs

1. **The approved AC** — `runs/<YYYY-MM-name>/02-ac.md`. Required. Primary input.
2. **`forms/scenario-template.md`** — output shape. Required.
3. **Current domain schema fragments** — `domains/<domain>/schema-fragment.zed` for awareness of existing relations and permissions. **Read-only.** The Scenario Builder references what already exists; it does not propose schema changes.
4. **`knowledge-base/spicedb-api-reference.md`** — for API surface (CheckPermission, WriteRelationships) and consistency posture. Required.
5. **`style/voice-profile.md`** and **`style/anti-ai-pm-writing.md`** — applied to narrative sections. Required.

> **Note on new relations:** If an AC requires a permission or relation that doesn't exist yet in the schema fragments, the scenario asserts it as required and flags it in the output (e.g. `# SCHEMA-NEEDED: relation trustee on account`). These flags become the primary input to the Schema Handoff. Don't invent schema notation — just flag what's missing.

---

## Output

- **File:** `runs/<YYYY-MM-name>/03-scenarios.md` — against `forms/scenario-template.md`.
- **Status on first emission:** `draft`. Flips to `reviewed` on PM coverage sign-off.

---

## Trust posture

**Auto-suggest.** PM reviews coverage before passing to Schema Handoff. No auto-act.

---

## Quality bar — what good looks like

A pass-grade scenarios file:

- Every approved AC ID appears in at least one scenario's `ac_ids` field.
- Every AC has at least one positive scenario AND one negative scenario where meaningful.
- Caveat-bearing AC have at least one in-scope and one out-of-scope scenario.
- Revocation-relevant AC have a revocation scenario with consistency posture stated.
- Setup state declared once at the top. Per-scenario blocks reference it.
- SCHEMA-NEEDED flags are explicit and specific — not vague ("need something for scope") but precise ("need a scope-bound caveat on the `trustee` relation on `account`").
- Narrative per scenario is plain English, one paragraph, voice-disciplined.

A fail-grade scenarios file:

- AC IDs missing from coverage.
- Missing negatives where AC implies a deny case.
- Scenario references permissions or relations without flagging when they don't exist yet.
- SCHEMA-NEEDED flags are absent when new relations are clearly implied by the AC.
- Scenarios that can't be understood without reading the schema — they should be readable by a TL who hasn't seen the AC.

---

## Human gate

PM reads the coverage matrix and verifies every approved AC is represented. Checks that SCHEMA-NEEDED flags are complete and accurate — these go directly to the TL in the next step. Flips status to `reviewed`.

---

## Invocation pattern

> "Scenario Builder: approved AC in `runs/<run>/02-ac.md`. Current schema in `domains/accounts/schema-fragment.zed`. Produce `03-scenarios.md`. Flag any relations or permissions that don't yet exist as SCHEMA-NEEDED. Reuse existing personas where the AC overlaps existing use cases."

---

## Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04-29 | Initial — ran at step 4, after schema sketch. |
| v2 | 2026-05-10 | Moved to step 3. Removed schema sketch dependency. Added SCHEMA-NEEDED flag convention. Schema handoff now feeds from scenarios, not the other way round. |
