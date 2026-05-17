# Skill: Triage

> The pipeline entry point. PM drops a raw input into `inbox/` and says the word. Triage handles everything else.

---

## How to invoke

```
Run Skill triage — for <filename>
```

Example:
```
Run Skill triage — for 2026-05-10-joint-account-ba-email.md
```

That's the entire command. No file paths, no list of attachments. The skill knows where to look.

---

## PM's job before invoking

1. Receive the stakeholder input (email, Confluence doc, Slack thread, BA brief — any format)
2. Save it to `inbox/` as `YYYY-MM-DD-<topic>.md`
3. Add a short frontmatter block:
   ```yaml
   ---
   received: YYYY-MM-DD
   from: <sender name and role>
   format: <email|doc|brief|slack>
   status: pending-triage
   ---
   ```
4. Say: **"Run Skill triage — for `<filename>`"**

---

## What triage does (agent instructions)

When invoked, read the following automatically — no need for the PM to specify:

- `inbox/<filename>` — the raw input
- `domains/accounts/ac-corpus.md` — existing coverage check (accounts is the anchor domain; load others if the input clearly touches them)
- `runs/_template/00-run-card.md` — run card template
- `knowledge-base/delegation-use-cases.md` — if the input involves delegation, PoA, bereavement, guardianship, or any multi-party access pattern

Produce two outputs:

**OUTPUT 1 — Triage verdict (in chat):**
1. Domain(s) — which domains this touches and why
2. Use case type — new use case / change to existing (name it) / out of scope
3. Complexity — single or multi-domain; whether new schema elements are likely needed
4. Regulatory flags — specific acts/rules (no generic "complies with FCA")
5. Missing information — gaps the Spec Writer would hit; listed as questions for the PM
6. Recommended action — open new run / extend run `<name>` / park (with reason) / escalate

**OUTPUT 2 — Populated run card** (only if action = "open new run"):

Create `runs/YYYY-MM-<short-name>/00-run-card.md` from the template. Populate:
- `run` — the folder path being created
- `title` — clear, specific title for this use case
- `domain` — primary domain from the verdict
- `status` — in-progress
- `opened` — today's date
- `target_close` — 7 days from today
- "What this run is" — one paragraph, plain English, from the agent
- "Stakeholder brief" — verbatim content of the inbox file (minus frontmatter); source attribution above the block
- "Domain and SME" — domain filled; SME left as PM name
- "Pipeline status" — all steps at not-started
- "Decisions log" — one entry: today's date, "Run opened via triage from `<filename>`"
- "Open issues" — every item from the Missing information section above

Do not invent. Flag gaps explicitly.

---

## After triage

- PM reads verdict — confirms domain, scope, open issues are complete
- PM reviews run card — adjusts anything the agent couldn't infer
- PM says: **"Proceed to Step 1"** — then invoke Skill 01

If missing information items exist, resolve them before Step 1. The Spec Writer reads only the run card — incomplete briefs produce incomplete PRDs.

- **Park:** log reason in `log/build-log.md`, move inbox file to `inbox/archived/`
- **Extend existing run:** add to that run's decisions log and open issues; re-run affected steps
