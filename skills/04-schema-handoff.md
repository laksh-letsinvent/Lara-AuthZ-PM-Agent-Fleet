# Skill: Schema Handoff

> Produces the PM's brief to the Tech Lead. Step 4 — the final pipeline output. Not a schema design; that's the TL's job.

---

## How to invoke

```
Run Skill schema-handoff — for <run-name>
```

Example:
```
Run Skill schema-handoff — for 2026-05-joint-account
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## Pre-conditions

- `03-scenarios.md` is signed off (run card step 3 = `signed-off`)
- If Skill 05 (schema-sketch) was run, `05-schema-sketch.md` exists and is signed off

---

## What schema-handoff does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `runs/<run-name>/02-ac.md` — approved AC; domain is declared in the run card
- `runs/<run-name>/03-scenarios.md` — approved scenarios, including any SCHEMA-NEEDED flags
- `runs/<run-name>/05-schema-sketch.md` — if it exists, reference it in the brief as a proposed starting point for TL review
- `domains/<domain>/regulatory-anchors.md` — for constraint sourcing
- `domains/<domain>/schema-fragment.zed` — to identify backward-compatibility requirements
- `forms/schema-handoff-template.md` — the output shape
- `style/voice-profile.md` + `style/anti-ai-pm-writing.md` — writing discipline

Produce the following:

**OUTPUT — Schema handoff brief:**

Write `runs/<run-name>/04-schema-handoff.md` against `forms/schema-handoff-template.md`.

Rules:
- No `.zed` syntax anywhere. You are describing requirements, not designing schema
- Section 2 (What must be achievable): summarise the key capability assertions from the scenarios in plain English; pull SCHEMA-NEEDED flags from `03-scenarios.md` and use them to inform what you flag as constraints and open questions
- Section 4 (Known constraints): factual only; each constraint must be traceable to a regulatory anchor or an existing AC
- Section 5 (Out of scope): be explicit — ambiguity here is expensive for the TL
- Section 6 (Open questions): minimum 2 genuine questions for the TL; things that require schema expertise to answer, not rhetorical
- If a schema sketch exists, reference it in section 2: note it is a proposed starting point, not a finished design — the TL is free to depart from it
- Apply voice profile to all prose sections
- Length: 1–2 pages maximum

Do not invent. Flag gaps explicitly.

---

## Human gate

Review before sending to TL:
- Does section 2 accurately reflect what the scenarios assert?
- Are all SCHEMA-NEEDED flags from the scenarios represented (as constraints or open questions)?
- Is any `.zed` syntax present? If so, remove it
- Are the open questions actually for the TL, not already answered by the PM?

Flip status to `ready-for-tl`. Send to the TL. **Your run is complete.**

## After the TL receives it

The TL's schema work is tracked outside the run folder (schema PR, fragment update). When schema is complete, flip `04-schema-handoff.md` status to `schema-complete` and merge the AC into `domains/<domain>/ac-corpus.md`.
