# Skill: Schema Sketch (Optional)

> Produces a first-draft schema proposal in SpiceDB notation. Optional step 5 — invoke only when you want to give the TL a starting point rather than a blank page. Runs after Scenario Builder (step 3) and before Schema Handoff (step 4).

---

## How to invoke

```
Run Skill schema-sketch — for <run-name>
```

Example:
```
Run Skill schema-sketch — for 2026-05-joint-account
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## When to invoke

Use this when:
- The use case introduces new actor types or new permission patterns not already in the schema
- You want to propose a schema shape and invite TL critique, rather than just asking questions
- The TL has limited bandwidth and a first draft reduces their design effort significantly

Skip this when:
- The AC shows no schema changes are needed (all required relations/permissions already exist)
- You want the TL to design from scratch — go straight to Skill 04 (Schema Handoff)
- You want to hand over requirements cleanly without constraining the TL's design choices

**Default flow:** 00 → 01 → 02 → 03 → 04 (skip this skill)  
**With schema sketch:** 00 → 01 → 02 → 03 → **05** → 04

---

## Pre-conditions

- `03-scenarios.md` is signed off (run card step 3 = `signed-off`)
- At least one `SCHEMA-NEEDED` flag exists in `03-scenarios.md` (if there are none, this skill is unnecessary)

---

## What schema-sketch does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `runs/<run-name>/02-ac.md` — approved AC; domain is declared in the run card
- `runs/<run-name>/03-scenarios.md` — approved scenarios with SCHEMA-NEEDED flags
- `domains/<domain>/schema-fragment.zed` — current schema; proposals are additive to this
- `knowledge-base/schema-design-patterns.md` — pattern library; every proposed element must cite at least one pattern
- `knowledge-base/zanzibar-spicedb-reference.md` — for caveat syntax, consistency posture, and traversal rules
- `forms/schema-sketch-template.md` — the output shape
- `style/voice-profile.md` + `style/anti-ai-pm-writing.md` — writing discipline for prose sections

Produce the following:

**OUTPUT — Schema sketch file:**

Write `runs/<run-name>/05-schema-sketch.md` against `forms/schema-sketch-template.md`.

Rules:
- Read every SCHEMA-NEEDED flag in `03-scenarios.md` — these are the gaps to address
- Only propose what the SCHEMA-NEEDED flags and AC require. No speculative additions
- Every proposed relation or permission must cite at least one pattern from `knowledge-base/schema-design-patterns.md`
- Proposals are additive — no deletions or renames of existing elements without explicit justification; backward-compat assessment is required
- Flag anything uncertain in the Open Questions section. Uncertainty expressed clearly is more useful than a confident wrong answer
- Include `.zed` comments that explain WHY, not just what. The TL is the primary reader
- Title every proposed block with a comment: `// PROPOSED — pending TL review`
- Apply voice profile to all prose sections

Do not invent. Flag gaps explicitly.

---

## Human gate

Before passing to TL:
1. Does every proposed element trace back to a specific SCHEMA-NEEDED flag or AC? Remove anything that doesn't
2. Are open questions genuine — things you couldn't resolve, not rhetorical?
3. Did the sketch cite at least one pattern per proposed element?
4. Is the backward-compat assessment present and honest?

Flip run card step 5 to `signed-off`. Then say: **"Run Skill schema-handoff — for `<run-name>`"**

In the schema-handoff brief, the skill will automatically reference this sketch in section 2 and flag it as a proposed starting point — the TL is free to depart from it.
