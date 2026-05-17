# Run Template

This folder defines the shape every run takes. Triage (Skill 00) uses this shape when it creates a new run — the PM does not copy this folder manually.

## Run folder shape

```
runs/YYYY-MM-<short-name>/
├── 00-run-card.md           ← created and populated by Triage
├── 01-prd.md                ← created by Spec Writer (Skill 01)
├── 02-ac.md                 ← created by Rule Lister (Skill 02)
├── 03-scenarios.md          ← created by Scenario Builder (Skill 03)
├── 05-schema-sketch.md      ← created by Schema Sketch (Skill 05) — optional
└── 04-schema-handoff.md     ← created by Schema Handoff (Skill 04) — always last
```

## How a run progresses

1. Triage reads `inbox/<input>.md` → creates `runs/YYYY-MM-<name>/00-run-card.md`
2. PM reviews run card, confirms proceed
3. Skill 01 (Spec Writer) → `01-prd.md` → PM signs off
4. Skill 02 (Rule Lister) → `02-ac.md` → PM signs off
5. Skill 03 (Scenario Builder) → `03-scenarios.md` → PM signs off
6. *(Optional)* Skill 05 (Schema Sketch) → `05-schema-sketch.md` → PM signs off
7. Skill 04 (Schema Handoff) → `04-schema-handoff.md` → PM sends to TL

## After sign-off

- Approved AC merged into `domains/<domain>/ac-corpus.md`
- Use case registered in the corpus registry table
- Run card status → `merged`
- Run folder kept permanently as historical record

## Note for framework contributors

The numbered output files are not pre-stubbed — each specialist creates them from scratch. Pre-stubbing tempts copy-paste editing, which defeats the agent-driven discipline.
