# Skill: Scenario Builder

> Turns approved AC into concrete runnable scenarios. Step 3. Comes before schema — scenarios define what must work, which is what the TL needs to design the schema.

---

## How to invoke

```
Run Skill scenario-builder — for <run-name>
```

Example:
```
Run Skill scenario-builder — for 2026-05-joint-account
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## Pre-conditions

- `02-ac.md` is signed off (run card step 2 = `signed-off`)

---

## What scenario-builder does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `runs/<run-name>/02-ac.md` — the approved AC; domain is declared in the run card
- `domains/<domain>/schema-fragment.zed` — existing relations/permissions for reference; read-only; gaps become SCHEMA-NEEDED flags
- `forms/scenario-template.md` — the output shape
- `knowledge-base/spicedb-api-reference.md` — for WRITE/CHECK/DELETE syntax and consistency posture
- `style/voice-profile.md` + `style/anti-ai-pm-writing.md` — writing discipline

Produce the following:

**OUTPUT — Scenarios file:**

Write `runs/<run-name>/03-scenarios.md` against `forms/scenario-template.md`.

Rules:
- Every approved AC ID must appear in at least one scenario's `ac_ids` field
- Every AC needs at least one positive scenario (allow) and one negative (deny) where the negation is meaningful
- Caveat-bearing AC need at least one in-scope and one out-of-scope scenario
- Revocation-relevant AC need a revocation scenario with consistency posture explicit (e.g. `CHECK with at_least_as_fresh(deleteZedToken)`)
- If a scenario requires a relation or permission that doesn't exist in the current `schema-fragment.zed`, flag it with a `# SCHEMA-NEEDED:` comment explaining exactly what's missing in plain English — do not invent schema notation
- Declare setup state once at the top of the file; per-scenario blocks reference it
- Narrative per scenario: one paragraph, plain English, voice-disciplined

Do not invent schema. Flag gaps explicitly with SCHEMA-NEEDED comments.

---

## Human gate

Review the coverage matrix (frontmatter `ac_ids_covered` vs. the AC list in `02-ac.md`):
- Every AC ID covered?
- Scenario type mix appropriate?
- SCHEMA-NEEDED flags complete and specific? (These feed the TL in step 4.)

Flip run card step 3 to `signed-off`. Then say: **"Run Skill schema-handoff — for `<run-name>`"**

If new schema elements are needed and you want to give the TL a draft starting point, say: **"Run Skill schema-sketch — for `<run-name>`"** first (optional step 5), then proceed to schema-handoff.
