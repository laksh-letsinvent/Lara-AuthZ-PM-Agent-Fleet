---
id: SCHEMA-HANDOFF
version: v1
status: active
owner: Laksh (PM authors; TL receives)
last_updated: 2026-05-10
tooling: Cowork (prose-shaped output)
supersedes: schema-sketcher.md (v1 — retired; schema design is TL territory)
---

# Schema Handoff — Specialist Contract

**Job:** Turn approved scenarios and AC into a clean PM-to-TL brief. Not a schema design. The brief tells the TL what must be achievable and asks the right questions so they can design the schema without reinterpreting intent.

---

## Purpose

Schema design is a technical decision. The PM's job ends at "here is what must be true and why." The TL's job is to figure out how to model it in SpiceDB. Producing half-formed schema sketches blurs that boundary and creates review confusion about whether the PM is making design decisions they shouldn't own.

This specialist produces the handoff artefact — everything the TL needs, nothing that presupposes their design choices.

---

## Inputs

1. **Approved scenarios** — `runs/<YYYY-MM-name>/03-scenarios.md`. Required. The scenarios are the primary surface of what must work.
2. **Approved AC** — `runs/<YYYY-MM-name>/02-ac.md`. Required. The AC are the contract.
3. **`forms/schema-handoff-template.md`** — output shape. Required.
4. **Affected domain `regulatory-anchors.md`** — for formulating accurate constraints (section 4 of the brief). Required.
5. **Affected domain `schema-fragment.zed`** — for awareness of what already exists; used only to identify backward-compat requirements and existing relations the brief should reference. **Read-only. Do not propose schema changes.**
6. **`style/voice-profile.md`** and **`style/anti-ai-pm-writing.md`** — applied to all prose sections. Required.

---

## Output

- **File:** `runs/<YYYY-MM-name>/04-schema-handoff.md`
- **Form:** `forms/schema-handoff-template.md`
- **Status on first emission:** `draft`. PM reviews, flips to `ready-for-tl`. TL acknowledges receipt and flips to `tl-acknowledged`. Schema design completion is tracked separately (schema PR or fragment update).

---

## Trust posture

**Auto-suggest.** The PM reviews the brief before it goes to the TL. The brief does not auto-send.

---

## Quality bar — what good looks like

A pass-grade handoff brief:

- States what must work in plain English that a non-technical stakeholder could read. No schema notation in sections 1 and 2.
- Lists every AC ID covered. The TL can cross-reference without hunting.
- Has at least two genuine open questions for the TL (section 6). If there are no open questions, the PM is probably speculating about schema design in sections 4–5 instead of asking.
- Constraints (section 4) are factual and sourced. "Trust deed scope is required" is a constraint. "We probably need a new caveat" is not a constraint — it's a schema design suggestion and belongs in the open questions.
- Out of scope (section 5) is explicit. Ambiguity about scope is expensive for the TL.
- No `.zed` syntax anywhere in the brief.
- Passes the anti-AI filter on all prose sections.

A fail-grade handoff brief:

- Contains proposed schema additions (relations, permissions, caveat definitions). That's the retired Schema Sketcher pattern.
- Has empty open questions (signals the PM either hasn't thought hard enough, or has answered questions that belong to the TL).
- States regulatory anchors without explaining their constraint implication (e.g. "Mental Capacity Act 2005" with no note on what it means for this use case).
- Is longer than two pages — scope likely needs splitting.

---

## Human gate

PM reviews the brief and flips status to `ready-for-tl`. The TL is then the receiver, not a reviewer of PM work. The PM's obligation ends at `ready-for-tl`. Schema design accountability transfers to the TL on `tl-acknowledged`.
