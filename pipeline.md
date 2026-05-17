# Pipeline — AuthZ Agent Fleet

> The end-to-end chain. How a requirement becomes a TL-ready schema brief. Five steps, four human gates, no auto-act. One post-close step that keeps the platform-wide permission view current.

---

## The chain

**Default path** (most runs):

```
Raw input (email / doc / Confluence / Slack)
        │
        ▼
[Skill 00 — Triage]           → domain, flags, gaps, action
        │  human gate
        ▼
[Skill 01 — Spec Writer]      → PRD                     (01-prd.md)
        │  human gate
        ▼
[Skill 02 — Rule Lister]      → Acceptance criteria     (02-ac.md)
        │  human gate
        ▼
[Skill 03 — Scenario Builder] → Scenarios + SCHEMA-NEEDED flags  (03-scenarios.md)
        │  human gate
        ▼
[Skill 04 — Schema Handoff]   → TL brief                (04-schema-handoff.md)
        │
        ▼
Tech Lead designs schema → schema-fragment.zed updated → run merged
        │
        ▼
[Skill 06 — Matrix Sync]      → Permission matrix updated  (schema/permission-matrix.md)
```

**With optional schema sketch** (when you want to give TL a starting point):

```
... [Steps 00–03 same as above] ...
        │  (scenarios signed off, SCHEMA-NEEDED flags confirmed)
        ▼
[Skill 05 — Schema Sketch]    → Draft .zed proposals    (05-schema-sketch.md)  ← OPTIONAL
        │  human gate
        ▼
[Skill 04 — Schema Handoff]   → TL brief (references sketch as proposed starting point)
        │
        ▼
Tech Lead reviews sketch + brief → validates/modifies schema → updates fragment
        │
        ▼
[Skill 06 — Matrix Sync]      → Permission matrix updated  (schema/permission-matrix.md)
```

Use Skill 05 when: the use case introduces new schema elements and you want to reduce TL design effort with a first draft. Skip it when: no schema changes are needed, or you want the TL to design from a blank page.

---

## How to start a run

1. Receive the stakeholder input (email, doc, Confluence page, Slack thread — any format)
2. Save it to `inbox/YYYY-MM-DD-<topic>.md` with a short frontmatter block (received date, sender, format)
3. Invoke Skill 00 (Triage) — point it at the inbox file
4. Triage produces: (a) a verdict in chat, and (b) a populated run card at `runs/YYYY-MM-<name>/00-run-card.md`
5. PM reviews the run card, resolves any open issues flagged, confirms proceed
6. Work through Skills 01–04 in order, one per session

The PM never touches the run card template manually. Triage creates it. Each subsequent step has a human gate — the agent drafts, you sign off before the next step runs.

---

## What each skill needs (at a glance)

| Step | Skill | Key inputs | Output | Required? |
|---|---|---|---|---|
| 0 | Triage | Raw input + ac-corpus | Verdict + action | Always |
| 1 | Spec Writer | Run card (brief) + domain slice | `01-prd.md` | Always |
| 2 | Rule Lister | PRD + ac-corpus + anchors | `02-ac.md` | Always |
| 3 | Scenario Builder | AC + schema fragment (read-only) | `03-scenarios.md` | Always |
| 5 | Schema Sketch | Scenarios + AC + schema fragment | `05-schema-sketch.md` | Optional |
| 4 | Schema Handoff | Scenarios + AC + sketch (if done) | `04-schema-handoff.md` | Always |
| 6 | Matrix Sync | All ac-corpus files + schema fragments | `schema/permission-matrix.md` | Post-close |

Full invocation detail (what to attach, what to say) is in `skills/0N-<name>.md`.

---

## After the run closes

When the TL confirms schema work is complete:
1. Append approved AC from `02-ac.md` into `domains/<domain>/ac-corpus.md`
2. Flip the use case status in the corpus registry to `Approved`
3. Update `00-run-card.md` status to `merged`, fill in the merge log
4. **Run Skill matrix-sync** — regenerates `schema/permission-matrix.md` from the updated corpus; review the diff before committing
5. The run folder stays as historical record — never delete it

Skill 06 (Matrix Sync) is idempotent — it can also be run standalone at any time to verify the matrix reflects current corpus state (e.g. before a stakeholder review, after a manual corpus correction).

---

## Porting this framework

Everything the framework needs is in this folder. To run it in a new organisation or domain:

1. Replace `knowledge-base/` content with your platform's reference docs (or keep Zanzibar/SpiceDB if it applies)
2. Replace `domains/` with your domain structure — one folder per bounded context
3. Replace `style/` with your voice profile and writing standards
4. Keep `forms/`, `specialists/`, `skills/`, `pipeline.md`, and `runs/` unchanged — they're domain-agnostic

The only thing that changes between organisations is the knowledge substrate. The pipeline logic is stable.
