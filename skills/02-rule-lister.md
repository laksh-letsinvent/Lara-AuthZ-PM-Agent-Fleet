# Skill: Rule Lister

> Turns an approved PRD into a structured AC corpus. Step 2 of the pipeline.

---

## How to invoke

```
Run Skill rule-lister — for <run-name>
```

Example:
```
Run Skill rule-lister — for 2026-05-joint-account
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## Pre-conditions

- `01-prd.md` is signed off (run card step 1 = `signed-off`)

---

## What rule-lister does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `runs/<run-name>/01-prd.md` — the approved PRD; domain is declared in the run card
- `domains/<domain>/ac-corpus.md` — existing AC for duplication and conflict check
- `domains/<domain>/regulatory-anchors.md` — every anchor cited in AC must exist here
- `domains/<domain>/schema-fragment.zed` — for relation/permission reference; read-only
- `forms/rules-template.md` — the output shape
- `style/voice-profile.md` + `style/anti-ai-pm-writing.md` — writing discipline
- `knowledge-base/zanzibar-spicedb-reference.md` — if the PRD involves caveats, consistency posture, or non-trivial permission derivation

Produce the following:

**OUTPUT — AC file:**

Write `runs/<run-name>/02-ac.md` against `forms/rules-template.md`.

Rules:
- One assertion per AC. "X can do Y and Z" is two ACs
- Every AC must cite a regulatory or business anchor that exists in `regulatory-anchors.md`. If you need one that isn't there, raise an open question — don't invent it
- Cover all required scenario types: positive happy path, negative non-relation, state-blocking (where relevant), caveat-out-of-scope (where relevant), revocation (where relevant). For any type that doesn't apply to this use case, state explicitly why it's N/A
- Check `ac-corpus.md` — flag any AC that duplicates or contradicts an existing one
- No hedge words in statement fields. "Should", "may", "might" are forbidden. Conditional permissions use `expected: conditional`
- Apply voice profile to `statement:` fields

Do not invent. Flag gaps explicitly.

---

## Human gate

Review each AC:
1. Does the anchor exist in `regulatory-anchors.md` and actually support this assertion?
2. Is every coverage type represented or explicitly called out as N/A?
3. Does any AC conflict with an existing one in `ac-corpus.md`?

Flip run card step 2 to `signed-off`. Then say: **"Run Skill scenario-builder — for `<run-name>`"**
