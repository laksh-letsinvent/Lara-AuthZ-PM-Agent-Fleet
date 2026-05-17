# Skill: Spec Writer

> Turns the stakeholder brief in the run card into a structured PRD. Step 1 of the pipeline.

---

## How to invoke

```
Run Skill spec-writer — for <run-name>
```

Example:
```
Run Skill spec-writer — for 2026-05-joint-account
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## Pre-conditions

- Triage is complete and the run folder exists at `runs/<run-name>/`
- `00-run-card.md` is populated — brief is pasted in, domain is declared
- PM has confirmed the verdict and resolved any missing-information items

---

## What spec-writer does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `runs/<run-name>/00-run-card.md` — the run card; read the brief from the Stakeholder brief section
- `domains/<domain>/ac-corpus.md` — existing coverage check; domain is declared in the run card
- `domains/<domain>/regulatory-anchors.md` — anchor citation; every anchor cited in the PRD must exist here
- `forms/prd-template.md` — the output shape
- `style/voice-profile.md` + `style/anti-ai-pm-writing.md` — writing discipline
- `knowledge-base/delegation-use-cases.md` — if the brief involves delegation, PoA, bereavement, or multi-party access
- `knowledge-base/banking-domain-context.md` — if the brief touches multiple consuming domains

Produce the following:

**OUTPUT — PRD file:**

Write `runs/<run-name>/01-prd.md` against `forms/prd-template.md`.

Rules:
- Read the brief from the run card file, not from chat
- Check `ac-corpus.md` — if this use case or something close is already modelled, say so explicitly in the Out of scope section and narrow the PRD scope accordingly
- Every regulatory anchor you cite must exist in `regulatory-anchors.md`. If you need one that isn't there, flag it as an open question — don't invent it
- No invented magnitude figures. If you can't quantify, say so plainly
- Apply voice profile and anti-AI filter. No "delve into", "robust", "leverage", "in today's evolving landscape", or any of the listed anti-patterns
- Out of scope section must have at least 3 items. Open questions must have at least 3

Do not invent. Flag gaps explicitly.

---

## Human gate

Read the PRD. Check:
- Problem statement is specific, not generic
- Out of scope is substantive
- Open questions are genuine gaps, not rhetorical
- No invented numbers
- No anchors cited that don't exist in `regulatory-anchors.md`

Flip status in the run card step 1 to `signed-off`. Then say: **"Run Skill rule-lister — for `<run-name>`"**
