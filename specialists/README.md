# Specialists

One contract per agent. Each contract defines: what the specialist reads, what it produces, what good looks like, where the human gate is.

## What's here

| File | Specialist | Step | Status |
|---|---|---|---|
| `spec-writer.md` | Spec Writer — run card → PRD | 01 | Active |
| `rule-lister.md` | Rule Lister — PRD → AC | 02 | Active |
| `scenario-builder.md` | Scenario Builder — AC → scenarios + SCHEMA-NEEDED flags | 03 | Active |
| `schema-handoff.md` | Schema Handoff — scenarios → TL brief | 04 | Active — default |
| `schema-sketcher.md` | Schema Sketch — scenarios → draft .zed proposals | 05 | Active — optional |

## Pipeline position

Default flow: 01 → 02 → 03 → 04  
With optional step: 01 → 02 → 03 → 05 → 04

Schema Sketch (05) is invoked when new schema elements are needed and you want to give the TL a draft starting point. Skip it when no schema changes are needed, or when you want the TL to design from a blank page.

## The discipline

Each contract is the specification you'd hand to anyone — present-you, future-you, someone at a new org — who needs to invoke this agent and trust the output. The contract names the quality bar; that's what you check at the human gate.
