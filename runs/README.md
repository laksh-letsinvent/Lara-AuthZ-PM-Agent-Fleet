# Runs

One folder per requirement or use case. Created by Triage (Skill 00) — the PM does not create these manually.

## Folder shape

```
runs/YYYY-MM-<short-name>/
├── 00-run-card.md           ← created by Triage; PM reviews and confirms
├── 01-prd.md                ← Spec Writer output
├── 02-ac.md                 ← Rule Lister output (structured AC)
├── 03-scenarios.md          ← Scenario Builder output (scenarios + SCHEMA-NEEDED flags)
├── 05-schema-sketch.md      ← Schema Sketch output (optional — draft .zed for TL)
└── 04-schema-handoff.md     ← Schema Handoff output (TL brief; always last)
```

Files are numbered by invocation order. Step 05 is optional and runs between 03 and 04 when used.

## How a run starts

1. PM saves raw input to `inbox/YYYY-MM-DD-<topic>.md`
2. PM invokes Skill 00 (Triage)
3. Triage produces a verdict and creates `runs/YYYY-MM-<name>/00-run-card.md`
4. PM reviews the run card, resolves any flagged gaps, confirms proceed
5. Skills 01 → 02 → 03 → (05) → 04 run in order, one human gate each

## Lifecycle

A run is a **branch**. PM signs off at each step before the next runs. After all required steps are signed off:

1. Approved AC from `02-ac.md` appended to `domains/<domain>/ac-corpus.md`
2. Use case added to the registry table in `ac-corpus.md`
3. `00-run-card.md` status flips to `merged`, merge log filled
4. Run folder stays as historical record — never deleted

## Status values

| Status | Meaning |
|---|---|
| `in-progress` | Pipeline running; at least one step still to produce output |
| `awaiting-sign-off` | All outputs produced; waiting on PM review |
| `merged` | AC merged into domain corpus |
| `parked` | Run paused — blocked on external input or regulatory clarification |
| `abandoned` | Run will not complete; use case scoped out |
