---
run: runs/<YYYY-MM-short-name>
title: <Use Case Title>
domain: <accounts|payments|cards|communications|customer-mgmt>
status: <in-progress|awaiting-sign-off|merged|parked|abandoned>
opened: <YYYY-MM-DD>
target_close: <YYYY-MM-DD>
closed: <YYYY-MM-DD or empty>
---

# Run Card — <Use Case Title>

> One-page record of the run. Status, signatories, key dates. Read this first when picking up a run.

## What this run is

One paragraph. The use case being defined, why now, and what the run will produce when complete.

## Stakeholder brief (input)

> The verbatim input the Spec Writer reads. Consolidate before pasting — drop salutations, scheduling chatter, anything not about the use case. If the brief exceeds a page, move it to `runs/<run>/_input/` and link from here.

```
<paste brief here — email body, bullet list, problem statement, or similar. Source attribution above the block.>
```

## Domain and SME

| Domain | SME | Sign-off status |
|---|---|---|
| <domain> | <name> | <pending / signed-off / blocked> |

## Pipeline status

| Step | Specialist | Output | Status |
|---|---|---|---|
| 1 | Spec Writer | `01-prd.md` | <not-started / in-progress / signed-off> |
| 2 | Rule Lister | `02-ac.md` | <...> |
| 3 | Scenario Builder | `03-scenarios.md` | <...> |
| 4 | Schema Handoff | `04-schema-handoff.md` | <...> |

## Decisions log

Append-only. Every meaningful call during this run, dated.

- **<YYYY-MM-DD>** — <Decision, alternatives considered, who signed off.>

## Open issues

- <Issue, owner, why it's open.>

## Merge log

Filled in only when status flips to `merged`.

- **<YYYY-MM-DD>** — Merged into `domains/<domain>/`. AC IDs assigned: AC-X-NNN through AC-X-NNN.
